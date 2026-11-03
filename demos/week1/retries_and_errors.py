"""Week 1 demo (deck slides 05 and 07): max_tokens, bad requests and retries.

    python week1/retries_and_errors.py
    DEMO_OFFLINE=1 python week1/retries_and_errors.py     no key: errors are simulated with the SDK's own exception classes

A: a reply cut off by max_tokens (check stop_reason).  B: a 400 (fix it, never retry unchanged).
C: which errors to retry, and a small backoff wrapper. The SDK already retries 429 and 5xx twice by default
(Anthropic(max_retries=2)); this shows what that does for you. A real 429 cannot be forced on demand, so C is simulated.
"""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos/ folder, for offline.py
import anthropic  # noqa: E402
from types import SimpleNamespace  # noqa: E402

from offline import get_client, reply, text  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")


def make_error(cls, status):
    fake = SimpleNamespace(status_code=status, headers={}, request=None)  # just what the exception reads
    return cls(f"simulated {status}", response=fake, body=None)


def responder(kw, call_no):  # offline only
    if kw["max_tokens"] < 1:
        raise make_error(anthropic.BadRequestError, 400)
    if kw["max_tokens"] < 60:
        return reply(text("Retries matter because networks and shared services fail in"), stop="max_tokens")
    return reply(text("Retry only errors that can fix themselves: rate limits and server errors."))


client = get_client(responder)
ASK = [{"role": "user", "content": "In four sentences, why do API calls need retries?"}]


def retryable(exc):
    """429 (rate limit), 5xx (server, 529 overloaded) and dropped connections: yes. 400, 401, 403, 404: no."""
    if isinstance(exc, anthropic.APIStatusError):
        return exc.status_code == 429 or exc.status_code >= 500
    return isinstance(exc, (anthropic.APIConnectionError, anthropic.APITimeoutError))


def with_backoff(fn, tries=4, base=0.2):
    for attempt in range(1, tries + 1):
        try:
            return fn()
        except Exception as exc:
            if not retryable(exc) or attempt == tries:
                raise
            wait = base * 2 ** (attempt - 1)
            print(f"  attempt {attempt} failed ({type(exc).__name__}); waiting {wait:.1f}s")
            time.sleep(wait)


def main():
    print("A. max_tokens too small")
    r = client.messages.create(model=MODEL, max_tokens=20, messages=ASK)
    print("  reply      :", next(b.text for b in r.content if b.type == "text"))
    print("  stop_reason:", r.stop_reason, "-> CUT OFF, not finished" if r.stop_reason == "max_tokens" else "")

    print("\nB. a bad request (max_tokens=0)")
    try:
        client.messages.create(model=MODEL, max_tokens=0, messages=ASK)
    except anthropic.BadRequestError as exc:
        print(f"  HTTP {exc.status_code} BadRequestError; retryable? {retryable(exc)}. Fix the request.")

    print("\nC. retry the retryable (simulated: 429, then 529 overloaded, then success)")
    errors = [make_error(anthropic.RateLimitError, 429), make_error(anthropic.OverloadedError, 529)]

    def flaky():
        if errors:
            raise errors.pop(0)
        return "success"
    print("  result:", with_backoff(flaky))
    for cls, code in ((anthropic.RateLimitError, 429), (anthropic.InternalServerError, 500),
                      (anthropic.BadRequestError, 400), (anthropic.AuthenticationError, 401)):
        print(f"  {code} {cls.__name__:<22} retry? {retryable(make_error(cls, code))}")


if __name__ == "__main__":
    main()
