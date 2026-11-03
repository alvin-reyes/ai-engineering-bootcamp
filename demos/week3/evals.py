"""Week 3 demo: a small eval set, code-graded checks + a model-graded rubric judge, and "measure the change".

    python evals.py                    # live if ANTHROPIC_API_KEY is set, else offline replay (canned answers)
    DEMO_OFFLINE=1 python evals.py     # force offline, even with a key

Two prompt versions answer the same 10 cases. Cheap checks run in code (contains, citation, "I don't know",
valid JSON); a rubric judge (a second model call) grades correctness and grounding. The table at the end is the
point: one change, one number before and after. Offline, the answers AND the judge's grades are canned, so you
see the mechanics, not real model quality. VERIFY live once with your key.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from offline import get_client, reply, text  # noqa: E402
from rag_eval import SYSTEM as PROMPT_V2, chunks, offline_responder as v2_answer, tfidf_retriever  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
PROMPT_V1 = "You are a helpful assistant. Use the documents to answer the question."

# question, phrase a correct answer must contain (None = unanswerable: the right reply is "I don't know")
CASES = [
    ("How long do I have to submit expenses?", "30 days"),
    ("What is the daily meal allowance when travelling?", "50 EUR"),
    ("Do I need a receipt for a 40 EUR taxi?", "25 EUR"),
    ("How far ahead should I book flights?", "14 days"),
    ("How fast must I report a stolen laptop?", "24 hours"),
    ("Where do I order an XK-2041?", "IT catalogue"),
    ("How many vacation days do I get?", "25 days"),
    ("I was sick for 5 days, what do I need?", "doctor"),
    ("What is the company's parental leave policy?", None),
    ("What is the CEO's phone number?", None),
]
JSON_CASES = [  # asked for structured output: graded by "is it valid JSON with the right keys"
    ("How long do I have to submit expenses?", "30 days"),
    ("How many vacation days do I get?", "25 days"),
]
ANSWER_SCHEMA = {"type": "object", "properties": {"answer": {"type": "string"}, "source": {"type": "string"}},
                 "required": ["answer", "source"], "additionalProperties": False}
JUDGE_SCHEMA = {"type": "object", "properties": {"correct": {"type": "boolean"}, "grounded": {"type": "boolean"},
                "reason": {"type": "string"}}, "required": ["correct", "grounded", "reason"],
                "additionalProperties": False}
RUBRIC = ("You grade answers from a docs Q&A bot. Rubric: correct = the answer matches the reference (or, when the "
          "reference says UNANSWERABLE, the answer says it does not know). grounded = every claim is supported by "
          "the chunks shown and nothing is invented. Reply as JSON.")


# ---------- offline stand-ins (canned: they show the mechanics, not a real model) ----------
def v1_answer(kwargs, call_no):
    """A weak prompt: never cites, never says 'I don't know' (it makes something up when nothing matches)."""
    out = v2_answer(kwargs, call_no)
    t = out["content"][0]["text"]
    if t.startswith("I don't know"):
        return reply(text("Employees typically get 12 weeks, but check with your manager."))
    return reply(text(re.sub(r"\s*\[[A-Za-z]+\]", "", t)))


def offline_model(kwargs, call_no):
    if "output_config" in kwargs and kwargs["system"].startswith("You grade"):
        user = kwargs["messages"][0]["content"]
        ref = re.search(r"Reference: (.*)", user).group(1).strip()
        ans = re.search(r"Answer: (.*)", user, re.S).group(1).strip()
        ok = ("don't know" in ans.lower()) if ref == "UNANSWERABLE" else (ref.lower() in ans.lower())
        reason = "matches the reference" if ok else "does not match the reference"
        return reply(text(json.dumps({"correct": ok, "grounded": ok, "reason": reason})))
    if "output_config" in kwargs:  # structured answer request
        base = v2_answer(kwargs, call_no)["content"][0]["text"]
        src = re.search(r"\[([A-Za-z]+)\]", base)
        return reply(text(json.dumps({"answer": re.sub(r"\s*\[[A-Za-z]+\]", "", base),
                                      "source": src.group(1) if src else "none"})))
    return (v2_answer if kwargs["system"] == PROMPT_V2 else v1_answer)(kwargs, call_no)


# ---------- the system under test ----------
def ask(client, system, question, retrieve, cs, structured=False):
    context = "\n\n".join(f'<chunk id="{c}">\n{cs[c]}\n</chunk>' for c in retrieve(question, 2))
    kw = dict(model=MODEL, max_tokens=512, system=system,
              messages=[{"role": "user", "content": f"{context}\n\nQuestion: {question}"}])
    if structured:
        kw["output_config"] = {"format": {"type": "json_schema", "schema": ANSWER_SCHEMA}}
    r = client.messages.create(**kw)
    return next((b.text for b in r.content if b.type == "text"), ""), context


# ---------- graders ----------
def code_checks(answer, expected):
    """Cheap, deterministic, run first."""
    if expected is None:
        return {"idk": "don't know" in answer.lower()}
    return {"contains": expected.lower() in answer.lower(), "cited": bool(re.search(r"\[[A-Za-z]+\]", answer))}


def judge(client, question, expected, answer, context):
    user = f"{context}\n\nQuestion: {question}\nReference: {expected or 'UNANSWERABLE'}\nAnswer: {answer}"
    r = client.messages.create(model=MODEL, max_tokens=300, system=RUBRIC,
                               messages=[{"role": "user", "content": user}],
                               output_config={"format": {"type": "json_schema", "schema": JUDGE_SCHEMA}})
    g = json.loads(next(b.text for b in r.content if b.type == "text"))
    return g["correct"] and g["grounded"], g["reason"]


def run_version(client, system, retrieve, cs):
    rows = []
    for q, expected in CASES:
        ans, ctx = ask(client, system, q, retrieve, cs)
        checks = code_checks(ans, expected)
        ok, why = judge(client, q, expected, ans, ctx)
        rows.append({"q": q, "answer": ans, "checks": checks, "judge": ok, "why": why,
                     "pass": all(checks.values()) and ok})
    json_ok = 0
    for q, expected in JSON_CASES:
        ans, _ = ask(client, system, q, retrieve, cs, structured=True)
        try:
            d = json.loads(ans)
            json_ok += set(d) == {"answer", "source"} and expected.lower() in d["answer"].lower()
        except json.JSONDecodeError:
            pass
    return rows, json_ok


def pct(n, d):
    return f"{n}/{d} = {n/d:.0%}" if d else "n/a"


def summary(rows, json_ok):
    ans = [r for r in rows if "contains" in r["checks"]]
    unans = [r for r in rows if "idk" in r["checks"]]
    return {
        "contains answer (code)": pct(sum(r["checks"]["contains"] for r in ans), len(ans)),
        "citation present (code)": pct(sum(r["checks"]["cited"] for r in ans), len(ans)),
        "says I don't know (code)": pct(sum(r["checks"]["idk"] for r in unans), len(unans)),
        "valid JSON + keys (code)": pct(json_ok, len(JSON_CASES)),
        "judge: correct+grounded": pct(sum(r["judge"] for r in rows), len(rows)),
        "OVERALL pass rate": pct(sum(r["pass"] for r in rows), len(rows)),
    }


if __name__ == "__main__":
    cs = chunks()
    retrieve = tfidf_retriever(cs)
    client = get_client(offline_model)
    results = {}
    for name, system in (("v1 (weak prompt)", PROMPT_V1), ("v2 (cite + say I don't know)", PROMPT_V2)):
        results[name] = run_version(client, system, retrieve, cs)
    s1, s2 = (summary(*results[n]) for n in results)
    names = list(results)
    print(f"{'check':28s} {names[0]:>18s} {names[1]:>30s}")
    for k in s1:
        print(f"{k:28s} {s1[k]:>18s} {s2[k]:>30s}")
    print("\nCases that changed (v1 -> v2):")
    for r1, r2 in zip(results[names[0]][0], results[names[1]][0]):
        if r1["pass"] != r2["pass"]:
            print(f"  {r1['q']}\n    v1 {'PASS' if r1['pass'] else 'FAIL'}: {r1['answer']}"
                  f"\n    v2 {'PASS' if r2['pass'] else 'FAIL'}: {r2['answer']}  (judge: {r2['why']})")
    print("\nFailing for v2:", [r["q"] for r in results[names[1]][0] if not r["pass"]] or "none")
