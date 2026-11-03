# Week 4 activities

*Your week at a glance · about 12 hours · both tracks*

Tue 1 Dec to Fri 4 Dec 2026. **Two 60-minute live teaching sessions: Session 1 on Tuesday and Session 2 on Thursday.
Friday is demo day, a separate showcase day (60 minutes).** In between you do the lab, your build, and Discord Q&A.
Clock times are [time] until your trainer posts them in Discord.

## Where things are taught

| What | Where it is |
|---|---|
| Tracing and cost, caching, security and prompt injection | Session 1 (Tue, live) |
| The partner red-team | Lab part 2: Tue after the session to Wed, in pairs, async on Discord |
| Deploying (Railway, Fly.io, Orgo) | Session 2 (Thu, live). Read reading 4 first |
| The fine-tune decision | Session 2 (Thu, live). Read reading 5 first. Then one line in lab part 4 |
| The demo-day brief and how to rehearse | Session 2 (Thu, live) |

## Day by day

| Day | Activity | Time | Track | Output / what you hand in |
|---|---|---|---|---|
| Before Tue | Read readings 1, 2 and 3 (tracing and cost, caching and latency, security and injection) | about 65 min | Both | Notes, and a question for Discord if something is unclear |
| Tue 1 Dec | **Session 1** (live): tracing and cost, caching, security and prompt injection, then the lab brief | [time], 60 min | Both | The lab brief in hand, and a swap time agreed with your partner |
| Tue 1 Dec | **Lab part 1 · Trace and price it**: one JSON line per model call, 10 realistic inputs | about 30 min, then 90 min on your capstone | Builder: start from `demos/week4/tracing_cost.py`. Operator: run your workspace on 5 real tasks and note time and usage shown | Cost per request, median latency, slowest case |
| Tue 1 Dec to Wed 2 Dec | **Lab part 2 · Red-team in pairs**, async on Discord: swap capstones, attack only through the inputs, post what you tried | about 30 min | Both | A list of attempts: what you tried, what happened, whether it worked |
| Wed 2 Dec | Lab part 3: fix what worked against you, rerun the same attack | about 20 min | Builder: a guardrail in code and a test. Operator: the instruction or approval step that fixed it | Before and after of one injection |
| Wed 2 Dec | Get your capstone **ready to ship**; run and fix your eval set (20+ cases, 3+ to refuse or escalate) | about 135 min | Builder: Dockerfile, health check, secrets in env vars (Thursday shows the path). Operator: the result shown from your real workspace, approval steps listed | A build you can run live, and your latest eval numbers |
| Wed 2 Dec or Thu 3 Dec, before the session | Read readings 4 and 5 (deploying; fine-tune or not) | about 35 min | Both | Notes |
| Thu 3 Dec | **Session 2** (live): deploy, the fine-tune decision, the demo-day brief and how to rehearse | [time], 60 min | Both | The deploy path, a fine-tune call for your capstone, and the Friday checklist |
| Thu 3 Dec | Lab part 4: write your one-line fine-tune decision | about 10 min | Both | One line with a number from your evals |
| Thu 3 Dec | Week 4 quiz (closed book, plain answers), after Session 2 because it covers deploy and fine-tuning | 15 min | Both | Your answers, in your own words |
| Thu 3 Dec | **Demo rehearsal**: run your full demo against the clock (10 minutes: 5 live, 2 evals, 3 questions), with a partner or in front of a mirror, then fix what dragged | about 45 min | Both | A demo that fits the slot, with the cost line and injection story ready |
| Thu 3 Dec | **Backup recording**: record your demo working on a real input, after the session | about 30 min | Both | A short video you can play if the live demo fails |
| Thu 3 Dec | **Office hour (optional)**: a stuck demo or a build problem | [time], 15 min | Both | Nothing to hand in. Skip it if you are on track. |
| Fri 4 Dec | Final check and 5 lines for the lab note, then **final build due** at [time] before demo day | about 30 min | Both | Your final build and the short note (see checklist) |
| Fri 4 Dec | **Demo day** (live, 60 min, showcase day): opening and guests 10 min, four slots of 10 minutes, close 10 min. Your slot: 5 min live demo, 2 min evals, 3 min questions | [time], 60 min | Both | Your live demo, eval results and cost or minutes saved |
| Any time | Discord Q&A | | Both | Questions in writing, so everyone can see the answer |

About 12 hours in total: before Tuesday about 65 min of readings, Tuesday about 3 h (session and lab part 1), Wednesday
about 3.5 h, Thursday about 3 h (readings 4 and 5, the session, rehearsal and recording; plus the optional 15 min),
Friday about 90 min.

## Checklist

- [ ] Before Tue 1 Dec: readings 1, 2, 3 done before Session 1.
- [ ] Tue 1 Dec: swap time agreed with your red-team partner on Discord.
- [ ] Tue 1 Dec: you can say "one request costs about X and takes about Y seconds" and point to the lines that show it.
- [ ] Before Thu 3 Dec: readings 4 and 5 done.
- [ ] Tue to Wed: one injection tried against a partner's capstone, one against yours, and the fix with a before and after.
- [ ] Wed 2 Dec: eval set of 20+ real cases, including 3+ to refuse or escalate, with results from this week.
- [ ] Wed 2 Dec: Builder: Dockerfile, health check, secrets in env vars (or deployed). Operator: result shown from your real workspace, approval steps listed.
- [ ] Thu 3 Dec: fine-tune decision written in one line, with a number from your evals.
- [ ] Thu 3 Dec: Week 4 quiz done, after Session 2.
- [ ] Thu 3 Dec: demo rehearsed against the clock at least once, and it fits in 10 minutes.
- [ ] Thu 3 Dec: backup recording saved where you can open it on demo day.
- [ ] **Fri 4 Dec: final build due [time], before demo day** (VERIFY the time; your trainer will confirm it in Discord). This is your final capstone build. Submit: [where to submit].
- [ ] Fri 4 Dec: lab note submitted (5 lines is fine): cost per request, median latency, the injection you tried, the fix, the fine-tune decision. Submit: [where to submit].
- [ ] Fri 4 Dec: present at demo day.
- [ ] No API keys, secrets or private data in any file, recording or note. Drafts only for anything that leaves your hands.

## Capstone milestone: demo day

Friday is the capstone milestone and the showcase day. Each slot is **10 minutes** (5 live, 2 evals, 3 questions; a visible timer cuts at 10:00): a live demo of your agent on a real input, your
**eval results** (your numbers and one thing they made you change), your **cost per request or minutes saved**, one
injection you tried and how you stopped it, then questions. Minutes saved must come from your own before and after
runs. Have your backup recording ready, play it if the live demo fails, say so, then try live again. You are graded on
the capstone rubric (six criteria, 0 to 3); the levels are in `build.md`.

## Optional stretch: deploy it

Not required this week. Thursday's Session 2 shows the path (read reading 4 first). If you want to go further, put your container on a platform your trainer showed (Railway or Fly.io),
check `/health`, read the logs, and practise a rollback. You press deploy yourself. Operator track: ask your trainer
before trying anything beyond your workspace.

## If you're stuck

1. Re-run the offline demo for the part you are on (`DEMO_OFFLINE=1`): no key or Wi-Fi needed.
2. Post in Discord what you tried and what you saw (no keys, no private data). Written questions help everyone.
3. Bring it to Thursday's Session 2, or the optional office hour after it. If a part will not work by Friday, show what does work and say what does not.

## After the bootcamp

Keep the habits that ship: eval before you change, keep it simple, stay current. Next steps: [alumni channel].
