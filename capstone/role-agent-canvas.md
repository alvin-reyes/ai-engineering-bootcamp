# Role agent canvas

Fill this in by the end of week 2. It becomes your capstone pitch: your agent persona, written as a role
contract (Role · Context · Tools · Guardrails · Verify).

**Name / handle:**  **Role:**  **Track:** Builder / Operator

## 01 ROLE: one job, one definition of done

### Role map

List 10–20 tasks you repeat. Be specific ("write the Monday status for leadership", not "reporting").

| Task | How often | Minutes per run | Pain (1–3) |
|---|---|---|---|
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |

### Pick one job

Score your top 3 candidates from 1 (poor) to 3 (good).

| Candidate | Frequent | Clear inputs and outputs | Easy to check | Mistakes are cheap | Total |
|---|---|---|---|---|---|
| &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; | &nbsp; |

**My job:**
**Why not the others (one line each):**

### Job spec

| | |
|---|---|
| Trigger: what starts it | |
| Inputs: what it reads, and where from | |
| Steps: what a good colleague would do | |
| Output: exactly what it produces, in what format | |
| Done means: how you tell a good output from a bad one | |
| Reviewer: who checks it before it is used | |

## 02 CONTEXT: load what it needs, hide what it doesn't

| Needs | Builder track | Operator track |
|---|---|---|
| Instructions | system prompt | `CLAUDE.md` + skill |
| Knowledge (documents, examples, style guides) | | |
| What it must NOT see | | |

## 03 TOOLS: least privilege, read-only by default

| Tool or app | Read or write | Why it needs it | Approval needed? |
|---|---|---|---|
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |

## 04 GUARDRAILS: the workflow gates every next step

- [ ] Outbound actions are drafts I send
- [ ] Read-only until a write is needed, and then it needs my approval
- [ ] No secrets in instructions or files
- [ ] The data I use is allowed by my employer (or is redacted)
- [ ] What it should refuse or hand back to me:

## 05 VERIFY: no proof, no handoff

- Who or what grades the output before I see it (eval script, checker subagent):

- Eval cases I can collect (where from, how many):
- What a passing output must have:
- Minutes per run today: ___ × runs per week: ___ = ___ minutes per week
