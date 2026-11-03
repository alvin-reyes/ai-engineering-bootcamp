"""Week 1 demo (deck slide 03): tokens, context and cost.

    python week1/tokens_and_cost.py
    DEMO_OFFLINE=1 python week1/tokens_and_cost.py     no key: estimates at about 4 characters a token

Live, it asks the API to count (messages.count_tokens). Offline, it estimates and says so: real counts differ,
and differ most for code, other languages and numbers.
Prices are EXAMPLES, not real. Set DEMO_PRICE_IN / DEMO_PRICE_OUT (US$ per million tokens) from the pricing page.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the demos/ folder, for offline.py
from offline import approx_tokens, get_client, offline_mode  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
PRICE_IN = float(os.environ.get("DEMO_PRICE_IN", "5.00"))     # example only: VERIFY on the pricing page
PRICE_OUT = float(os.environ.get("DEMO_PRICE_OUT", "25.00"))  # example only: VERIFY on the pricing page

HANDBOOK = "Employees must report a lost or stolen laptop to IT within 24 hours. " * 400
SAMPLES = {
    "English sentence": "The quick brown fox jumps over the lazy dog.",
    "Filipino sentence": "Mahalaga na iulat agad sa IT ang nawawalang laptop sa loob ng 24 oras.",
    "Python code": "def total(items):\n    return sum(i['price'] * i['qty'] for i in items)\n",
    "JSON": '{"id": 1042, "status": "shipped", "items": [{"sku": "A-17", "qty": 3}]}',
    "Long document (400 repeats)": HANDBOOK,
}

client = get_client(lambda kw, n: {"content": [], "stop_reason": "end_turn"})  # only count_tokens is used


def count(text):
    if offline_mode():
        return approx_tokens(text)
    return client.messages.count_tokens(model=MODEL, messages=[{"role": "user", "content": text}]).input_tokens


def main():
    how = "estimated (about 4 chars/token)" if offline_mode() else f"counted by the API for {MODEL}"
    print(f"Tokens: {how}. Example price ${PRICE_IN}/M in, ${PRICE_OUT}/M out.\n")
    print(f"{'input':<30}{'chars':>8}{'tokens':>8}{'chars/tok':>11}{'$ per call':>12}")
    for name, text in SAMPLES.items():
        n = count(text)
        print(f"{name:<30}{len(text):>8}{n:>8}{len(text) / n:>11.1f}{n * PRICE_IN / 1e6:>12.5f}")

    doc = count(HANDBOOK)
    reply = 300  # output tokens per answer, an assumption
    print(f"\nAsk 20 questions about the long document, resending it each time (the API is stateless):")
    print(f"  input  {doc} x 20 = {doc * 20} tokens -> ${doc * 20 * PRICE_IN / 1e6:.4f}")
    print(f"  output {reply} x 20 = {reply * 20} tokens -> ${reply * 20 * PRICE_OUT / 1e6:.4f}  (assumed {reply} per answer)")
    print("  Output costs more per token, but the long document dominates. Week 4: caching cuts the repeat.")


if __name__ == "__main__":
    main()
