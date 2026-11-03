"""Cost and latency summary from trace rows. Run on a trace file:  python -m ops.summary traces.jsonl --per-day 2000
"""
import json  # noqa: F401
import statistics  # noqa: F401
import sys

from ops.caching import cache_hit_rate  # noqa: F401


def read_traces(path) -> list:
    """Read a .jsonl trace file into a list of dicts. Blank lines are skipped."""
    # TODO: implement
    raise NotImplementedError("read_traces")


def summarize(rows, per_day=None) -> dict:
    """Numbers for the demo-day line "one request costs about X and takes about Y seconds".

    Calls that share a request_id are one request (their cost and latency add up). A row with no request_id is its own
    request. Return a dict with:
      calls, requests, errors (rows with an "error" key), cost_total, cost_per_request,
      median_latency_ms (median over requests; use statistics.median), max_latency_ms, slowest_task (task of the
      slowest request), cache_hit_rate (ops.caching.cache_hit_rate), and, only when per_day is given,
      projected_per_day and projected_30_days (cost_per_request times per_day, times 30).
    An empty list gives zeros and None, never a ZeroDivisionError.
    """
    # TODO: implement
    raise NotImplementedError("summarize")


def format_summary(s) -> str:
    """The summary as a few plain lines for the terminal or your README.

    Must mention "per request" and "median", and label every dollar figure as example prices to VERIFY.
    """
    # TODO: implement
    raise NotImplementedError("format_summary")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python -m ops.summary traces.jsonl [--per-day N]")
    day = int(sys.argv[sys.argv.index("--per-day") + 1]) if "--per-day" in sys.argv else None
    print(format_summary(summarize(read_traces(sys.argv[1]), day)))
