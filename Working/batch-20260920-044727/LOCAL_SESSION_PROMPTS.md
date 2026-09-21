# What to paste into the local Claude Code session

Two messages. Send the first, do the sign-in it stops for, then send the second.

## Message 1 — verify the folder, update it, and open the browser for sign-in

> First, before anything else, tell me plainly: what is your current working directory, and are
> you running on my local Windows machine or in a cloud container? Print the absolute path.
> Then confirm these three folders exist and list their files:
> Workspace\output\groundwater-abstraction-return-reconciliation,
> Workspace\output\sparse-probe-roundness-conformance-adjudication,
> Workspace\output\rail-corridor-incident-and-dispatch-ledger-recovery.
>
> If you are NOT on my local machine, or those folders are missing, stop and tell me. Do not
> continue.
>
> If everything checks out: run `git pull origin claude/wonderful-bohr-b7u814` to pick up the
> latest browser configuration, run `.\validate-portable.ps1` and report the result, then read
> `Working\batch-20260920-044727\HANDOFF_FOR_UPLOAD.md` and
> `eris_automation\State\controller.json` so you know the batch state.
>
> Then open the Playwright MCP browser, visible, and navigate to
> https://shipd.ai/quests/eris/datasets/jd71ktmw09xmcbpd8k2rwqc4v18efhft
> It will be signed out, because the browser now uses its own profile at
> Working\browser-profile-shipd. Stop there and tell me to sign in. Do not attempt to sign in
> yourself, and do not edit anything on Shipd yet.

You will see two approval prompts the first time: one to trust the project's MCP browser server,
and possibly one for the pull. Approve both.

When the browser window appears, sign in with the account that should own these uploads. That
profile is separate from your everyday browser and from any other account, and it is git-ignored,
so it stays on your machine.

## Message 2 — run the uploads (send only after you are signed in)

> I am now signed in with the correct account. Proceed with Status & Fix for batch
> batch-20260920-044727. It has three bound slots and three verified local packages under
> Workspace\output\, built in an earlier session; the ledger under eris_automation\State is
> authoritative and nothing has been written to Shipd yet.
>
> Take the slots in order. For each one, open its exact dataset and challenge URLs in separate
> tabs and verify the IDs before any write. Then run the submission-pool workflow from that
> slot's package: upload the listed source files, rebuild, set the licence and canonical source
> URL, clear every red and yellow finding genuinely, and Mark as Ready. Then fill the challenge
> form from CHALLENGE_FORM_FILL.md, paste PASTE_THIS_PREPARE.txt and PASTE_THIS_GRADE.txt, run
> Prepare, and run the full check suite until everything is green.
>
> Stop each slot with all checks green and Run Agents visibly available. Do not click Run Agents.
> Update SUBMISSION_POOL_STATE.json and the controller after each phase, and tell me if any
> check fails so I can see what you changed.

Add the words `through Run Agents` to message 2 only if you also want the challenges launched.

## If message 1 says it is in a cloud container

Then that session is not on your local folder, and it cannot reach your files or your browser.
Close it and open the local bot folder directly in the Claude Code desktop app for Windows, then
send message 1 again.
