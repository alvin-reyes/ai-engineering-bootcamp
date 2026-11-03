"""Tracing: wrap every model call, write one JSON line per call (latency, tokens, estimated cost).

    tracer = Tracer(client)
    response = tracer.call("triage", request_id="req-1", model=MODEL, max_tokens=300, system=..., messages=[...])

A trace line never contains the prompt or the answer, only sizes and timings, so it is safe to keep and share.
Start from demos/week4/tracing_cost.py, but make it yours: understand every line before you keep it.
"""
import json  # noqa: F401
import time  # noqa: F401
from pathlib import Path  # noqa: F401

# Example prices, USD per million tokens. NOT real quotes. VERIFY against the current pricing page before you
# show a cost to anyone. Cache write = 1.25x input and cache read = 0.1x input is the usual pattern: VERIFY that too.
PRICE_INPUT = 5.00        # example price, VERIFY
PRICE_OUTPUT = 25.00      # example price, VERIFY
PRICE_CACHE_WRITE = 6.25  # example price, VERIFY
PRICE_CACHE_READ = 0.50   # example price, VERIFY


def estimate_cost(usage) -> float:
    """USD for one call from a usage object.

    The usage object has input_tokens, output_tokens, cache_creation_input_tokens and cache_read_input_tokens.
    A missing or None field counts as 0. Prices are per MILLION tokens.
    """
    # TODO: implement
    raise NotImplementedError("estimate_cost")


class Tracer:
    """Wraps client.messages.create. Records a trace line per call, even when the call fails."""

    def __init__(self, client, path="traces.jsonl", echo=True, fresh=True):
        """client: anything with client.messages.create(**kw). path: the .jsonl file. echo: also print each line.
        fresh: start the file empty. Keep every row in self.rows too."""
        # TODO: implement
        raise NotImplementedError("Tracer.__init__")

    def call(self, task, request_id=None, **kw):
        """Make the call with client.messages.create(**kw), time it, log it, return the response unchanged.

        Each trace line is one JSON object with: call (1, 2, 3...), request_id, task, model, latency_ms (int),
        input_tokens, output_tokens, cache_write, cache_read, stop_reason, cost_usd (rounded to 6 places).

        If the call raises: log a line with latency_ms, error (the exception TYPE name only, never its message, it
        may hold a secret) and cost_usd 0.0, then re-raise. Never log the prompt or the answer text.
        """
        # TODO: implement (time with time.perf_counter, write with self._log)
        raise NotImplementedError("Tracer.call")

    def _log(self, row):
        """Append row to self.rows, print "TRACE <json>" if echo, and append the JSON line to the file."""
        # TODO: implement
        raise NotImplementedError("Tracer._log")

    def summary(self, per_day=None):
        """Print the summary table and return the numbers: use ops.summary.summarize and format_summary."""
        # TODO: implement
        raise NotImplementedError("Tracer.summary")
