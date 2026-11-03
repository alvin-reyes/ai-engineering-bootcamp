# Lab · Your first API app

*Builder about 100 minutes (six steps), Operator about 70 (four steps) · Tuesday after session 1 to Thursday, on your own · everyone (two tracks)*

Do this after session 1 (Tuesday), at your own pace: steps 1 to 3 on Tuesday, steps 4 and 5 on Wednesday, and step 6 on Thursday after session 2, which shows the prompt lab. Hand in your lab notes with the build (Friday, before the showcase); post questions in Discord. Bring what broke to session 2. It also covers what is not taught live: see the readings.

## Builder track

1. **Setup (10 min).** `cd demos`, create the venv, `pip install -r requirements.txt`, set `ANTHROPIC_API_KEY` in your
   shell. Check:
   ```bash
   python kickoff/hello_llm.py "Explain tokens in one line."
   ```
   No key? Use `DEMO_OFFLINE=1 python week1/stream_chat.py --script`.
2. **Read and run the chat (15 min).**
   ```bash
   python week1/stream_chat.py
   ```
   Chat for four turns, then `/tokens`, then `/summary`. Write down: how did the token count change each turn?
3. **Break it on purpose (15 min).** Try each, and write what you see and why:
   - `/short <any question>`: what is `stop_reason`?
   - Comment out the line that appends the assistant reply to `history`. What does the model forget?
   - Change `max_tokens` to 5 in `summary()`. What happens to the JSON?
4. **Change something (20 min).** Pick one: a different system prompt; add a field to `SUMMARY_SCHEMA`; print the cost
   of each turn using `tokens_and_cost.py` as a guide.
5. **Run the comparison (10 min).**
   ```bash
   python week1/prompting_examples.py
   ```
   Replace the ticket with your own text. Which of the five passes helped most?
6. **Prompt iteration against an eval set (30 min).** Prompts are code: change one thing, measure.
   ```bash
   DEMO_OFFLINE=1 python week1/prompt_lab.py      # see the table first (canned replies)
   python week1/prompt_lab.py                     # with your key: your real scores
   ```
   a. Read `week1/prompts/v1.txt` to `v4.txt` and `CHANGELOG.md`. Copy `v3.txt` to `v5.txt` (never edit the old versions).
   b. Make **one** change in `v5.txt` with a reason (a clearer rule, a better example, a rule with its why). Add a line to your own changelog.
   c. Run `python week1/prompt_lab.py --versions v3,v5` (the script loads any `prompts/vN.txt`; offline, a new version just repeats v3's canned replies, so the real comparison needs your key).
   d. Write down the score of each version and which tickets flipped. Keep the change only if the score or the flipped cases improved.
   e. Add **two tickets of your own** to the `EVAL` list (one tricky, one that tries to give an instruction). Check your examples in the prompt are not in `EVAL`.
   Write three lines: what you changed, the score before and after, and why eight tickets is not enough.

## Operator track

Suggested split: step 1 on Tuesday, step 2 on Wednesday, steps 3 and 4 on Thursday after session 2.

1. **Workspace (20 min).** Open your Claude workspace. Create a project or folder for your role with a `CLAUDE.md`
   that says who you are, what you do, and what the agent may never do (send anything without your approval).
2. **Prompt ladder (25 min).** Take a real piece of work text (private details removed). Run the five passes from
   lesson 2: weak, goal+context+format, a system-style instruction in `CLAUDE.md`, two examples, a fixed output
   format. Save all five prompts and replies.
3. **Eval by hand (15 min).** Write 8 real (redacted) cases for your task with the answer you expect for each. Run your best prompt on all 8
   and mark each right or wrong. Change one thing and run all 8 again. Which cases flipped?
4. **Notes (10 min).** Write three lines: which pass helped most, what the weak prompt got wrong, and one thing you
   will always put in the instructions from now on.

## Everyone

- Post one question you still have in the channel.
- Keep your key and any private text out of anything you share.
