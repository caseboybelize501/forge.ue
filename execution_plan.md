You are an autonomous execution agent.

reference the forgeue.md file and :

Your source of truth is: `forgeue.md`
Read it first. Do not proceed until you have read it.

You will execute this project in phases.
You cannot skip a phase.
You cannot write code until ALL phases are complete.
Each phase produces exactly one MD file.
If any phase output does not match forgeue.md, stop and return to Phase 1.

---

~~PHASE 1: REQUIREMENTS~~
~~Read: forgeue.md~~
~~Produce: requirements.md~~
~~Do not proceed until this file exists and is saved.~~
**✓ COMPLETE**

~~PHASE 2: ARCHITECTURE~~
~~Read: forgeue.md + requirements.md~~
~~Produce: architecture.md~~
~~Do not proceed until this file exists and is saved.~~
**✓ COMPLETE**

~~PHASE 3: DEPENDENCY GRAPH~~
~~Read: architecture.md~~
~~Produce: dependency_graph.md~~
~~Do not proceed until this file exists and is saved.~~
**✓ COMPLETE**

~~PHASE 4: MODULE DEPENDENCIES~~
~~Read: dependency_graph.md~~
~~Produce: module_dependencies.md~~
~~Do not proceed until this file exists and is saved.~~
**✓ COMPLETE**

~~PHASE 5: FILE MANIFEST~~
~~Read: module_dependencies.md~~
~~Produce: file_manifest.md~~
~~Every file that will ever exist in this project must be listed here.~~
~~Do not proceed until this file exists and is saved.~~
**✓ COMPLETE**

~~PHASE 6: CODE CRITIC (PRE-BUILD)~~
~~Read: ALL prior MDs + forgeue.md~~
~~Ask: Does this architecture fulfill the original vision?~~
~~Produce: critic_prebuild.md~~
~~Write either APPROVED or RETURN TO PHASE [N] and why.~~
~~Do not proceed until this file says APPROVED.~~
**✓ COMPLETE — APPROVED**

PHASE 7: TASK SCHEDULE
Read: file_manifest.md + critic_prebuild.md
Break every file into atomic tasks with dependencies.
Produce: task_schedule.md
Do not proceed until this file exists and is saved.

PHASE 8: FOLDER STRUCTURE
Read: file_manifest.md + task_schedule.md
Create all folders and empty stub files now.
No logic. No implementation. Stubs and docstrings only.
Produce: structure_confirmed.md
Do not proceed until this file exists and is saved.

PHASE 9: CODE CRITIC (FINAL)
Read: ALL MDs + actual folder structure
Ask: Does the structure match the manifest? Does it match forgeue.md?
Produce: critic_final.md
Write either APPROVED or RETURN TO PHASE [N] and why.
Do not proceed until this file exists and is saved.

---

ONLY after critic_final.md says APPROVED:
Begin sequential code generation.
One file at a time.
After each file, check against forgeue.md.
If drift is detected, stop. Do not patch forward.
Return to the phase where drift originated.
Regenerate from there.

The vision is in forgeue.md.
It does not change.
You execute against it. Always.
