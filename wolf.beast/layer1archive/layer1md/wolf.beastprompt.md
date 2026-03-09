================================================================
WOLVERINE: UNBOUNDED
A FORGE Game Brief — prompt.md
Read exactly once by architect_agent. Never read again after Layer 1.
================================================================

## GOVERNANCE
**Parent Document:** critic_final.md (Layer 1 Phase 9)
**Status:** READ-ONLY — Source document. Modifications require architect review.
**Layer:** L0 (Source)

================================================================

LICENSE
───────
Private Repository — All Rights Reserved
Game output owned entirely by developer.
Unreal Engine 5 royalty: 5% gross revenue after first $1M USD
per product per calendar year (Epic Games standard EULA).
No FORGE royalty on shipped game.

ENGINE:          Unreal Engine 5.3+
TARGET PLATFORMS: PC (primary), PS5, Xbox Series X
GENRE:           Third-person open world action
REFERENCE:       Spider-Man PS4 (traversal fluidity + open world density)
                 X-Men Origins: Wolverine PS3 (combat viscerality)
                 Batman: Arkham City (world design + predator gameplay)
TONE:            Brutal. Personal. Noir western in a modern city.
                 Wolverine is not a hero. He is a consequence.

================================================================
THE GAME
================================================================

LOGLINE:
Logan has been living off-grid in a decaying industrial city —
part Montreal, part Detroit, part nowhere — when a Weapon X
splinter cell begins kidnapping mutants from the streets.
Nobody sends him. Nobody asks him. He goes anyway.
Over 72 hours the city tears itself apart and so does he.

THIS IS NOT AN ORIGIN STORY.
Logan knows exactly what he is. The claws come out in the
first ten seconds. The game never makes you wait to be Wolverine.

================================================================
THE FEEL — WHAT EVERY SYSTEM MUST SERVE
================================================================

THE THREE PILLARS:

PILLAR 1 — YOU FEEL THE CLAWS
  Not button presses. Physical events.
  When claws hit flesh: camera micro-stutters, controller vibrates
  asymmetrically (left claw, right claw separately), audio has
  weight and wet resistance, enemies react with real physics.
  When claws hit metal: sparks, screech, different resistance.
  When claws hit concrete: chunks, dust, grinding.
  The material system is not cosmetic. It is the combat.

PILLAR 2 — DAMAGE IS A RESOURCE
  Logan takes real damage. Wounds appear on the model in real time.
  Slashes across chest. Bullet holes. Burn marks.
  Healing factor closes them visibly over seconds.
  Low health = more wounds visible = faster healing rate
  (body compensating) = higher rage multiplier.
  Getting hurt makes you more dangerous.
  This is not just visual. Damage state affects every system.

PILLAR 3 — THE CITY IS ALIVE AND DESTRUCTIBLE
  Open world. Not a sandbox. A living place.
  Civilians react to mutant violence. Police escalate.
  Weapon X operatives patrol. Mutant underground exists.
  Every street fight has consequences that ripple outward.
  Nothing resets. Destroyed environments stay destroyed.
  The city remembers what Logan did.

================================================================
WORLD
================================================================

CITY: PORT ASHFORD
  Fictional post-industrial city. Population 800,000.
  Three districts, each with distinct identity:

  THE BASIN (starting area):
    Former industrial waterfront. Rusted cranes, warehouses,
    container yards. Weapon X is operating here openly.
    Low-rise, dense, brutal architecture.
    Night-time rain for first act. Always wet.

  MIDTOWN ASHFORD:
    Downtown. Glass and steel over crumbling foundations.
    Civilians dense. Police presence heavy.
    Weapon X has infiltrated city government.
    Mutant underground hides in the subway system below.

  THE RIDGE:
    Elevated residential and campus district.
    Ashford Biomedical (Weapon X front company) HQ here.
    Clean surface. Rot underneath.
    Final act takes place here.

WORLD SCALE:
  Traversable on foot or via claw-sprint and environment climbing.
  No fast travel. Distance is deliberate — Logan walks
  through the consequences of what he did.
  15-20 minute traverse time across full city on foot.
  3-5 minutes using full movement kit.

TIME OF DAY / WEATHER:
  Dynamic. 72-hour story plays in real game time (compressed).
  Night 1: rain, Basin, establishing brutality.
  Day 1: Midtown, consequences, exposure.
  Night 2: escalation, Ridge approach.
  Weather affects combat (rain slicks surfaces, reduces visibility),
  stealth (noise masking), and enemy behaviour (patrols tighten).

================================================================
COMBAT SYSTEM
================================================================

PHILOSOPHY:
  Spider-Man PS4 reference = fluidity and momentum.
  Wolverine application: every attack chains into the next
  without stopping. No attack animations that lock you in place
  longer than necessary. Aggression is always rewarded.
  Standing still is always punished.

BASIC FRAMEWORK:
  Light attack:   fast claw swipes, builds combo
  Heavy attack:   slow powerful slash, breaks guard, staggers
  Dodge:          short burst in any direction (not a roll —
                  Wolverine doesn't roll, he lurches)
  Grab:           context-sensitive, different near walls/ledges/enemies
  Rage:           fills from damage taken + damage dealt, see below

COMBO SYSTEM:
  Freeform directional. Not a locked string system.
  Direction + attack = different strike angle.
  Aerial attacks available from any jump.
  Enemy ragdoll is physically simulated — where they land
  affects what you can do next (pin against wall, slam to ground,
  throw into group).

CLAW LUNGE:
  Hold aim + attack = claw lunge across gap to enemy.
  Covers 15-20 meters. Can chain: lunge → hit → lunge → hit.
  This is the Spider-Man traversal equivalent for combat.
  Crossing a room in three seconds through four enemies
  via consecutive lunges is the core power fantasy.

RAGE SYSTEM:
  Fills from: taking damage, landing combos, environmental kills.
  Depletes when: not fighting (30 second drain if idle).
  Low rage:  normal combat
  Mid rage:  attacks leave burning claw trails, faster healing
  Full rage: BERSERKER MODE
    Camera pulls slightly wider
    Animations change (more feral, less precise)
    Damage multiplier 3x
    Healing factor at maximum
    Enemies show fear response (some flee, some freeze)
    Duration: 20 seconds or until rage depletes
    Cannot be manually activated — must be earned through damage

ENVIRONMENTAL KILLS:
  Every environment has kill opportunities.
  Throw enemy into electrical panel: electrocution.
  Slam into pipe: impalement (M-rated, not gratuitous — consequence).
  Throw through window: fall damage.
  Car door: brutal improvised weapon, then discard.
  The environment is always a weapon.

ENEMY TYPES:
  WEAPON X SOLDIERS:     trained, coordinated, flank by default
  HEAVY UNITS:           powered armour, require claw pry to damage
  MUTANT HUNTERS:        counter-mutant tech, can dampen healing factor
  FERAL MUTANTS:         fast, unpredictable, dodge-heavy
  SENTINELS (late game): large, multi-phase, environmental destruction

PREDATOR MODE:
  (Arkham City reference)
  Some missions require no detection.
  Vent system traversal. Silent takedowns from above.
  Claw marks on surfaces as environmental storytelling.
  Enemies find bodies and escalate.
  Logan is absolutely not stealthy. The point is that he tries.
  Failed stealth = full combat, which is always an option.

================================================================
MOVEMENT SYSTEM
================================================================

TRAVERSAL PHILOSOPHY:
  Logan does not fly. He does not web-swing.
  He moves like a predator — low, fast, always threatening.
  But he is extremely physically capable.
  The traversal must feel powerful without feeling superhuman-floaty.

MOVEMENT KIT:
  SPRINT:          full speed run, claws retracted
  CLAW SPRINT:     claws out, can slash obstacles/enemies while running,
                   slightly slower but combat-ready
  WALL CLIMB:      claw into any climbable surface (brick, concrete,
                   metal — not glass), full vertical + horizontal
  LEDGE VAULT:     automatic when sprinting toward chest-height obstacle
  CLAW SWING:      throw claw into overhead surface, swing on it,
                   release to launch — covers 20-30m horizontal
                   (Spider-Man reference — limited version, requires
                    valid surface overhead, not infinite web)
  DROP:            from any height, land on enemy = ground slam
  CLAW BRAKE:      drag claws on wall while falling = controlled descent

TRAVERSAL FEEL TARGET:
  Moving across the Basin at full speed using claw swing + wall climb
  + ledge vault should feel like watching a hunting animal move.
  Fast. Low. Every surface is something to push off from.
  Reference: Mirror's Edge momentum + Spider-Man PS4 fluidity
  applied to a ground/wall hybrid mover.

================================================================
PROGRESSION SYSTEM
================================================================

NO SKILL TREES. NO MENUS.
Logan does not unlock abilities. He already has them.
What changes is Logan's control over himself.

TRAUMA SYSTEM (replaces XP/levels):
  Completing missions + finding collectibles unlocks MEMORIES.
  Memories are not cutscenes. They are playable fragments —
  30-60 second first-person flashbacks of past violence.
  Each memory unlocked = Logan masters one aspect of control.
  Mechanical result: combo window extends slightly,
                     rage meter fills faster,
                     healing factor efficiency improves.
  This is narrative-mechanical integration:
  Logan gets better at fighting as he accepts what he is.

WEAPON X INTEL (collectible system):
  Files found in the world. Audio logs. Photographs.
  Each one expands the story of what Weapon X did.
  No map markers. Found by exploration + following leads.

SAFE HOUSES:
  4 locations across the city. Hidden.
  Logan sleeps. Wounds fully heal. Time advances.
  No upgrade menus here. Just rest and a journal.
  The journal updates automatically with Logan's internal
  monologue about what just happened. First person, terse.

================================================================
NARRATIVE STRUCTURE
================================================================

ACTS:
  ACT 1 — THE BASIN (3-4 hours)
    Logan arrives. Finds first mutant victim. Weapon X soldiers
    are everywhere. Establishes: what is happening, who is doing it.
    Ends with: Logan captured, claws neutralised briefly.

  ACT 2 — MIDTOWN (4-5 hours)
    Escape. Logan exposed in populated area.
    Meets mutant underground. Alliance of necessity — not friendship.
    Weapon X goes public: frames Logan for violence.
    Police, media, civilians all against him.
    Ends with: mutant underground betrayal.

  ACT 3 — THE RIDGE (3-4 hours)
    Alone. City locked down. Ashford Biomedical tower.
    Everything Weapon X built comes apart from the inside.
    Final confrontation: not a boss — a reckoning.
    Ends: ambiguous. Logan leaves. City is changed. So is he.

TONE NOTES:
  No quips. Logan is not funny in this game.
  No redemption arc. He does not become a better person.
  Supporting characters die. Some because of him.
  The violence has weight because the story gives it weight.
  Player should feel effective and uncomfortable simultaneously.

KEY CHARACTERS:
  LOGAN:          Player character. 197 years old. Tired.
  DR. REYES:      Weapon X lead scientist. True believer, not villain.
                  She thinks she is saving mutantkind. She is wrong.
  ECHO:           Mutant underground contact. Telepathic. Sees
                  everything Logan has done. Helps him anyway.
  DIRECTOR HARROW: Weapon X commander. Has the adamantium files.
                   Knows exactly what Logan is. Has a use for it.
  VICTOR:         Shows up at Act 2 end. Not an ally. Not quite enemy.
                  Has his own reasons for being here.

================================================================
AUDIO DESIGN
================================================================

MUSIC:
  No orchestral score. No licensed tracks.
  Reactive ambient score — industrial, percussive, atonal.
  Combat: rhythm builds with combo count.
  Stealth: sparse, tension-based.
  Exploration: city ambience, distant sirens, rain.
  Rage mode: music drops to pure percussion and distortion.

SOUND DESIGN PRIORITIES (in order):
  1. Claw deployment: iconic, immediate, satisfying
  2. Claw impacts per material (6 material types minimum)
  3. Healing: wet cellular sound, subtle, continuous during recovery
  4. Enemy reactions: fear escalation through voice
  5. City ambience: layered, directional, always present

VOICE:
  Logan: minimal. Speaks when necessary. Interior monologue in journal.
  Enemies: reactive to combat state, material, situation.
  Civilians: panic, specific, not generic.

================================================================
VISUAL DIRECTION
================================================================

RENDERING:
  Lumen (global illumination) — critical for wet surfaces at night
  Nanite — high density urban geometry without LOD pop
  Ray-traced shadows in performance mode optional

COLOUR PALETTE:
  Basin:   near-monochrome. Blue-black. Orange industrial light.
  Midtown: cold white fluorescent over dirty concrete.
  Ridge:   false warmth. Corporate beige over clinical white.
  Rage mode: desaturation + red vignette (subtle — not comic book)

WOLVERINE MODEL:
  No costume for first two acts. Civilian clothes that get
  progressively destroyed over the 72 hours.
  Wounds visible on model at all times.
  Healing visible: skin knitting, cloth does NOT repair
  (costume damage is permanent — visual storytelling).
  Claws: wet when deployed from flesh. Dry when retracted.

HUD PHILOSOPHY:
  Minimal. Health shown as wound density on model, not bar.
  Rage shown as vignette intensity, not meter (until full rage).
  Objective: compass bearing only, no waypoint beam.
  Player learns to read the world, not the HUD.

================================================================
HARD REQUIREMENTS FOR FORGE architect_agent
================================================================

HR-01  CLAWS DEPLOY IN FIRST 10 SECONDS OF GAMEPLAY.
       Tutorial does not exist. The opening IS the tutorial.

HR-02  DAMAGE MODEL IS REAL-TIME ON CHARACTER MESH.
       Not a texture swap. Actual mesh deformation for major wounds.
       Healing is visible mesh restoration.

HR-03  NO LOADING SCREENS WITHIN THE CITY.
       District transitions seamless. Only loading: game start,
       fast travel to safe house (if implemented), mission replay.

HR-04  RAGE CANNOT BE MANUALLY ACTIVATED.
       It is earned through damage taken. Never a button press.
       Any design that makes rage a cooldown = wrong.

HR-05  ENVIRONMENTAL DESTRUCTION IS PERSISTENT.
       Destroyed objects do not respawn. Ever.
       The city remembers. Design all areas accordingly.

HR-06  CLAW MATERIAL SYSTEM HAS MINIMUM 6 MATERIAL TYPES.
       Flesh, bone, light metal, heavy metal, concrete, glass.
       Each with distinct audio, visual, and haptic response.

HR-07  PREDATOR MODE IS ALWAYS OPTIONAL.
       Every stealth section has a loud solution.
       Never lock the player out of combat.

HR-08  NO SKILL TREES. NO UPGRADE MENUS.
       Progression is entirely through the Trauma System.
       UI should never show XP numbers, level numbers, or skill points.

================================================================
FUNCTIONAL REQUIREMENTS
================================================================

FR-01  Open world city (Port Ashford) — three distinct districts
FR-02  Seamless traversal: claw sprint, wall climb, claw swing, drop
FR-03  Freeform directional combo combat system
FR-04  Claw lunge (gap-close attack, chainable)
FR-05  Rage system: fills from damage, drains when idle, Berserker Mode
FR-06  Real-time wound + healing system on character mesh
FR-07  Material-responsive claw impact system (6 types)
FR-08  Environmental kill system (context-sensitive per environment)
FR-09  Enemy AI: soldier coordination, fear response, escalation
FR-10  Predator mode: vent traversal, silent takedowns, body discovery
FR-11  Trauma System progression (memories → mechanical improvement)
FR-12  Dynamic weather system (rain, time of day, lighting impact)
FR-13  Persistent environmental destruction
FR-14  Mutant escalation system (city response to Logan's actions)
FR-15  Weapon X Intel collectible system (no map markers)
FR-16  4 safe houses with journal system
FR-17  Three-act narrative with playable memory fragments
FR-18  Reactive audio score (combat intensity → music intensity)
FR-19  Minimal HUD (wound-based health, vignette rage, compass only)
FR-20  Haptic feedback system (asymmetric per claw, per material)

================================================================
NON-FUNCTIONAL REQUIREMENTS
================================================================

NFR-01  60fps performance mode on PS5 / Xbox Series X
NFR-02  Claw deploy-to-first-impact: < 200ms from button press
NFR-03  Healing visual: begins within 500ms of damage event
NFR-04  Enemy AI response to player position update: < 100ms
NFR-05  City population density: minimum 40 civilians visible
         in populated districts at any time
NFR-06  Persistent destruction state survives save/load cycle
NFR-07  Memory fragment load time: < 2 seconds (seamless feel)
NFR-08  Audio mix: claw impact never masked by music or ambience

================================================================
TECH STACK (FORGE architect_agent decisions)
================================================================

Engine:         Unreal Engine 5.3+
Rendering:      Lumen + Nanite (required — city density demands it)
Physics:        Chaos Physics (ragdoll + environmental destruction)
Animation:      Motion Matching (traversal fluidity requirement)
                Control Rig (procedural claw deployment/retraction)
AI:             Behavior Trees + EQS (Environment Query System)
Audio:          MetaSounds (reactive score system)
Haptics:        Platform-native (DualSense adaptive triggers for
                claw resistance per material)
Destruction:    Chaos Destruction (persistent, not resetting)
Crowd:          Mass AI (city population density)

================================================================
9-PHASE ENGINE INSTRUCTIONS
================================================================

EXECUTION RULES:
- Read every phase completely before starting.
- Produce output MD before proceeding.
- Do not skip or merge phases.
- Git commit after every phase.
- Critic returns RETURN TO PHASE [N]: execute immediately.
- Every MD begins with SUMMARY block (150 tokens max).
- Every MD ends with DECISION_HASH block (JSON).
- Phase 6 and Phase 9: read DECISION_HASH first,
  full content only on contradiction.

================================================================
LAYER 1 — ARCHITECTURE PLANNING
Reads: prompt.md only
Produces: /layer1/ — 9 MD files
================================================================

PHASE 1 → /layer1/requirements.md
  Read: prompt.md
  Extract: all FRs, NFRs, HRs.
  For each HR: what FORGE test proves it is satisfied?
  HR-01: first claw deployment time measured from game start.
  HR-02: wound system — what does "mesh deformation" require
         technically? Define the UE5 implementation approach.
  HR-04: rage activation — grep all Blueprint for manual trigger.
  HR-08: grep all UMG widgets for XP/level/skill references.
  Make every requirement binary testable.

PHASE 2 → /layer1/architecture.md
  Read: prompt.md + layer1/requirements.md
  Design: complete UE5 game architecture.
  Include:
    GameMode / GameState / PlayerState hierarchy for Wolverine
    Character component breakdown:
      WolverineMovementComponent (custom — extends CharacterMovement)
      ClawComponent (deployment, material detection, impact dispatch)
      WoundSystemComponent (mesh deformation, healing tick)
      RageComponent (fill rate, drain rate, Berserker state machine)
      TraumaSystemComponent (memory unlock, mechanical bonuses)
    AI architecture: Weapon X soldier BT, fear state machine,
                     escalation manager (city-wide state)
    World architecture: district streaming, destruction persistence,
                        weather system, time-of-day progression
    Audio architecture: MetaSounds reactive graph
    HUD architecture: minimal (wound-driven, vignette-driven)
  Every component maps to ≥1 FR/NFR/HR.

PHASE 3 → /layer1/dependency_graph.md
  Read: layer1/architecture.md
  Build: UE5 module dependency graph.
  Nodes: every C++ module, every major Blueprint system,
         every plugin dependency.
  Critical: ClawComponent depends on MaterialResponseSystem
            WoundSystem depends on ClawComponent impact events
            RageComponent depends on WoundSystem damage events
            TraumaSystem depends on MissionSystem completion events
  Cycle detection on module graph.
  Any cycle = return to Phase 2.

PHASE 4 → /layer1/module_dependencies.md
  Read: layer1/dependency_graph.md
  Topo sort → UBT build levels.
  Level 0: Core types, enums, interfaces (no game deps)
  Level 1: MaterialResponseSystem, WoundSystem (no player deps)
  Level 2: ClawComponent, RageComponent (depends L1)
  Level 3: WolverineCharacter (depends L2)
  Level 4: AI, World, Audio (depends L3)
  Level 5: UI, HUD (depends L4)
  Critical path: Core → Material → Claw → Character
                 (this is the minimum to get claws in game)

PHASE 5 → /layer1/file_manifest.md
  Read: layer1/module_dependencies.md
  List: EVERY file.
  C++ files: .h + .cpp pairs, topo level, FR refs
  Blueprint files: name, parent class, purpose, FR refs
  Config files: DefaultGame.ini, DefaultInput.ini sections
  Include: every UE5 Automation Test file
  Include: MetaSounds assets (named, not implemented)
  This list is complete and final.

PHASE 6 → /layer1/critic_prebuild.md
  Read: ALL Layer 1 MDs + prompt.md (DECISION_HASH first)
  Critical checks:
    HR-01: does architecture guarantee claw deploy < 10s?
           What is the opening sequence? Is it designed yet?
    HR-02: is mesh deformation technically feasible with
           Chaos Physics + Nanite? Nanite and mesh deform conflict —
           RESOLVE THIS before Layer 2.
    HR-04: is RageComponent state machine truly event-driven
           with no manual activation path?
    HR-05: how does persistent destruction survive level streaming?
           District reloads — does destruction state persist?
    Motion Matching: does it handle wall climb + claw swing
           transitions? Or does it require custom animation nodes?
  Output: APPROVED or RETURN TO PHASE [N].

PHASE 7 → /layer1/task_schedule.md
  Read: layer1/file_manifest.md + layer1/critic_prebuild.md
  JSON task graph.
  First milestone: CLAWS IN GAME
    task_ids that get to playable claw combat in empty level.
    This is the first vertical slice.
    Target: end of parallel group covering Level 0-3 files.
  Second milestone: CHARACTER IN WORLD
    Movement kit working in Port Ashford geometry.
  Third milestone: FULL COMBAT LOOP
    Rage + wounds + material response all functional.

PHASE 8 → /layer1/structure_confirmed.md
  Read: layer1/file_manifest.md + layer1/task_schedule.md
  Action: Create ALL folders, C++ header stubs, Blueprint stubs.
  C++ stubs: correct UCLASS/UPROPERTY/UFUNCTION macros,
             correct parent class, correct includes.
             Zero implementation — pass bodies only.
  Blueprint stubs: correct parent class, correct event graph
                   entry points. Zero node logic.
  Produce: file count diff. Must match exactly.

PHASE 9 → /layer1/critic_final.md
  Read: ALL Layer 1 MDs + actual folder structure
  Verify:
    Folder matches file_manifest.md exactly.
    All C++ stubs pass UHT dry-run (macro compliance).
    HR-02 Nanite/mesh deform conflict: resolution documented.
    RageComponent: no manual activation path in any stub.
    No skill tree / XP / level references in any UMG stub.
    Persistent destruction: streaming solution defined.
  Output: APPROVED or RETURN TO PHASE [N].
  APPROVED = Layer 1 permanently frozen.

================================================================
LAYER 2 — CODE PLANNING + STRESS TEST
Reads: ENTIRE /layer1/ at every phase
Produces: /layer2/ — 9 MD files + codingschedule.md
================================================================

PHASE 1 → /layer2/requirements2.md
  Read: ENTIRE /layer1/
  Re-derive at code level.
  Critical additions:
    Motion Matching dataset: what animations needed for
    wall climb → claw swing → aerial lunge chain?
    How many motion matching clips minimum for fluid traversal?
    Chaos Destruction + streaming: exact technical solution
    for persistent destruction across district boundaries?
    MetaSounds reactive graph: what parameter drives
    combat intensity? How does combo count map to audio?
    DualSense haptics: does UE5.3 support per-trigger
    asymmetric haptic strength natively?

PHASE 2 → /layer2/architecture2.md
  Read: ENTIRE /layer1/ + layer2/requirements2.md
  Validate all Layer 1 architectural decisions.
  Critical:
    Nanite + wound deformation conflict:
      Nanite does not support skeletal mesh deformation.
      Solution: Logan character uses non-Nanite skeletal mesh.
      World geometry uses Nanite. Confirm this is Layer 1 error
      corrected here and document the fix.
    Motion Matching traversal: define exact blend parameters.
    ClawComponent material detection: line trace per claw tip
    per frame, or collision event? Which is performant at 60fps?

PHASE 3 → /layer2/dependency_graph2.md
  Read: ENTIRE /layer1/ + layer2/architecture2.md
  Validate all C++ dependencies installable/available.
  Validate all UE5 plugin dependencies (built-in vs marketplace).
  Produce: list of all plugins required with versions.
  Check: Motion Matching plugin availability in UE5.3.
  Check: MetaSounds is built-in (confirm version).

PHASE 4 → /layer2/module_dependencies2.md
  Read: ENTIRE /layer1/ + layer2/dependency_graph2.md
  Validate UBT build order at C++ import level.
  Critical: WoundSystemComponent tick rate — if healing runs
  every frame at 60fps on mesh deformation, what is the
  performance budget? Define tick group and tick interval.

PHASE 5 → /layer2/file_manifest2.md
  Read: ENTIRE /layer1/ + layer2/module_dependencies2.md
  Full C++ contracts:
    Every UCLASS: name, parent, key UPROPERTY fields with types
    Every UFUNCTION: name, params, return, BlueprintCallable?
    Every component: BeginPlay, TickComponent, key events
  Blueprint contracts:
    Every Blueprint: parent class, exposed variables,
    event graph entry points (BeginPlay, custom events)
  Critical contracts:
    UWolverineClawComponent::OnClawImpact(
      FHitResult Hit, EClawMaterialType Material) → void
    UWolverineWoundSystem::ApplyWound(
      FVector Location, float Severity) → void
    UWolverineRageComponent::OnDamageReceived(
      float Amount, AActor* Source) → void
      (no public ActivateRage function — enforces HR-04)

PHASE 6 → /layer2/critic_prebuild2.md
  Read: ENTIRE /layer1/ + ALL /layer2/ (DECISION_HASH first)
  Cross-layer stress test:
    Nanite fix confirmed in architecture2.md?
    HR-04: UWolverineRageComponent has NO public ActivateRage?
           Check file_manifest2.md. If it exists = FAIL.
    HR-08: search all UMG contracts for XP/level/skill. Must be empty.
    Motion Matching: animation clip count sufficient for
                     fluid traversal? Define minimum.
    Persistent destruction: solution from architecture2.md
                            correctly reflected in module contracts?
  Output: APPROVED or RETURN TO PHASE [N].

PHASE 7 → /layer2/task_schedule2.md
  Read: layer2/file_manifest2.md + layer2/critic_prebuild2.md
  Session milestones:
    MILESTONE 1 — CLAW VERTICAL SLICE
      ClawComponent + MaterialResponseSystem + basic combat
      Testable: claw deploy, impact, 6 material responses
    MILESTONE 2 — MOVEMENT VERTICAL SLICE
      WolverineMovementComponent + Motion Matching base
      Testable: sprint, wall climb, claw swing in test level
    MILESTONE 3 — DAMAGE LOOP
      WoundSystem + RageComponent + healing visual
      Testable: take damage → wound appears → heals → rage fills
    MILESTONE 4 — ENEMY LOOP
      Soldier BT + fear state + escalation manager
      Testable: soldier flanks, registers rage, attempts retreat
    MILESTONE 5 — WORLD INTEGRATION
      Port Ashford geometry + destruction + weather + population
    MILESTONE 6 — FULL GAME LOOP
      All systems integrated, Act 1 playable

PHASE 8 → /layer2/structure_confirmed2.md
  Read: layer2/file_manifest2.md + layer2/task_schedule2.md
  Validate: all C++ stubs match contracts in file_manifest2.md.
  UHT compile: all UCLASS macros correct.
  HR-04 final check: grep all stubs for ActivateRage public
  function. Must return zero results.

PHASE 9 → /layer2/critic_final2.md
  Read: ENTIRE /layer1/ + ALL /layer2/ + folder structure
  Final sign-off:
    Nanite/skeletal mesh conflict resolved.
    HR-04 enforced in contracts (no public rage activation).
    HR-08 enforced (no XP/level in any contract).
    Motion Matching clip list defined and sufficient.
    Persistent destruction solution architecturally sound.
    All 6 material types defined in EClawMaterialType enum.
  Output: APPROVED or RETURN TO PHASE [N].
  APPROVED = Layer 1 + Layer 2 permanently frozen.

PHASE 10 → /layer2/codingschedule.md
  Read: ALL /layer2/ only
  Milestone-driven schedule.
  Every session maps to one milestone or sub-milestone.
  Each session has: files, validation method, milestone target.
  First session: Core types + EClawMaterialType enum + IWolverineInterface
  These unblock everything. Build them first.

================================================================
LAYER 3 — CODE EXECUTION
Reads: Layer 2 MDs + code being written. NEVER Layer 1.
Produces: /layer3/codecriticlayer3phaseN.md per session
================================================================

SESSION PATTERN:
  BUILD: implement session N against file_manifest2.md contracts.

  VALIDATE per session:
    UHT: all UCLASS macros valid
    UBT: module compiles clean
    HR check relevant to session:
      Claw sessions:    material enum has exactly 6 types
      Rage sessions:    grep for ActivateRage public → must be empty
      UI sessions:      grep UMG for XP/level → must be empty
      Destruction sess: verify no reset timer in destruction code

  PRODUCE: /layer3/codecriticlayer3phaseN.md
    session_id, files_built, ubt_result, uht_result,
    hr_checks: {hr_id: PASS|FAIL},
    contract_compliance: PASS|FAIL per file,
    milestone_progress: which milestone this advances,
    overall: APPROVED|RETURN TO [filename] and why

  GIT COMMIT after APPROVED only.
  TAG each milestone completion: git tag milestone-N

DRIFT PROTOCOL:
  UBT/UHT error:      fix file → re-run session critic
  Contract error:     return to layer2/file_manifest2.md
                      Layer 2 repair from Phase 5
  Design error:       return to layer2/architecture2.md
                      Layer 2 repair from Phase 2
  HR violation found: HALT. Return to source phase.
                      Do not patch forward.
  Never Layer 1. Never patch forward past source of drift.

================================================================
MILESTONES AT A GLANCE
================================================================

M1  CLAW VERTICAL SLICE      Claws deploy, impact 6 materials,
                              camera + haptic + audio all respond
M2  MOVEMENT VERTICAL SLICE  Full traversal kit in test level
M3  DAMAGE LOOP              Wounds + healing + rage all functional
M4  ENEMY LOOP               Soldiers think, fear, escalate
M5  WORLD INTEGRATION        Port Ashford alive + destructible
M6  FULL GAME LOOP           Act 1 playable start to finish
M7  CONTENT COMPLETE         All three acts playable
M8  PLATFORM GOLD            PC + PS5 + Xbox builds passing cert

================================================================
CONTEXT BUDGET
================================================================

Layer 1 per phase:
  Ph 1:   prompt.md only               ~5k tokens
  Ph 2:   prompt + req                 ~10k tokens
  Ph 3-5: single prior MD              ~6-8k each
  Ph 6:   ALL L1 + prompt              ~35k ← cliff
  Ph 7-8: 2 MDs                        ~12k
  Ph 9:   ALL L1 + folder              ~40k ← cliff

Layer 2 per phase:
  Ph 1-5: ALL L1 + growing L2          ~40-55k
  Ph 6:   ALL L1 + ALL L2              ~65k ← peak
  Ph 9:   ALL L1 + ALL L2 + folder     ~70k ← peak

Layer 3 per session:
  3 L2 MDs + prev critic + code        ~15-20k ← bounded

Model requirements:
  Layer 1: 64k minimum (game arch is denser than software arch)
  Layer 2: 128k minimum
  Layer 3: 32k sufficient

================================================================
SUMMARY COMPRESSION RULE
================================================================

Every MD begins with:
## SUMMARY (max 150 tokens)

Every MD ends with:
## DECISION_HASH
```json
{
  "key_decisions": [],
  "constraints": [],
  "derived_from": "filename",
  "derived_from_hash": "sha256"
}
```

Phase 6 + Phase 9: DECISION_HASH first. Full content on contradiction.

================================================================
END OF prompt.md
Logan doesn't wait to be Wolverine.
Neither does the game.
================================================================