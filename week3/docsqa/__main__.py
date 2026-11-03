"""Command line.

    python -m docsqa ask "How many days do customers have to return a bike?"
    python -m docsqa eval [--k 5] [--retrieval-only]
"""
import argparse
import os

from .answer import answer_question, get_client
from .evalrun import load_eval_set, recall_at_k, run_eval
from .ingest import ingest
from .retrieve import Retriever


def main(argv=None):
    p = argparse.ArgumentParser(prog="docsqa")
    p.add_argument("command", choices=["ask", "eval"])
    p.add_argument("question", nargs="?")
    p.add_argument("--docs", default="docs")
    p.add_argument("--evalset", default="evalset/eval_set.jsonl")
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--retrieval-only", action="store_true", help="skip the model: report recall only")
    a = p.parse_args(argv)
    retriever = Retriever(ingest(a.docs))
    if a.command == "ask":
        ans = answer_question(a.question or "", retriever, get_client())
        print(ans.text)
        print("Sources:", ", ".join(ans.citations) or "none")
        return
    cases = load_eval_set(a.evalset)
    if a.retrieval_only or not os.environ.get("ANTHROPIC_API_KEY"):
        print(f"cases: {len(cases)}   recall@{a.k}: {recall_at_k(cases, retriever, a.k):.0%}   (answer accuracy needs a key)")
        return
    r = run_eval(cases, retriever, get_client(), a.k)
    print(f"cases: {r['n']}   recall@{a.k}: {r['recall_at_k']:.0%}   answer accuracy: {r['accuracy']:.0%}")
    print("failing cases:", ", ".join(r["failures"]) or "none")


if __name__ == "__main__":
    main()
