# Week 4 starter: make your capstone production-worthy

This is the learner starter for the final build. You drop these pieces into **your own capstone** (not a toy), make
the tests pass, and show it on demo day (Fri 4 Dec). Everything here is a skeleton: signatures, docstrings and
`# TODO:` markers. You write the code, and you must be able to explain every line of it. If an AI helps you write it,
you still explain it.

Read first: `readings/week4/` (readings 1 to 5, `lab.md`, `build.md`). Examples to read, not copy blindly:
`demos/week4/` (`tracing_cost.py`, `caching_demo.py`, `injection_redteam.py`, `deploy/`).

## What is in the box

| Path | You build | Week 4 topic |
|---|---|---|
| `ops/tracing.py` | `estimate_cost`, `Tracer`: one JSON line per model call (latency, tokens, estimated cost) | Tracing and cost |
| `ops/summary.py` | `summarize`, `format_summary`, `read_traces`: cost per request, median latency, slowest case | Tracing and cost |
| `ops/caching.py` | `build_request`, `find_volatile`, `cache_hit_rate`: stable prefix first, `cache_control` | Caching and latency |
| `ops/guard.py` | `wrap_untrusted`, `guard_system`, `requires_approval`, `run_tool_call`, `check_output` | Security and injection |
| `deploy/` | `app.py` (`/health`, `/ask`), `Dockerfile`, `fly.toml`, `railway.json`, `README.md` | Deploying |
| `lab/` | `attacks.json`, `redteam_worksheet.md`, `run_attacks.py`, `README.md` | Lab parts 2 and 3 |
| `tests/` | Already written. They encode the criteria below. Do not edit them to make them pass. | |

## Run and test

Python 3.11 or newer. No API key and no network are needed for the tests: they use a fake model client
(`tests/conftest.py`) and run the service on a free localhost port.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                          # at the start most tests FAIL. That is the point: red, then green.
pytest tests/test_tracing.py    # one file at a time
pytest -k cache                 # or one topic
```

Work in this order, one test file at a time: `test_tracing.py`, `test_caching.py`, `test_guard.py`, then
`test_service.py` and `test_deploy_files.py`, then `test_lab.py`. Green tests prove the mechanics only. They do not
prove your capstone is good: use your own eval set for that.

Then wire it into your capstone: copy `ops/` into your repo, call your model through `Tracer.call(...)`, build your
requests with `build_request(...)`, fence every document or tool result with `wrap_untrusted(...)`, and send every
tool call through `run_tool_call(...)`. Point `deploy/app.py` at your agent. Run your own 20+ case eval before and
after each change.

## Acceptance criteria (from `readings/week4/build.md`)

Builder track. Tick each one with evidence you can show.

- [ ] **The agent**: a repo with the agent, its tools, an eval script and a README. Runs live on a real input.
- [ ] **Operate it**: tracing gives cost per task and median latency from your own runs (`python -m ops.summary traces.jsonl`). Prices are labelled as examples or checked (`VERIFY`).
- [ ] **Caching**: the stable part of your prompt comes first, nothing that changes every call sits before it, and you can show cache reads going up on repeat calls (if your model and prompt are long enough to cache; VERIFY the minimum).
- [ ] **Secure it**: an injection test and a fix, in code and a test, with the before and after kept (`lab/attacks.json`, `lab/run_attacks.py`, a test in your repo).
- [ ] **Evals**: 20+ real cases including 3+ to refuse or escalate, with this week's results; one change measured before and after.
- [ ] **Ship it**: deployed, or ready to deploy: Dockerfile, a `/health` check, secrets only in environment variables.
- [ ] **Rules for both tracks**: drafts only for anything outbound, read-only by default, no secrets in any file, data you are allowed to use.
- [ ] `pytest` is green in this starter, and you can explain what each test is checking.

You are graded on the capstone rubric (`modules/12-capstone-role-agent/rubric.md`): six criteria scored 0 to 3. To pass
you need solid (2) or above on Role fit, Correctness, Evals and Safety. A secret found in your submission makes Safety
missing: rotate it straight away.

## Builder or Operator?

- **Builder (code)**: everything above. This starter is for you.
- **Operator (Claude workspace, no code)**: you do not need `ops/`, `deploy/` or `pytest`. You do the same jobs without code:
  run your workspace on 5 real tasks and note the time and the usage it shows (tracing and cost); attack a partner with
  `lab/redteam_worksheet.md` and write down the instruction or approval step that fixed it (security); list your approval
  steps and show the result from your real workspace (ship it); keep an eval sheet with grades. Use `lab/attacks.json`
  as a list of ideas to type in by hand. Minutes saved must come from your own before and after runs.

## Demo-day checklist (Fri 4 Dec, 10 minutes: 5 live, 2 evals, 3 questions)

Final build due Friday at [time], before demo day (your trainer confirms the time in Discord). Backup recording made on
Thursday after Session 2.

- [ ] The user and the problem in two sentences.
- [ ] The agent working on a real input, live. A recorded backup is ready: if the live demo fails, play it, say so, then try live again.
- [ ] Your eval numbers, and one thing they made you change.
- [ ] Cost per request (or minutes saved from your own runs), with the trace lines that show it.
- [ ] One injection you tried and how you stopped it (before and after).
- [ ] Ready for: why this design and not a simpler one; what it cannot do.
- [ ] Rehearsed against the clock at least once. It fits in 10 minutes.
- [ ] No API key, secret or private data on screen, in files, in the recording or in your note.
- [ ] The 5-line lab note submitted: cost per request, median latency, the injection you tried, the fix, the fine-tune decision (one line with a number from your evals).

## Rules

- Never commit a key. Keys and tokens live in environment variables only. The tests scan for common key shapes.
- Prices in `ops/tracing.py` are **examples**. Check the current pricing page and change them before you show a cost as fact.
- **Humans deploy.** Nothing here deploys for you. You press the button, and you can roll back. Orgo steps are unverified (`VERIFY`): ask your trainer before relying on them.
- Test attacks use fake recipients and fake tools. Never send anything real while red-teaming.
- Stuck? Post in Discord what you tried and what you saw (no keys, no private data).
