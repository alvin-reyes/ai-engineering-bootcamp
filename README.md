# AI Engineering Bootcamp · starter code

AR Data · instructor: Alvin Reyes · ardata.tech

Everything you run or build during the bootcamp. Four weeks after an onboarding week; live sessions on
Tuesday and Thursday, your build shown at the Friday showcase. Your capstone: an AI agent for your own role.

## Set up once

```bash
git clone <this repo> && cd ai-engineering-bootcamp
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...      # from your environment, never in a file you commit
```

No key yet, or no Wi-Fi? Every demo runs offline with canned replies: `DEMO_OFFLINE=1 python demos/week1/...`.

## Each week

| Week | Folder |
|---|---|
| 0 · Onboarding | [`week0/`](week0/README.md) |
| 1 · LLM Foundations | [`week1/`](week1/README.md) |
| 2 · Tools & Agents | [`week2/`](week2/README.md) |
| 3 · RAG & Evals | [`week3/`](week3/README.md) |
| 4 · Ship It | [`week4/`](week4/README.md) |

Inside each week:

- `README.md`: your week at a glance (what to do each day, how long, what to hand in, when).
- `lab/`: the lab steps (`LAB.md`) and any files you edit during the lab.
- `BRIEF.md` (what to build and how it is graded) and `BUILD.md` (how to work on the starter code).
- The starter code, with `# TODO:` markers. Run `pytest` inside the week's folder: the acceptance tests fail
  until you build it, and pass when you are done.

`demos/` holds every live demo from the sessions; `capstone/` the canvas, rubric, track guide and templates.

## Rules that apply to every build

- Keys and secrets only in environment variables. Never commit them.
- Read-only tools by default; anything that sends, writes or pays waits for a human "yes".
- Use AI coding tools freely, and be ready to explain every line you hand in.
