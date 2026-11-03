# Live demos

One runnable demo per demo slide. Python 3.11+, then from this folder:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...      # never commit it
export DEMO_MODEL=claude-opus-5-5 # optional: the model the cohort uses
```

| Week | Run (from this folder) | What it shows |
|---|---|---|
| Kickoff | `python kickoff/hello_llm.py "Explain tokens in one line."` | Streaming, stop_reason, token usage |
| Kickoff (Operator) | follow `kickoff/hello-role-agent/DEMO.md` | Role + a drafts-only guardrail in one `CLAUDE.md` |
| 1 | `python week1/tokens_and_cost.py` | Token counts and a cost estimate for different inputs |
| 1 | `python week1/prompting_examples.py` | Weak vs strong prompt, system prompt, few-shot, JSON schema output |
| 1 | `python week1/stream_chat.py` (`--script` for a hands-free run) | Multi-turn memory, structured summary, `/tokens`, max_tokens cut-off |
| 1 | `python week1/retries_and_errors.py` | SDK retries, rate limits, which errors to retry and which to fix |
| 2 | `python week2/support_agent.py --yes "Where is ORD-1002? It arrived broken, can I get a refund?"` (`--no` to refuse) | The agent loop, 3 tools, validation, a human approval gate |
| 2 | `python week2/tool_design.py` (`--errors`) | Vague vs precise tool descriptions; errors returned as tool results |
| 2 | `python week2/agent_vs_workflow.py` | The same job as a fixed workflow and as an agent: when each wins |
| 2 | `python week2/verify_gate.py` (`--skip-verify`) | Verify step: a test command decides "Done", not the agent (red on purpose with `--skip-verify`) |
| 2 | `python week2/mcp_client.py` (starts `mcp_server.py`; no key needed) | The same support tools served over MCP: list tools, call them, errors. Add to Claude Code: `claude mcp add support -- python3 week2/mcp_server.py` |
| 3 | `python week3/chunking.py` | Three chunking strategies and their recall |
| 3 | `python week3/rag_eval.py`, then `--ask "How fast must I report a stolen laptop?"` | recall@k, keyword misses on paraphrases, cited answers, "I don't know" |
| 3 | `python week3/local_embeddings.py` (`EMBED_BACKEND=tfidf` to skip the model) | Private, on-machine embeddings vs TF-IDF on the same eval set |
| 3 | `python week3/evals.py` | Code-graded + model-graded checks; compare two prompt versions |
| 4 | `python week4/tracing_cost.py` (`--per-day 2000`) | One trace line per call: latency, tokens, cost; monthly projection |
| 4 | `python week4/caching_demo.py`, then `--break` | Cache writes then reads; a timestamp in the system prompt breaks it |
| 4 | `python week4/injection_redteam.py` (`--no-guardrails`) | A prompt injection in a document, and the guardrails that stop it |
| 4 | `week4/deploy/` (see its README) | A tiny agent service with /health and /ask, ready for Railway / Fly.io / Orgo |

**Offline mode.** Every demo also runs with no API key or no Wi-Fi: `DEMO_OFFLINE=1` (or simply no key) replays
canned model replies through `offline.py` and prints a banner saying so. Use it as a stage fallback; it shows the
mechanics, not a real model. To run a whole week in teaching order: `../present/demo.sh N`.

## Status

- Checked here without an API key: every script compiles; the Week 3 eval runs (keyword retrieval:
  recall@1 85%, misses the two paraphrase questions); the Week 2 agent loop passes a scripted fake-client test
  (parallel tool results in one message, validation errors, the approval gate).
- VERIFY before teaching: run each demo once with your API key. Model output, cache token counts and the exact
  minimum cacheable prompt length depend on the model.
- All data is made up (`week2` orders and help docs, `week3/docs/handbook.md`).
