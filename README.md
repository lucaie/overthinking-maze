# overthinking-maze

A small browser task for studying **overthinking as deliberation beyond the value of computation**. Part of a COGS 188D final project (Option 3, Project B: policy compression, Prof. Lucy Lai, UCSD, fall 2026).

The design is Mouselab-MDP style (Callaway, Lieder, Krueger & Griffiths, 2017) with an added **memory phase**, so one task measures both cognitive costs:

- **Computation:** clicks that reveal hidden rewards (each click costs points), plus planning time.
- **Policy complexity (memory):** the chosen path must be walked from memory. Its cost is the turn-coded policy complexity *I(S;A)* in nats.

Current version: **v2.8** (`index.html`).

## One round
1. **Price card (3 s):** shows this round's click price (2 or 4 pt) and whether there's a time limit.
2. **Start:** the maze stays hidden until the player clicks the pulsing start square in the centre. The planning clock starts here, so nobody plans for free and the mouse starts from the same spot every round.
3. **Plan:** three 6-step paths from the start, new random shapes every round, one each at low (≈0.4–0.55), mid (≈0.6–0.95) and high (≈1.0–1.2) turn-coded complexity in nats. Each stop hides a small value (±4/8). **One stop per path, at a random position, hides a big value (±24/48)**, so there's no "check the leaves" shortcut. Each click shows a red "−price" pop-up.
4. **Done:** the start square turns into a blue **done** square (after the first reveal, or 1 s after start). Clicking it ends planning.
5. **Choose:** pick a path by clicking any of its stops. In timed rounds, looking ends at the player's deadline, then there are 5 s to pick (no pick = "froze", scores only −click costs).
6. **Remember:** the maze disappears for 2.5 s.
7. **Walk:** reproduce the path with the arrow keys (or on-screen pad). A correct walk earns the path's reward minus click costs. A wrong step earns only the minus.

## Session structure
- **Practice (6 rounds):** 4 untimed, then 2 timed.
- **Per-player deadline:** 60% of the median planning time in the 4 untimed practice rounds, rounded to 0.5 s and kept within 5–15 s.
- **Real rounds (24):** 2 blocks of 12 (no limit vs. deadline, random order). Click price 2/4 is mixed within each block.
- **Matched pairs:** 10 maze problems appear once in each block (same paths, rewards and price, different rotation/mirror), plus 2 unpaired fillers per block. This compares the same problem with and without the deadline.
- About 15 minutes. A **demo mode** (3 rounds, nothing saved) is on the start screen.

## Data
Every finished round is auto-saved in the browser (localStorage) by player ID. The end screen and the "Saved data on this device" panel show the CSV to copy.

One CSV row per round. Key columns:
- **Design:** `player`, `session`, `version`, `round`, `block`, `problem_id`, `copy`, `rotation`, `mirrored`, `click_cost`, `deadline`, `deadline_ms`, `natural_plan_ms`
- **Mazes:** `reward_*`, `nats_*`, `acts_*` (S/L/R codes), `bigpos_*`, `node_values`, `path_cells`
- **Computation:** `n_clicks`, `clicks` (node, value, time), `leader_after_each_click`, `time_first_click_ms`, `inter_click_ms`, `start_wait_ms`, `planning_time_ms`, `choice_time_ms`, `timed_out`, `froze`
- **Choice and memory:** `chosen_path`, `chosen_nats`, `best_path`, `chose_best`, `walk_keys`, `walk_correct`, `first_error_step`
- **Attention:** `away_ms`, `away_events` (time the page lost focus, so distraction isn't counted as thinking)
- **Outcome:** `path_reward`, `paid_for_clicks`, `score`

## Model (`model/`)
- `agents.py`, `simulate.py`, `figure.py`: VOC agents (balanced, overthinker, under-thinker) simulated on the task with and without a deadline. Findings in [`model/README.md`](model/README.md), results in `summary.txt` and `deadline_effect.png`.
- `fit_pilot.py`: fits a player's stopping threshold *r* and choice precision *β* to their own click sequences by maximum likelihood.
  `python fit_pilot.py data.csv '[-8,-4,4,8]' '[-48,-24,24,48]'`

## Changelog
- **v2.8:** the centre start square becomes the **done** button once planning starts (after the first reveal, or 1 s after start, so a double-click can't skip a round). Side "done" button removed.
- **v2.7:** per-player deadline (see above) plus 2 timed practice rounds; logs `deadline_ms`, `natural_plan_ms`. Click prices 1/3 → 2/4 (simulation: at 1 pt, clicking almost everything is optimal, so over-clicking wasn't diagnostic). Demo mode.
- **v2.6:** click the start square to begin each round; logs `start_wait_ms`.
- **v2.5:** matched-pair problems across blocks; choice cap 3 s → 5 s; side-by-side layout.
- **v2.4:** choice cap in timed rounds (pilot: deliberation leaked into choice time); logs `froze`.
- **v2.3:** 3 s price card; deadline 7 s → 12 s; rewards doubled (pilot total was −64).
- **v2.2:** auto-save per player ID with saved-data panel.
- **v2.1:** red "−price" pop-up on every click (pilot: the price went unnoticed).
- **v2:** random big-value position; random 6-step paths with varied nats; deadline block; prices mixed within blocks; focus-loss logging; player ID.
- **v1:** fixed 3 shapes, big values always at the last stop, 2 cost blocks. Pilot issues: leaf-only shortcut, memory too easy, zigzag chunkable, order confound, distraction counted as thinking.

## Run
Open `index.html` in a browser, or serve it with GitHub Pages (Settings → Pages → Deploy from branch → `main` / root).

> Note: data from anyone other than the author needs human-subjects approval first.
