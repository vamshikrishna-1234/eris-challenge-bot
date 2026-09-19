# Cross-Computer Coordination

## One Skill, Shared Files, Separate Challenge Ownership

Install the same `eris-challenge-factory` skill once on every computer. Do not install one skill per challenge or embed skills inside tasks.

Synchronize these shared assets through a private Git repository, OneDrive, or another conflict-aware mechanism:

- live `rules` and checkpoints;
- `prev_reviews.txt`;
- idea inventories;
- accepted examples or their index;
- `challenge_registry` status files;
- completed challenge folders when both computers need them for duplicate audits.

Chats are not the source of truth. Persist every approved idea, source decision, blocker, reviewer lesson, and task ID in files.

## Ownership Protocol

- One status JSON per challenge.
- One owner machine and one owner task per challenge folder.
- Use statuses: `idea`, `claimed`, `researching`, `building`, `blocked`, `ready_for_review`, `submitted`, `accepted`, `rejected`, `abandoned`.
- A second computer may review read-only. Transfer ownership explicitly before it edits the challenge.
- Independent challenges should use different folders and different status files.

## Sync Protocol

1. Sync before scouting or claiming.
2. Claim and sync immediately.
3. Sync after source verification, initial build, reviewer revision, and final audit.
4. Sync before and after appending `prev_reviews.txt`.
5. Resolve conflicts by preserving both reviewer entries and the newest valid rule; never discard another machine's work blindly.

## Recommended Division

- Computer A: idea scouting, duplicate audits, dataset/license research, and task creation.
- Computer B: challenge implementation, data preparation, grader work, and baseline runs.
- Either computer: final independent review, provided it does not edit the folder while the owner is actively changing it.

This division is optional. The ownership rule is mandatory.
