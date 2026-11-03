# Final build and demo day

*10 minutes to read · everyone · this is what you are graded on*

## The final build

Your capstone agent, for your own role, in a state you can run live. This week's additions are the "operate it"
and "secure it" layers.

| | Builder track | Operator track |
|---|---|---|
| The agent | Repo: agent, tools, eval script, README | Workspace folder: `CLAUDE.md`, skills, subagents, eval sheet, short write-up |
| Operate it | Tracing with cost per task and latency; prices labelled as examples or checked | Time saved per run from your own before and after runs; approval steps listed |
| Secure it | Injection test and a fix (code and a test) | Injection test notes and the instruction or approval step that fixed it |
| Evals | 20+ real cases incl. 3+ to refuse or escalate; one change measured before and after | Eval sheet with grades; same minimums |
| Ship it | Deployed (or ready with a Dockerfile, health check, secrets in env vars) | Result shown from the real workspace |

Rules for both: drafts only for outbound, read-only by default, no secrets in files, data you are allowed to use.

## Demo day

- Date and place: Fri 4 Dec, showcase day, [time, link].
- Final build due Friday at [time], before demo day. Your backup recording is made on Thursday, after Session 2.
- One after another, strict time. Presentation order: [order set by your trainer].
- Each slot is **10 minutes**: 5 minutes live demo, 2 minutes of evals, 3 minutes of questions. A visible timer cuts at 10:00. Demo day is Friday, 60 minutes: 10 to open, four slots, 10 to close.

### What to show

1. **The user and the problem** in two sentences.
2. **The agent working on a real input**, live. Have a recorded backup in case the live demo fails, then try live anyway.
3. **Your evals:** your numbers, and one thing they made you change.
4. **Cost and safety:** cost per request (or time saved), and one injection you tried and how you stopped it.
5. **Be ready for:** why this design and not a simpler one; what it cannot do.

## How it is graded

The capstone rubric, scored 0 to 3 on six criteria: missing (0), partial (1), solid (2), excellent (3).

| Criterion | Solid (2) means |
|---|---|
| Role fit | One recurring task from your real role, clearly scoped; time saved from your own runs |
| Correctness | Works live on real or realistic redacted inputs; failures handled without crashing or inventing |
| Design | The simplest design that fits; clear instructions and tools |
| Evals | 20+ real cases incl. 3+ to refuse or escalate; results reported |
| Safety | Outbound is draft-only; read-only by default; no secrets in files |
| Explanation | You explain why this job, why this design, what it cannot do |

To pass you need **solid or above on Role fit, Correctness, Evals and Safety**, no criterion missing, and every weekly
build at solid or above. A time-saved number with no runs behind it caps Role fit at partial. A secret found in your
submission makes Safety missing: rotate it straight away.
Full rubric with Builder and Operator evidence: `modules/12-capstone-role-agent/rubric.md`.
