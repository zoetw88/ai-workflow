# LLM Application Pitfalls — what AI-app builders keep getting wrong

Read before building anything that puts an LLM in production: agents, RAG,
chatbots, pipelines. Same spirit as go.md/python.md — these are recurring traps.

## Prompt injection (the #1 interview question and the #1 real risk)

Threat model in one line: **anything the model reads can try to steer it** —
web pages, retrieved docs, file contents, tool outputs, user uploads, PR
comments. Defense is layered, never a single filter:

1. **Trust boundaries in the prompt.** Wrap external content in explicit
   markers and tell the model it's data, not instructions. Never concatenate
   untrusted text into the system prompt.
2. **Capability limits beat instructions.** An injected "ignore previous
   instructions" can't exfiltrate what the process can't reach: scope tool
   permissions per task, run tools in a sandbox, keep secrets out of the
   sandbox entirely (inject credentials at egress / host-side, never in
   context — a secret in the prompt is readable by any injection).
3. **Human gates on irreversible actions.** Sending, deleting, paying,
   publishing → confirm with a human, always. Injection then costs at most a
   wasted turn, not an incident.
4. **Detect the redirect.** If content from an external source asks the agent
   to change task, escalate access, or touch unrelated systems — stop and
   surface it instead of complying.

## Secrets and PII

- NEVER put API keys or credentials in system prompts or messages — they
  persist in logs, event history, and caches for the life of the session.
- LLM traces are logs: scrub PII before storing; never log full prompts
  containing user data without a retention policy.
- Model outputs can leak inputs. If the context contains secrets, assume any
  output channel (including error messages) can echo them.

## No evals = no engineering

- A prompt change without a regression suite is a deploy without tests.
  Keep golden cases; grade with rubrics (LLM-as-judge for open-ended output,
  exact/structural checks where possible); run on every prompt/model change.
- Measure the baseline (no-skill / no-RAG / smaller model) — if you can't
  show the delta, you can't justify the cost.
- Non-determinism means N runs per case, not 1. Report pass rate, not a
  single anecdote.

## Context management

- Prompt caching is a prefix match: timestamps, UUIDs, unsorted JSON anywhere
  early in the prompt silently kill the cache. Stable content first, volatile
  content last.
- Don't re-explore what you can cache in a file: repeated discovery cost
  across sessions is a design smell (persist maps/notes, read them first).
- Long conversations need a plan: compaction or context editing, chosen
  deliberately — not "hope the window is big enough".

## Cost engineering

- Route by task, not by habit: top model for judgment-heavy steps, mid-tier
  for building, cheapest for mechanical verification. Revisit routing every
  model generation.
- Token counts are model-specific: re-baseline with count_tokens when
  switching models; never estimate with another vendor's tokenizer.
- Bound agentic loops: max turns, token budgets, cost ceilings. An unbounded
  loop is an unbounded bill.

## Output handling

- Never string-match serialized tool inputs — always parse JSON (escaping
  varies by model version).
- Check stop_reason before reading content: refusal / max_tokens / tool_use
  all need different handling; index-zero-and-pray crashes on refusals.
- Structured output beats "please reply in JSON": use schema enforcement
  where the API supports it; validate anyway.

## Agent design

- One agent per context, one context per concern: parallel read-only fan-out
  is cheap and safe; parallel writers need isolation (worktrees, containers).
- Sub-agent reports are claims, not facts: verify file paths and diffs before
  acting on them.
- Instructions are not enforcement: anything that MUST happen needs a
  mechanism (hook, schema, gate), not a sentence in the prompt.

## Pre-ship checklist

- [ ] External content wrapped and treated as data; injection redirect path tested
- [ ] Tool permissions scoped; secrets unreachable from model context
- [ ] Human confirmation on irreversible actions
- [ ] Eval suite exists and runs on prompt/model changes; baseline measured
- [ ] stop_reason handling covers refusal and max_tokens
- [ ] Loop bounds: max turns / token budget / cost ceiling
- [ ] Cache hit rate verified (cache_read_input_tokens > 0 on repeat traffic)
