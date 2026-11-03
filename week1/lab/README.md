# Week 1 lab: your first API app (Builder)

The lab uses the course demos, not this starter, so there is no code to write here. Full instructions with the
reasons: `readings/week1/lab.md`. The exact commands, from the root of the course repo:

```bash
cd demos
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...                   # in your shell only

# Step 1: setup check
python kickoff/hello_llm.py "Explain tokens in one line."
# no key? canned replies, same mechanics:
DEMO_OFFLINE=1 python week1/stream_chat.py --script

# Step 2: read and run the chat; try 4 turns, then /tokens, then /summary
python week1/stream_chat.py

# Step 3: break it on purpose (edit week1/stream_chat.py in your own copy)
#   /short <question>                          -> what is stop_reason?
#   comment out the history.append(assistant)  -> what does the model forget?
#   max_tokens=5 in summary()                  -> what happens to the JSON?

# Step 5: the five-pass prompt comparison (replace the ticket with your own text)
python week1/prompting_examples.py

# Step 6 (Thursday, after session 2): prompt iteration against an eval set
DEMO_OFFLINE=1 python week1/prompt_lab.py      # the table first (canned replies)
cp week1/prompts/v3.txt week1/prompts/v5.txt   # never edit old versions; make ONE change in v5.txt
python week1/prompt_lab.py --versions v3,v5    # needs your key for real scores
```

Step 4 (change something) is an edit to your own copy of `demos/week1/stream_chat.py`: a different system prompt, a
new field in `SUMMARY_SCHEMA`, or the cost per turn (use `week1/tokens_and_cost.py` as a guide). Step 6e adds two
tickets of your own to the `EVAL` list in `week1/prompt_lab.py`.

Keep lab notes (what you saw and why) and hand them in with the build. When you start the build, the code you
write goes in this starter's `assistant/` folder.
