"""A minimal deployable agent service: standard library only (plus the anthropic SDK for live answers).

    GET  /health                 -> {"status": "ok", "version": ..., "mode": "live" | "offline"}
    POST /ask  {"question": ...} -> {"answer": ..., "mode": ..., "usage": {...}, "ms": ...}
    GET  /ask?q=...              -> same, for quick curl tests

Config comes ONLY from environment variables (never from files in the image):
    ANTHROPIC_API_KEY   the key. Unset (or DEMO_OFFLINE=1) = offline mode with a canned answer, for local tests.
    ASK_TOKEN           required in live mode: callers send "Authorization: Bearer <token>". Without it, /ask
                        refuses in live mode so a public URL cannot spend your credit.
    DEMO_MODEL          model id, default claude-opus-5-5
    PORT                default 8080
    APP_VERSION         shown by /health, so you can see which release is running after a deploy or rollback

One JSON log line per request goes to stdout (platforms show stdout as logs). Questions are NOT logged, only sizes.
"""
import json
import os
import signal
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
VERSION = os.environ.get("APP_VERSION", "dev")
MAX_QUESTION_CHARS = 2000
MAX_TOKENS = 400
SYSTEM = ("You are a helpful assistant for a small team. Answer briefly. You only draft text for a human to review; "
          "you cannot send, buy or change anything.")


def offline():
    return os.environ.get("DEMO_OFFLINE") == "1" or not os.environ.get("ANTHROPIC_API_KEY")


_client = None


def answer(question):
    """Returns (text, usage dict). Offline: a canned answer. Live: one real Messages API call."""
    if offline():
        return f"[offline] I received a question of {len(question)} characters. Set ANTHROPIC_API_KEY for a real answer.", {}
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(timeout=30.0, max_retries=2)
    r = _client.messages.create(model=MODEL, max_tokens=MAX_TOKENS, system=SYSTEM,
                                messages=[{"role": "user", "content": question}])
    text = "".join(b.text for b in r.content if b.type == "text")
    return text, {"input_tokens": r.usage.input_tokens, "output_tokens": r.usage.output_tokens}


class Handler(BaseHTTPRequestHandler):
    server_version = "agent-service"

    def log_message(self, *args):  # silence the default access log; we write our own JSON line
        pass

    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _log(self, rid, code, t0, **extra):
        print(json.dumps({"id": rid, "method": self.command, "path": urlparse(self.path).path, "status": code,
                          "ms": round((time.perf_counter() - t0) * 1000), **extra}), flush=True)

    def _ask(self, question):
        rid, t0 = uuid.uuid4().hex[:8], time.perf_counter()
        token = os.environ.get("ASK_TOKEN")
        if not offline() and not token:
            self._send(503, {"error": "ASK_TOKEN is not set; /ask is disabled in live mode"})
            return self._log(rid, 503, t0)
        if token and self.headers.get("Authorization") != f"Bearer {token}":
            self._send(401, {"error": "missing or wrong bearer token"})
            return self._log(rid, 401, t0)
        if not isinstance(question, str) or not question.strip():
            self._send(400, {"error": "send a non-empty 'question'"})
            return self._log(rid, 400, t0)
        if len(question) > MAX_QUESTION_CHARS:
            self._send(413, {"error": f"question longer than {MAX_QUESTION_CHARS} characters"})
            return self._log(rid, 413, t0)
        try:
            text, usage = answer(question)
        except Exception as e:  # never leak details (or keys) to the caller; the log has the type
            self._send(502, {"error": "the model call failed; try again"})
            return self._log(rid, 502, t0, error=type(e).__name__)
        ms = round((time.perf_counter() - t0) * 1000)
        self._send(200, {"answer": text, "mode": "offline" if offline() else "live", "usage": usage, "ms": ms})
        self._log(rid, 200, t0, q_chars=len(question), **usage)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/health":  # cheap: no model call, so the platform can poll it all day
            return self._send(200, {"status": "ok", "version": VERSION, "mode": "offline" if offline() else "live"})
        if url.path == "/ask":
            return self._ask((parse_qs(url.query).get("q") or [""])[0])
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/ask":
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(min(n, 20_000)) or b"{}")
            question = body.get("question") if isinstance(body, dict) else None
        except (ValueError, UnicodeDecodeError):
            question = None
        self._ask(question)


def main():
    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    signal.signal(signal.SIGTERM, lambda *a: sys.exit(0))  # platforms stop containers with SIGTERM
    print(json.dumps({"event": "start", "port": port, "version": VERSION, "mode": "offline" if offline() else "live",
                      "model": MODEL}), flush=True)
    try:
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    main()
