---
name: weekly-status-draft
description: Draft the weekly operations status update for leadership from this week's tickets and notes. Use when I say "draft the status", "weekly update", or "/weekly-status-draft".
---

# Weekly status draft

Inputs: this week's closed and open tickets from [ticket tool], my notes in `notes/` from the last 7 days, and last
week's status in `drafts/` (for continuity).

1. Read last week's status. Note anything marked "at risk" or "next week".
2. Read this week's tickets and notes. Group them into: shipped, in progress, at risk, blocked.
3. For each "at risk" or "blocked" item, say why and what would unblock it.
4. Write `drafts/<date>-status.md` in the format of `knowledge/status-template.md`: at most 10 bullets, plain words,
   each bullet ending with its source (ticket id or note file).
5. Ask the `status-checker` subagent to check the draft. Apply its fixes.
6. Tell me the file path, anything you could not find, and the one item leadership most needs to act on.

Never send the update. I review and send it myself.
