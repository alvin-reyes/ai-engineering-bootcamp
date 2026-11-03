# Builder track: role agent starter

Your capstone grows out of your weekly builds: the week 1 assistant gives you the API client and streaming, week 2
gives you the tool loop, week 3 gives you retrieval and evals. Keep that code; reshape it around your job spec.

## Suggested layout

```
my-role-agent/
  README.md          # your job spec (from the canvas), how to run, results
  agent.py           # the loop: model call -> run tools -> repeat (from week 2)
  prompts.py         # system prompt: role, job, rules, output format
  tools.py           # one function + schema per tool; validate inputs; read-only first
  knowledge/         # documents the agent retrieves from (week 3); redacted if needed
  evals/
    cases.jsonl      # 20+ real past inputs with what a good output must contain
    run_evals.py     # runs every case, grades it, prints a score
  tests/             # pytest: tools, failure handling, one end-to-end case
  .env.example       # names of the variables you need; never the values
```

## Checklist

- [ ] The system prompt states the role, the one job, the output format, and what to refuse or hand back.
- [ ] Every tool has a strict schema; inputs are validated before the tool runs.
- [ ] Write actions (send, post, update) stop for your approval.
- [ ] `run_evals.py` prints a score you can compare before and after a change.
- [ ] Each run logs what it read, which tools it called, tokens used and time taken.
- [ ] No keys in the repo; `.env` is in `.gitignore`.
