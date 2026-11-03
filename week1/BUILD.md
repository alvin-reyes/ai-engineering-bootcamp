# Week 1 build starter: a streaming CLI assistant

This is the starting point for the **Builder** weekly build (due Friday, before the showcase). You fill in the
`# TODO:` markers; the tests tell you when each part works. The code you hand in must be code you can explain.

## What you build

A terminal chat app on an LLM API that:

1. streams replies token by token,
2. keeps multi-turn history (the API remembers nothing, so you send it all every turn),
3. answers `/summary` with JSON that is valid against a schema,
4. handles a cut-off reply (`stop_reason` is `max_tokens`) and API errors cleanly,
5. reads the key from the environment and never puts it in the repo,
6. has tests, including one failure case.

## Acceptance criteria and where they live

| Criterion | Where | Tests |
|---|---|---|
| Streams token by token | `Assistant.ask` in `assistant/core.py` | `test_streams_chunk_by_chunk` |
| Keeps multi-turn history | `Assistant.ask` | `test_history_is_resent_every_turn` |
| `/summary` is valid JSON for the schema | `Assistant.summary`, `validate_summary` | `test_summary_*`, `test_validate_summary` |
| Cut-off reply handled | `Assistant.ask`, `Assistant.summary` | `test_cut_off_*` |
| API errors handled cleanly | `describe_error`, `ask`, `summary`, `handle` in `assistant/cli.py` | `test_api_errors_*`, `test_handle_never_crashes_*` |
| Key from the environment only | `get_api_key` | `test_key_from_environment`, `test_missing_key_*`, `test_no_key_in_the_repo` |
| Three tests, one a failure case | `tests/` | The provided tests are the contract; add three of your own in `tests/test_mine.py` (one must be a failure case) |

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate     # Python 3.11 or newer
pip install -r requirements.txt
python -m pytest -q                                    # no API key needed
export ANTHROPIC_API_KEY=...                           # in your shell, never in a file in this repo
python -m assistant                                    # the chat
```

At the start nearly every test fails with `NotImplementedError`. That is the plan: pick one TODO, make its tests
pass, repeat. A good order: `get_api_key`, `describe_error`, `validate_summary`, `Assistant.ask`,
`Assistant.summary`, `handle`.

## How the tests work without a key

`tests/conftest.py` ships a small fake client with the same shape as `anthropic.Anthropic()` for the calls you use
(`messages.stream` and `messages.create`). `Assistant` takes the client as an argument, so the tests hand it the fake
and script what the "model" says. Read `conftest.py` first: you will use the same idea for your own tests
(`fake.say("text")`, `fake.say("...", stop="max_tokens")`, `fake.fail(api_error("rate_limit"))`).
The demo `demos/offline.py` in the course repo does the same job for the live demos.

## Layout

```
assistant/core.py   Assistant, SUMMARY_SCHEMA, describe_error, validate_summary, get_api_key   (TODOs)
assistant/cli.py    handle(), main()                                                           (handle is a TODO)
tests/              conftest.py (fake client) and test_assistant.py (the acceptance tests)
lab/README.md       the lab commands
```

Do not change function names or signatures: the tests call them. You can add helpers and files.

## Builder vs Operator

This starter is for the **Builder** track (code). The **Operator** track does a different weekly build (your first
role setup: workspace, role `CLAUDE.md`, one skill, three cases) and does not use this repo. If you are unsure
which track you are on, ask in the channel.

## Before you submit

- [ ] `python -m pytest -q` passes, and your own three tests (one failure case) are in `tests/test_mine.py`
- [ ] No key, token or private data in the repo (`.env` is ignored by `.gitignore`)
- [ ] You can explain every line: how you handle a `max_tokens` stop, and what is in the history on turn three
