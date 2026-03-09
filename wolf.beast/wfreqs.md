# WOLVERINE: UNBOUNDED — Workflow Frequencies

## GOVERNANCE
**Parent Document:** critic_final.md (Layer 1 Phase 9)
**Status:** READ-ONLY — Layer 1 frozen. Modifications require return to source phase.
**Layer:** L1 | **Phase:** P1

## SUMMARY
Development rhythm and iteration frequencies for FORGE pipeline execution on the Wolverine project.

---

## LAYER 1 FREQUENCIES (Architecture Planning)

| Phase | Agent | Estimated Time | Git Commit Required |
|-------|-------|----------------|---------------------|
| Phase 1: requirements.md | architect_agent | 45 min | ✅ |
| Phase 2: architecture.md | architect_agent | 90 min | ✅ |
| Phase 3: dependency_graph.md | architect_agent | 60 min | ✅ |
| Phase 4: module_dependencies.md | architect_agent | 45 min | ✅ |
| Phase 5: file_manifest.md | architect_agent | 60 min | ✅ |
| Phase 6: critic_prebuild.md | critic_agent | 75 min | ✅ |
| Phase 7: task_schedule.md | architect_agent | 45 min | ✅ |
| Phase 8: structure_confirmed.md | architect_agent + CLI | 60 min | ✅ |
| Phase 9: critic_final.md | critic_agent | 60 min | ✅ |

**Layer 1 Total:** ~9 hours (single session or split across 2 days)

---

## LAYER 2 FREQUENCIES (Code Planning + Stress Test)

| Phase | Agent | Estimated Time | Git Commit Required |
|-------|-------|----------------|---------------------|
| Phase 1: requirements2.md | architect_agent | 60 min | ✅ |
| Phase 2: architecture2.md | architect_agent | 90 min | ✅ |
| Phase 3: dependency_graph2.md | architect_agent | 60 min | ✅ |
| Phase 4: module_dependencies2.md | architect_agent | 45 min | ✅ |
| Phase 5: file_manifest2.md | architect_agent | 75 min | ✅ |
| Phase 6: critic_prebuild2.md | critic_agent | 90 min | ✅ |
| Phase 7: task_schedule2.md | architect_agent | 60 min | ✅ |
| Phase 8: structure_confirmed2.md | architect_agent + CLI | 75 min | ✅ |
| Phase 9: critic_final2.md | critic_agent | 75 min | ✅ |

**Layer 2 Total:** ~10.5 hours

**codingschedule.md:** Generated after Layer 2 Phase 9 approval (~30 min)

---

## LAYER 3 FREQUENCIES (Implementation Phases)

Layer 3 executes in 10 phases based on the task_schedule from Layer 2.

| Phase | Focus | Estimated Time | Git Commit |
|-------|-------|----------------|------------|
| Phase 1 | Core types, interfaces, enums | 45 min | ✅ |
| Phase 2 | MaterialResponseSystem, WoundSystem | 60 min | ✅ |
| Phase 3 | ClawComponent, RageComponent | 90 min | ✅ |
| Phase 4 | WolverineCharacter + MovementComponent | 90 min | ✅ |
| Phase 5 | AI systems (Behavior Trees, EQS) | 75 min | ✅ |
| Phase 6 | World systems (district streaming, weather) | 75 min | ✅ |
| Phase 7 | Audio (MetaSounds), Haptics | 60 min | ✅ |
| Phase 8 | HUD, TraumaSystem, Safe Houses | 60 min | ✅ |
| Phase 9 | Integration, tests, polish | 90 min | ✅ |
| Phase 10 | Final critic, packaging prep | 60 min | ✅ |

**Layer 3 Total:** ~11.75 hours

---

## CRITIC GATE FREQUENCIES

| Gate | Trigger | Max Wait Time | Action on Failure |
|------|---------|---------------|-------------------|
| critic_prebuild (L1P6) | After file_manifest | 75 min | RETURN TO PHASE N |
| critic_final (L1P9) | After structure_confirmed | 75 min | RETURN TO PHASE N |
| critic_prebuild2 (L2P6) | After file_manifest2 | 90 min | RETURN TO PHASE N |
| critic_final2 (L2P9) | After structure_confirmed2 | 75 min | RETURN TO PHASE N |
| critic_layer3 (each phase) | After each L3 phase | 45 min | RETURN TO PHASE N |

**Rule:** Critic returns "RETURN TO PHASE [N]" → execute immediately. Do not proceed.

---

## GIT COMMIT FREQUENCIES

| Event | Commit Message Pattern |
|-------|------------------------|
| After each Layer 1 phase | `L1P[N]: [phase_name] — [brief_description]` |
| After each Layer 2 phase | `L2P[N]: [phase_name] — [brief_description]` |
| After each Layer 3 phase | `L3P[N]: [phase_name] — [brief_description]` |
| After critic approval | `CRITIC: Layer [N] Phase [M] — APPROVED` |
| After repair cycle | `REPAIR: [file_name] — [error_fixed]` |

**Commit Frequency:** Every 45-90 minutes during active development

---

## REPAIR LOOP FREQUENCIES

| Layer | Max Repair Cycles | Avg Time per Cycle | Trigger |
|-------|-------------------|--------------------|---------|
| Layer 1 | 3 per phase | 30 min | Critic rejection |
| Layer 2 | 3 per phase | 30 min | Critic rejection |
| Layer 3 | 3 per file | 20 min | UHT/UBT failure |

**Rule:** After 3 failed repair cycles → escalate to architect_agent for redesign.

---

## MILESTONE FREQUENCIES

| Milestone | Target | Cumulative Time |
|-----------|--------|-----------------|
| CLAWS IN GAME | End L3P3 | ~20 hours |
| CHARACTER IN WORLD | End L3P4 | ~25 hours |
| FULL COMBAT LOOP | End L3P5 | ~30 hours |
| AI + WORLD COMPLETE | End L3P6 | ~35 hours |
| AUDIO + HUD COMPLETE | End L3P8 | ~40 hours |
| INTEGRATION COMPLETE | End L3P9 | ~45 hours |
| READY FOR PACKAGING | End L3P10 | ~47 hours |

---

## DAILY CADENCE (Recommended)

| Day | Focus | Target |
|-----|-------|--------|
| Day 1 | Layer 1 (Phases 1-5) | requirements → file_manifest |
| Day 2 | Layer 1 (Phases 6-9) | critic_prebuild → critic_final |
| Day 3 | Layer 2 (Phases 1-5) | requirements2 → file_manifest2 |
| Day 4 | Layer 2 (Phases 6-9) | critic_prebuild2 → critic_final2 + codingschedule.md |
| Day 5 | Layer 3 (Phases 1-4) | Core systems → WolverineCharacter |
| Day 6 | Layer 3 (Phases 5-7) | AI → Audio/Haptics |
| Day 7 | Layer 3 (Phases 8-10) | HUD → Packaging prep |

**Total Development Time:** ~47 hours over 7 days

---

## HARD REQUIREMENTS VERIFICATION FREQUENCY

| HR | Verification Point | Method |
|----|--------------------|--------|
| HR-01 (Claws < 10s) | L1P6, L3P3, L3P9 | Time measurement from game start |
| HR-02 (Mesh deformation) | L1P6, L3P2, L3P9 | Nanite/Chaos compatibility check |
| HR-03 (No loading screens) | L1P2, L3P6 | Level streaming test |
| HR-04 (Rage event-driven) | L1P6, L3P3, L3P9 | Grep Blueprint for manual triggers |
| HR-05 (Persistent destruction) | L1P6, L3P6 | Save/load cycle test |
| HR-06 (6 material types) | L1P1, L3P2 | MaterialResponseSystem audit |
| HR-07 (Predator optional) | L1P2, L3P5 | Stealth/combat path audit |
| HR-08 (No skill trees) | L1P1, L3P8, L3P9 | UMG widget grep for XP/levels |

---

## DECISION_HASH
```json
{
  "document": "wfreqs.md",
  "project": "wolf.beast",
  "version": "1.0",
  "created": "2026-03-08",
  "layer1_phases": 9,
  "layer2_phases": 9,
  "layer3_phases": 10,
  "total_estimated_hours": 47,
  "critic_gates": 20,
  "hard_requirements": 8,
  "functional_requirements": 20,
  "non_functional_requirements": 8
}
```

---

*WOLVERINE: UNBOUNDED — A FORGE Game*
*Private Repository — All Rights Reserved*
