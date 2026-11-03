"""A minimal deployable agent service: standard library plus the anthropic SDK for live answers.

    GET  /health                 -> {"status": "ok", "version": ..., "mode": "live" | "offline"}
    POST /ask  {"question": ...} -> {"answer": ..., "mode": ..., "usage": {...}, "ms": ...}
    GET  /ask?q=...              -> same, for quick curl tests

Config comes ONLY from environment variables (never from files in the image):
    ANTHROPIC_API_KEY  the key. Unset (or DEMO_OFFLINE=1) = offline mode with a canned answer, for local tests.
    ASK_TOKEN          callers send "Authorization: Bearer <token>". Required in live mode so a public URL cannot
                       spend your credit.
    MODEL              model id (VERIFY the id you will use)
    PORT               default 8080
    APP_VERSION        shown by /health so you can see which release is running

One JSON log line per request goes to stdout. Questions are NOT logged, only their size.
Start from demos/week4/deploy/app.py, but write it yourself and understand every line.
"""
import hmac  # noqa: F401
import json
import os
import signal
import sys
import time  # noqa: F401
import uuid  # noqa: F401
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse  # noqa: F401

MODEL = os.environ.get("MODEL", "claude-opus-5-5")  # VERIFY the model id you will really use
MAX_QUESTION_CHARS = 2000
MAX_TOKENS = 400
SYSTEM = ("You are a helpful assistant for a small team. Answer briefly. You only draft text for a human to review; "
          "you cannot send, buy or change anything.")  # TODO for your capstone: replace with your agent's system prompt

_client = None


def offline() -> bool:
    return os.environ.get("DEMO_OFFLINE") == "1" or not os.environ.get("ANTHROPIC_API_KEY")


def set_client(c):
    """Tests use this to plug in a fake model client. None resets to the real one."""
    global _client
    _client = c


def answer(question):
    """Returns (text, usage dict). May raise.

    Offline (and no client set): a canned text that mentions the question length, and {}.
    Otherwise: one messages.create call with model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM and the question as the
    only user message. Use the client from set_client if there is one, else import anthropic and build
    anthropic.Anthropic(timeout=30.0, max_retries=2). Text = the joined text blocks (block.type == "text").
    usage = {"input_tokens": ..., "output_tokens": ...}.
    """
    # TODO: implement
    raise NotImplementedError("answer")


def handle_ask(question, authorization):
    """The whole /ask decision, without HTTP. Returns (status, body). `authorization` is the header value or None.

    Check in this order:
      503 {"error": "... ASK_TOKEN ..."}  live mode (not offline()) and ASK_TOKEN is not set
      401                                 ASK_TOKEN is set and authorization != "Bearer <token>" (compare in constant time: hmac.compare_digest)
      400                                 question is not a non-empty string (spaces only counts as empty)
      413                                 longer than MAX_QUESTION_CHARS
      502 {"error": "..."}                answer() raised: say nothing about why, not even the message
      200 {"answer", "mode": "live" | "offline", "usage", "ms"}
    A refused caller must never reach the model. Add a "_log" key to the body with extra fields for the log line
    ({"error": <exception type>} on 502; {"q_chars": n, **usage} on 200); Handler._send removes it before sending.
    """
    # TODO: implement
    raise NotImplementedError("handle_ask")


def log_request(method, path, status, t0, **extra):
    """One JSON line to stdout per request, flushed: id (short random), method, path, status, ms, and **extra.
    Never put the question or any secret in it. Platforms show stdout as logs."""
    # TODO: implement
    raise NotImplementedError("log_request")


class Handler(BaseHTTPRequestHandler):
    server_version = "agent-service"

    def log_message(self, *args):  # silence the default access log; we write our own JSON line
        pass

    def _send(self, code, body):
        extra = body.pop("_log", {})
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        return extra

    def do_GET(self):
        """GET /health -> 200 {"status": "ok", "version": APP_VERSION or "dev", "mode"}; cheap, NO model call.
        GET /ask?q=... -> handle_ask(q, Authorization header). Anything else -> 404. Log one line per request."""
        # TODO: implement
        self._send(501, {"error": "TODO: do_GET"})

    def do_POST(self):
        """POST /ask with a JSON body {"question": ...} -> handle_ask. Read at most 20_000 bytes. A body that is not
        JSON or not an object counts as no question (400). Any other path -> 404. Log one line per request."""
        # TODO: implement
        self._send(501, {"error": "TODO: do_POST"})


def make_server(host="0.0.0.0", port=None):
    """Build the server. port=0 picks a free port (tests); None reads PORT (default 8080)."""
    return ThreadingHTTPServer((host, int(os.environ.get("PORT", "8080")) if port is None else port), Handler)


def main():
    server = make_server()
    signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))  # platforms stop containers with SIGTERM
    print(json.dumps({"event": "start", "port": server.server_address[1], "version": os.environ.get("APP_VERSION", "dev"),
                      "mode": "offline" if offline() else "live", "model": MODEL}), flush=True)
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
