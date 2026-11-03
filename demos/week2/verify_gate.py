"""Week 2 demo: Verify. An agent writes code; a deterministic command, not the agent, decides if it is Done.

    python verify_gate.py                # agent writes slugify.py; the harness runs the tests; Done only if green
    python verify_gate.py --skip-verify  # the "vibes" path: trust the agent's "all tests pass" (see what happens)
    DEMO_OFFLINE=1 python verify_gate.py # no key: canned agent (first attempt is buggy, second is fixed)

This is the rule behind ADE / BMAD (ade.ardata.tech): plan -> build -> verify, and "Done only when the
verification command passes". The agent never gives itself Done. The humans wrote the tests first; they are the
contract. The agent's only tool writes one file, slugify.py, in a temp folder.

DEMO ONLY: it runs model-written code on your machine. In real use run it in a container, and a human reviews
what ships.
"""
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # the demos/ folder
from offline import get_client, reply, text, tool  # noqa: E402

MODEL = os.environ.get("DEMO_MODEL", "claude-opus-5-5")
MAX_ROUNDS = 3  # attempts the harness allows before it stops and hands the problem to a human

TASK = ("Write slugify(text) in slugify.py: lowercase; accents removed (e -> e); every run of characters that "
        "are not letters or digits becomes one '-'; no leading or trailing '-'. Use the write_file tool, then "
        "tell me when you are done.")

TESTS = '''import unittest
from slugify import slugify


class TestSlugify(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_collapses_spaces_and_trims(self):
        self.assertEqual(slugify("  Multiple   spaces "), "multiple-spaces")

    def test_accents(self):
        self.assertEqual(slugify("Cr\\u00e8me Br\\u00fbl\\u00e9e!"), "creme-brulee")

    def test_repeated_separators(self):
        self.assertEqual(slugify("a--b"), "a-b")

    def test_empty(self):
        self.assertEqual(slugify(""), "")


if __name__ == "__main__":
    unittest.main()
'''
# The verification command. Swap for ["pytest", "-q"] in a project that uses pytest.
VERIFY_CMD = [sys.executable, "-m", "unittest", "-v", "test_slugify"]

TOOLS = [{
    "name": "write_file",
    "description": "Write the full contents of slugify.py (replaces the file). The only file you may write.",
    "input_schema": {"type": "object", "properties": {"content": {"type": "string"}},
                     "required": ["content"], "additionalProperties": False},
    "strict": True,
}]

BUGGY = "def slugify(text):\n    return text.lower().replace(' ', '-')\n"
FIXED = '''import re
import unicodedata


def slugify(text):
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")
'''


def scripted_agent(kwargs, call_no):
    """Offline stand-in for the model. Round 1: buggy code and an overconfident claim. Round 2: the fix."""
    messages = kwargs["messages"]
    last = messages[-1]["content"]
    if isinstance(last, list):  # a tool_result just came back: say we are done
        return reply(text("Done. slugify.py is written and all tests pass."))
    if len(messages) == 1:
        return reply(text("Writing slugify.py."), tool("write_file", {"content": BUGGY}))
    return reply(text("Thanks for the failures. Fixing accents and repeated separators."),
                 tool("write_file", {"content": FIXED}))


def verify(workdir):
    """Run the verification command. Its exit code is the only thing that counts. Returns (ok, output)."""
    p = subprocess.run(VERIFY_CMD, cwd=workdir, capture_output=True, text=True, timeout=30)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def agent_turn(client, messages, workdir):
    """One agent run: let it call write_file until it stops calling tools. Returns its last text."""
    for _ in range(6):
        resp = client.messages.create(model=MODEL, max_tokens=2000, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        said = next((b.text for b in resp.content if b.type == "text"), "")
        if resp.stop_reason != "tool_use":
            return said
        results = []
        for b in resp.content:
            if b.type == "tool_use":
                with open(os.path.join(workdir, "slugify.py"), "w") as f:
                    f.write(b.input["content"])
                print(f"  [tool] write_file -> slugify.py ({len(b.input['content'])} chars)")
                results.append({"type": "tool_result", "tool_use_id": b.id, "content": "Wrote slugify.py."})
        messages.append({"role": "user", "content": results})
    return "[agent hit its step limit]"


def main():
    skip = "--skip-verify" in sys.argv
    client = get_client(scripted_agent)
    with tempfile.TemporaryDirectory() as workdir:
        with open(os.path.join(workdir, "test_slugify.py"), "w") as f:
            f.write(TESTS)
        messages = [{"role": "user", "content": TASK}]
        for round_no in range(1, MAX_ROUNDS + 1):
            print(f"\n== Round {round_no}: agent works ==")
            said = agent_turn(client, messages, workdir)
            print(f"  agent says: {said}")
            if skip:
                print("\nDONE (unverified: we believed the agent)")
                ok, out = verify(workdir)
                print(f"  ...but the verification command says: {'green' if ok else 'RED'}")
                print("\n".join("    " + line for line in out.splitlines()[-12:]))
                return 0 if ok else 1
            print(f"== Round {round_no}: harness verifies: {' '.join(VERIFY_CMD[1:])} ==")
            ok, out = verify(workdir)
            print("\n".join("  " + line for line in out.splitlines()))
            if ok:
                print(f"\nDONE: verification command passed (round {round_no}).")
                return 0
            print(f"\nNOT DONE: verification failed (round {round_no}). Failures go back to the agent.")
            messages.append({"role": "user", "content": "The verification command failed. Output:\n" + out[-1500:]
                             + "\nFix slugify.py and say when you are done."})
        print(f"\nNOT DONE: still red after {MAX_ROUNDS} rounds. Stop and hand it to a human.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
