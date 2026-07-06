---
name: go-pitfalls
description: Use before writing or reviewing Go code. Pre-write checklist of traps AI repeatedly hits — context propagation, goroutine ownership, error wrapping, HTTP timeouts, data races.
---

<!-- Canonical source: ~/.ai-workflow/pitfalls/go.md — if that file exists on this machine,
     read it instead; it may be newer than this embedded copy. -->

Treat this as a pre-write checklist. Re-read before generating Go code touching these areas.

## Context (`context.Context`)

- Every I/O / RPC / DB call MUST accept `ctx`.
- `ctx` is always the FIRST parameter — never anywhere else.
- NEVER store `ctx` in a struct.
- HTTP handlers: use `r.Context()`, do NOT call `context.Background()`.
- When you spawn a goroutine inside a request, propagate the parent `ctx`. Never `context.Background()` there.
- `context.WithTimeout` always paired with `defer cancel()`. Forgetting is a leak.
- Don't use context for passing optional data (the `WithValue` anti-pattern).

## Goroutines

- Before spawning, answer: **who cancels it? who waits for it?** If you can't answer both, don't spawn.
- Use `errgroup.WithContext` instead of bare `sync.WaitGroup` + manual error channel.
- `defer wg.Done()` MUST be the FIRST line inside the goroutine.
- Channels without a reader leak the writer. Always bound your producer or use `select` with `ctx.Done()`.
- Avoid `go func() { ... }()` at the end of an HTTP handler — request `ctx` is canceled when the response is sent.

## Interfaces

- **Accept interfaces, return structs.**
- Don't extract an interface "for testability" if there's only one implementation.
- Small interfaces beat large ones (`io.Reader` is 1 method).
- Don't make `*T` AND `T` both satisfy an interface — pick one receiver style.

## Errors

- Compare with `errors.Is(err, ErrFoo)` — NEVER `err == ErrFoo`.
- Extract with `errors.As(err, &target)`.
- Wrap with `fmt.Errorf("doing X: %w", err)` — the `%w` is mandatory.
- Sentinel errors: `var ErrNotFound = errors.New(...)` at package level.
- NEVER `panic` in library code.
- Don't swallow errors with `_ = doSomething()`.

## Generics (Go 1.18+)

- Write concrete first. Generalize after the THIRD repetition.
- Cap type parameters at 2.
- Use `~int` in constraints to allow named types.
- Generics ≠ polymorphism. For runtime dispatch, use interfaces.

## Concurrency primitives

- Reads + writes on a `map` from multiple goroutines = data race. Use `sync.Map` (read-heavy) or `sync.RWMutex` + plain map.
- Counters: `atomic.Int64`, not `int64 + Mutex`.
- `sync.Once` for lazy init — but prefer eager init at package level if possible.
- `select` with no `default` blocks; with `default` is non-blocking poll.

## HTTP servers

- Always set timeouts: `ReadHeaderTimeout`, `ReadTimeout`, `WriteTimeout`, `IdleTimeout`. Zero = unlimited = slowloris.
- `http.DefaultClient` has no timeout. NEVER use it in production.
- Close response bodies: `defer resp.Body.Close()` immediately after the error check.
- Drain before close to reuse connection: `io.Copy(io.Discard, resp.Body)`.

## Testing

- `t.Parallel()` requires careful state isolation.
- Use `testing/quick` or `gopter` for property-based tests on pure functions.
- Capture loop variable `tc := tc` before `t.Run` in pre-1.22 code.
- `t.Cleanup()` beats `defer` for ordered teardown.
- Always run `-race` in CI.

## Module hygiene

- `replace` directives should be temporary. Audit them.
- Many `// indirect` lines → run `go mod tidy`.
- Pinning to commit hash is fine but flag for upgrade later.

## Pre-commit checklist

- [ ] All exported funcs have doc comments
- [ ] `go vet ./...` passes
- [ ] `staticcheck ./...` passes (if installed)
- [ ] `go test -race -count=1 ./...` passes
- [ ] No `context.Background()` introduced inside request paths
- [ ] No new goroutines without a documented owner
