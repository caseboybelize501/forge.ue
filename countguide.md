COUNT RECONCILIATION PROTOCOL

## Add this to every project. Bakes completeness into the gates permanently.

## Version 1.0 — triggered by the coding schedule gap discovery

-----

# THE PROBLEM IT SOLVES

Critics validate correctness. Not completeness.
A file manifest can pass every quality check and still be missing files.
The model doesn’t know what it doesn’t know.
Count reconciliation makes completeness a hard arithmetic gate, not an assumption.

-----

# WHERE TO ADD IT: END OF LAYER 1

## STEP 1: Lock the count before critic_final.md is written

After structure_confirmed.md is produced, before Phase 9 runs:

Add this block to your Phase 9 prompt:

```
BEFORE writing critic_final.md, perform COUNT LOCK:

1. Count every file listed in file_manifest.md
Record as: L1_MANIFEST_COUNT = [N]

2. Count every stub file actually created in the folder structure
Record as: L1_STRUCTURE_COUNT = [N]

3. These two numbers must match exactly.
If they do not match: STOP. Do not write critic_final.md.
Return to Phase 5 (file_manifest.md) and reconcile.

4. Write both numbers into critic_final.md as a header:
L1_MANIFEST_COUNT: [N]
L1_STRUCTURE_COUNT: [N]
STATUS: MATCH ✓

Only after STATUS: MATCH ✓ can critic_final.md say APPROVED.
```

## WHAT critic_final.md NOW LOOKS LIKE:

```
# critic_final.md
L1_MANIFEST_COUNT: 47
L1_STRUCTURE_COUNT: 47
STATUS: MATCH ✓

APPROVED.

[rest of critic notes]
```

That number — 47 — is now a hard contract.
It travels into Layer 2 as a constraint.
Nothing can override it.

-----

# WHERE TO ADD IT: LAYER 2 PHASE 5

When generating file_manifest2.md, add this explicit check:

```
BEFORE finalizing file_manifest2.md:

1. Read critic_final.md from Layer 1
Extract: L1_MANIFEST_COUNT = [N]

2. Count every file in file_manifest2.md
Record as: L2_MANIFEST_COUNT = [X]

3. L2_MANIFEST_COUNT must be >= L1_MANIFEST_COUNT
If X < N: STOP. Do not proceed to Phase 6.
Missing files = N - X minimum.
Return to Phase 3 (dependency_graph2.md) and find what was dropped.

4. Write into file_manifest2.md as a header:
L1_CONTRACT_COUNT: [N]
L2_MANIFEST_COUNT: [X]
DELTA: [X - N]
STATUS: COMPLETE ✓ (or INCOMPLETE — [N-X] files missing)
```

## WHAT file_manifest2.md NOW LOOKS LIKE:

```
# file_manifest2.md
L1_CONTRACT_COUNT: 47
L2_MANIFEST_COUNT: 52
DELTA: +5
STATUS: COMPLETE ✓
(note: 5 additional files identified during code planning — see entries marked NEW)

[full file list]
```

Delta can be positive — Layer 2 often discovers files Layer 1 didn’t know it needed.
Delta cannot be negative. Ever.

-----

# WHERE TO ADD IT: LAYER 2 PHASE 10 (CODING SCHEDULE)

Before codingschedule.md is finalized:

```
BEFORE finalizing codingschedule.md:

1. Read file_manifest2.md
Extract: L2_MANIFEST_COUNT = [X]

2. Count every file assigned a task ID in codingschedule.md
Record as: SCHEDULE_FILE_COUNT = [Y]

3. Y must equal X exactly.
If Y < X: STOP. Files exist in manifest with no scheduled task.
Find them. Assign them. Do not close the schedule until Y = X.

4. Write into codingschedule.md as a header:
L2_MANIFEST_COUNT: [X]
SCHEDULE_FILE_COUNT: [Y]
STATUS: COMPLETE ✓ (or INCOMPLETE — [X-Y] files unscheduled)
```

This is exactly where your gap occurred.
The schedule was correct but short.
This gate would have caught it before you ever started coding.

-----

# WHERE TO ADD IT: LAYER 3 EACH SESSION CRITIC

At the end of each codecriticlayer3phaseN.md:

```
RUNNING TOTALS (update at every session):
Files scheduled: [X] (from codingschedule.md header)
Files completed: [Y] (cumulative across all sessions so far)
Files remaining: [X - Y]
Sessions completed: [N]
STATUS: ON TRACK / BEHIND / COMPLETE
```

This gives you a live completion percentage at every gate.
You always know exactly where you are.
You can never accidentally think you’re done when you’re not.

-----

# THE FULL COUNT CHAIN

```
Layer 1 Phase 9 → critic_final.md
L1_MANIFEST_COUNT: 47 ← LOCKED

Layer 2 Phase 5 → file_manifest2.md
L1_CONTRACT_COUNT: 47
L2_MANIFEST_COUNT: 52 ← must be >= 47
DELTA: +5 ✓

Layer 2 Phase 10 → codingschedule.md
L2_MANIFEST_COUNT: 52
SCHEDULE_FILE_COUNT: 52 ← must equal 52
STATUS: COMPLETE ✓

Layer 3 Session N → codecriticlayer3phaseN.md
Files completed: 31/52
Files remaining: 21
STATUS: ON TRACK
```

One number flows through every layer.
It cannot be lost. It cannot be rounded down.
Completeness is now arithmetic, not assumption.

-----

# YOUR SITUATION RIGHT NOW

## You are at: End of Layer 1

### IMMEDIATE NEXT STEPS:

**Step 1: Count reconciliation on Layer 1 (do this now)**

```
Open file_manifest.md
Count every file listed → record as L1_MANIFEST_COUNT
Count every stub in your folder structure → record as L1_STRUCTURE_COUNT
If they match → add both numbers to critic_final.md
If they don't match → go back to file_manifest.md before proceeding
```

**Step 2: Write critic_final.md with count locked**

```
critic_final.md must contain:
L1_MANIFEST_COUNT: [N]
L1_STRUCTURE_COUNT: [N]
STATUS: MATCH ✓
APPROVED.
```

**Step 3: Git commit Layer 1 close**

```
git add .
git commit -m "Layer 1 COMPLETE — critic_final.md APPROVED — manifest count: [N]"
git push
```

**Step 4: Start Layer 2 Phase 1**

```
Prompt:
"Read the entire Layer 1 folder.
Your source of truth is all 9 Layer 1 MDs.
L1_MANIFEST_COUNT = [N] — this is a hard contract.
Begin Layer 2 Phase 1: produce requirements2.md
Read: entire Layer 1 folder
Job: re-derive requirements through a coding lens
Do not proceed until requirements2.md is saved and committed."
```

**Step 5: At Layer 2 Phase 5 — enforce the count**

```
file_manifest2.md must contain >= [N] files.
Write L1_CONTRACT_COUNT and L2_MANIFEST_COUNT as a header.
If L2 count < L1 count: return to dependency_graph2.md.
```

**Step 6: At Layer 2 Phase 10 — enforce the schedule count**

```
codingschedule.md must schedule every file in file_manifest2.md.
Write SCHEDULE_FILE_COUNT as a header.
If schedule count < manifest count: find the missing files before closing.
```

-----

# THE ONE ADDITION TO THE ARCHITECTURE

```
Every layer close requires:
count(files produced) = count(files planned)
This number is written into the closing critic MD.
The next layer reads this number as a hard floor.
The number can only stay the same or grow.
It can never shrink.
That is completeness as a gate.
```

-----

# UPDATED ONE RULE

The prompt is a document.
It is read exactly once.
Every layer is a phase engine applied to verified output.
Every layer close locks a file count.
Every layer open inherits that count as a hard floor.
Trust compounds. Completeness is arithmetic. Vision never drifts.
That is the exponential.