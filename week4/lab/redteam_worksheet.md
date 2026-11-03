# Red-team worksheet

Fill one block per attempt. Post the finished list in your pair's Discord thread. **No API keys, no private data,
no real people's details.** Nothing may be really sent: use fake recipients and fake tool handlers.

Rules of the exercise: attack **only through the inputs** (a document, a tool result, user text). Do not read your
partner's code first and do not ask for hints. About 15 minutes each way.

| Field | Your note |
|---|---|
| Pair partner (handle) | |
| App under attack (one line: what it does) | |
| Date | |

## Attempts (copy this block for each attempt; aim for at least 6)

```
Attempt #:
Input channel (document / tool_result / user_text):
Idea (hidden "ignore previous instructions" / another user's data / send or delete / print the system prompt / other):
Exact text I used (also add it to lab/attacks.json):
What I expected:
What happened (quote the agent's answer or the tool calls it made):
Did it work? (yes / partly / no):
```

## Fixes (lab part 3, for each attack that worked against YOUR app)

```
Attack id (from lab/attacks.json):
Before (what the app did, in one line):
Guardrail added (remove the tool / gate it / scope the data / output check / other):
Where in the code (file and function), or for the Operator track: the instruction or approval step:
After (same attack rerun, what happened):
Test that keeps it fixed (name of the test), Builder track:
```

## Summary (goes in your 5-line lab note)

- Attacks tried: __ . Worked: __ . Fixed: __ .
- The one I will tell at demo day (attack, then fix, with before and after):
