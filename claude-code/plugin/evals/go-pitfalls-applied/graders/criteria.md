# Grading criteria: go-pitfalls rules survive into generated code

The prompt asks for a Go HTTP handler that spawns a background job and returns
immediately. This is a trap the go-pitfalls skill explicitly covers: the
request context is canceled when the response is sent, so the goroutine must
NOT inherit r.Context() directly for its outbound call, must NOT use
context.Background() bare (no timeout = leak), and goroutine ownership (who
cancels it, who waits) should be addressed.

Score 1.0 if ALL of:
- The background goroutine does not use r.Context() for the 30s outbound call
  (uses context.WithTimeout over a detached/base context, or an explicit
  worker/queue pattern)
- Any context.WithTimeout/WithCancel is paired with defer cancel()
- The outbound HTTP call does not use http.DefaultClient (or sets an explicit
  timeout on the client), and goroutine ownership is at least acknowledged
  (bounded worker, errgroup, or a comment on cancellation/lifetime)

Score 0.5 if the code avoids the r.Context() cancellation bug but misses the
other hygiene points (bare context.Background() with no timeout, or
http.DefaultClient, or no defer cancel()).

Score 0.0 if the goroutine uses r.Context() for the background call (it will
be canceled the moment 202 is returned), or the code ignores context entirely.
