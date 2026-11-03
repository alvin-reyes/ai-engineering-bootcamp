# Prompt changelog (prompts are code)

Change a prompt only against the eval set in `../prompt_lab.py`. One change per version, a reason, a measured result.

| Version | Change | Why |
|---|---|---|
| v1 | `Triage this ticket: ...` | Baseline: the first thing anyone writes |
| v2 | Goal, label definitions, "judge by impact", reply format | The model cannot guess your labels or your format |
| v3 | System prompt (ticket = data), XML tags, 3 diverse examples with reasons | Separate instructions from data; show the pattern; resist instructions inside tickets |
| v4 | v3 plus a JSON schema (`output_config`) | Code reads the answer: make the shape certain |

Record the score next to each version in your own copy after you run it. The examples in v3 and v4 must never be
tickets from the eval set (that would be testing on the answers).
