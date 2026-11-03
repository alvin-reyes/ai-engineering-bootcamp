# 8 · Builder prework: Python, HTTP/JSON and Git refresher

*1–2 hours · Builder track · skip any section you can already do without looking anything up*

Week 1 assumes you can do each of the things below. The code is in `readings/week0/code/` in the course repo: run
it, change it, break it.

## Set up a project the way we will every week

```bash
mkdir prework && cd prework
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install pytest anthropic
```

A virtual environment (`.venv`) keeps each project's packages separate. Activate it in every new terminal.

## Python: types, dataclasses, errors, async

You should be comfortable reading and writing this:

```python
"""Builder prework: typed functions, a dataclass, and an async fan-out."""
import asyncio
import json
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    status: str
    total: float


def parse_order(raw: str) -> Order:
    """Parse one order from JSON text, failing loudly on bad input."""
    data = json.loads(raw)
    missing = {"order_id", "status", "total"} - data.keys()
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    return Order(order_id=str(data["order_id"]), status=str(data["status"]), total=float(data["total"]))


async def fetch_status(order_id: str) -> str:
    await asyncio.sleep(0.1)  # stands in for a slow network call
    return f"{order_id}: delivered"


async def fetch_all(order_ids: list[str]) -> list[str]:
    # run the slow calls at the same time, not one after another
    return await asyncio.gather(*(fetch_status(o) for o in order_ids))


if __name__ == "__main__":
    print(parse_order('{"order_id": "ORD-1", "status": "shipped", "total": "19.90"}'))
    print(asyncio.run(fetch_all(["ORD-1", "ORD-2", "ORD-3"])))
```

Check yourself:
- **Type hints** (`raw: str -> Order`): document what goes in and out; your editor uses them to catch mistakes.
- **Dataclasses** give you a small, typed record without boilerplate.
- **Fail loudly on bad input** (`raise ValueError`) instead of passing half-broken data along. You'll do this with
  every tool input your agent receives.
- **async/await + `asyncio.gather`** run slow network calls at the same time. Agents often call several tools at
  once; this is how.

## Tests with pytest

Every weekly build includes tests, including at least one failure case:

```python
import asyncio
import time

import pytest

from orders import fetch_all, parse_order


def test_parses_a_good_order():
    order = parse_order('{"order_id": "ORD-1", "status": "shipped", "total": 19.9}')
    assert order.order_id == "ORD-1" and order.total == 19.9


def test_rejects_an_order_with_missing_fields():
    with pytest.raises(ValueError, match="total"):
        parse_order('{"order_id": "ORD-1", "status": "shipped"}')


def test_fetches_concurrently():
    start = time.perf_counter()
    assert len(asyncio.run(fetch_all(["a", "b", "c"]))) == 3
    assert time.perf_counter() - start < 0.25  # three 0.1 s calls at once, not 0.3 s in a row
```

Run them with `pytest -q`. All three should pass. Then break `parse_order` on purpose and watch a test fail.

## HTTP and JSON

LLM APIs are HTTP APIs that send and receive JSON. You should be able to call one, handle errors, and pull out the
fields you need. This uses only the standard library (the official SDKs wrap the same ideas):

```python
"""Builder prework: call a JSON API (PyPI package info) with the standard library, with a timeout and error handling."""
import json
import sys
import urllib.error
import urllib.request

package = sys.argv[1] if len(sys.argv) > 1 else "anthropic"
url = f"https://pypi.org/pypi/{package}/json"  # PyPI's public JSON API: no key needed
request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "bootcamp-prework"})
try:
    with urllib.request.urlopen(request, timeout=10) as response:
        data = json.load(response)
except urllib.error.HTTPError as err:
    sys.exit(f"HTTP {err.code}: the server answered with an error")
except urllib.error.URLError as err:
    sys.exit(f"Network problem: {err.reason}")
info = data["info"]
print({"name": info["name"], "latest_version": info["version"], "summary": info["summary"]})
```

```bash
python http_json.py anthropic          # prints the package's name, latest version, summary
python http_json.py no-such-package    # shows the error path (HTTP 404)
```

Know these status codes: **200** OK · **400** your request is wrong (fix it, don't retry) · **401/403** auth ·
**404** not found · **429** rate limited (wait, retry) · **5xx** server problem (retry with backoff).

## Environment variables, not keys in code

```bash
export ANTHROPIC_API_KEY=...   # in your shell, never in a file you commit
```

```python
import os
key = os.environ["ANTHROPIC_API_KEY"]   # the Anthropic SDK reads it for you automatically
```

Add `.env` and `.venv/` to your `.gitignore` on day one.

## Git and GitHub

The everyday loop for each weekly build:

```bash
git checkout -b week1-build          # a branch for this piece of work
git add -A && git commit -m "Streaming assistant with structured summary"
git push -u origin week1-build       # then open a pull request on GitHub for review
```

You should be able to: clone a repo, branch, commit, push, open a pull request, and read a review comment. Run
`git status` before every commit to make sure no secrets or `.venv` are about to go in.

<!-- diagram:git-flow -->
<figure class="diagram">
<svg viewBox="0 0 820 210" role="img" aria-label="The Git loop for each weekly build: branch off main, commit as you go, push, open a pull request, get it reviewed, then merge back into main." xmlns="http://www.w3.org/2000/svg" font-family="Inter, Helvetica, Arial, sans-serif"><defs><marker id="git-n" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker><marker id="git-r" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#E0141F"/></marker></defs><line x1="30" y1="160" x2="790" y2="160" stroke="currentColor" stroke-width="2" stroke-opacity="0.8"/><text x="30" y="186" font-size="13" font-weight="700" text-anchor="start" fill="currentColor" fill-opacity="0.8">main</text><circle cx="60" cy="160" r="6" fill="currentColor" fill-opacity="0.85"/><circle cx="120" cy="160" r="6" fill="currentColor" fill-opacity="0.85"/><circle cx="700" cy="160" r="6" fill="currentColor" fill-opacity="0.85"/><circle cx="760" cy="160" r="6" fill="currentColor" fill-opacity="0.85"/><path d="M120,160 C160,160 160,70 200,70" fill="none" stroke="#E0141F" stroke-width="2"/><line x1="200" y1="70" x2="560" y2="70" stroke="#E0141F" stroke-width="2" stroke-opacity="1"/><path d="M560,70 C640,70 660,160 700,160" fill="none" stroke="#E0141F" stroke-width="2"/><circle cx="240" cy="70" r="6" fill="#E0141F"/><text x="240" y="52" font-size="12" font-weight="600" text-anchor="middle" fill="currentColor" fill-opacity="0.8">commit</text><circle cx="330" cy="70" r="6" fill="#E0141F"/><text x="330" y="52" font-size="12" font-weight="600" text-anchor="middle" fill="currentColor" fill-opacity="0.8">commit</text><circle cx="420" cy="70" r="6" fill="#E0141F"/><text x="420" y="52" font-size="12" font-weight="600" text-anchor="middle" fill="currentColor" fill-opacity="0.8">commit</text><text x="150" y="186" font-size="12.5" font-weight="700" text-anchor="start" fill="#E0141F" fill-opacity="0.9">git checkout -b week1-build</text><rect x="470" y="92" width="150" height="50" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-opacity="0.55"/><text x="545.0" y="113.0" font-size="15" font-weight="700" text-anchor="middle" fill="currentColor">Pull request</text><text x="545.0" y="132.0" font-size="12.5" font-weight="400" text-anchor="middle" fill="currentColor" fill-opacity="0.75">review → fix → approve</text><text x="500" y="40" font-size="12.5" font-weight="700" text-anchor="middle" fill="currentColor" fill-opacity="0.9">git push</text><text x="700" y="132" font-size="12.5" font-weight="700" text-anchor="middle" fill="currentColor" fill-opacity="0.9">merge</text></svg>
<figcaption>One branch per weekly build. Commit small, push, open a pull request, answer the review, and only then merge into main.</figcaption>
</figure>
<!-- /diagram:git-flow -->

## Ready check

- [ ] `pytest -q` passes the three tests above, and you can make one fail on purpose
- [ ] `http_json.py` prints package info, and you can explain what happens on a 404 or a 429
- [ ] You can explain why `asyncio.gather` is faster for three slow calls
- [ ] You've pushed a branch to GitHub and opened a pull request
- [ ] `demos/kickoff/hello_llm.py` streams a reply with your API key
