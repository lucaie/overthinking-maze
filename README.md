# overthinking-maze

A small browser task for studying **overthinking as deliberation beyond the value of computation**. It's part of a COGS 188D final project (Option 3, Project B: policy compression, Prof. Lucy Lai, UCSD, fall 2026).

The design is Mouselab-MDP style (Callaway, Lieder, Krueger & Griffiths, 2017) with an added **memory phase**, so one task measures both cognitive costs:

- **Computation:** clicks that reveal hidden rewards (each click costs points), plus planning time.
- **Policy complexity (memory):** the chosen path must be walked from memory. Its cost is the turn-coded policy complexity *I(S;A)* in nats.

## One round (v2)
1. **Plan:** three 6-step paths from the start, with new random shapes every round, one each at low (≈0.45), mid (≈0.6–0.9) and high (≈1.0+) turn-coded complexity in nats. Each stop hides a small value (±4/8). **One stop per path, at a random position, hides a big value (±24/48)**, so there's no "check the leaves" shortcut.
2. **Choose:** pick a path. In deadline rounds, looking ends after 12 s (the timer starts after a 3 s price card).
3. **Remember:** the maze disappears for 2.5 s.
4. **Walk:** reproduce the path with the arrow keys. A correct walk earns the path's reward minus click costs. A wrong step earns only the minus.

Structure: 4 practice rounds, then 2 blocks of 12 (no limit vs. 12 s limit, random order). The click price (1 or 3 pt) is mixed within each block, which avoids order and learning confounds.

## Data
One CSV row per round (copy at the end). Key columns: `player`, `click_cost`, `deadline`, `timed_out`, `nats_*`, `acts_*` (S/L/R codes), `bigpos_*`, `n_clicks`, `clicks` (node, value, time), `leader_after_each_click`, `inter_click_ms`, `planning_time_ms`, `chosen_path`, `chosen_nats`, `best_path`, `walk_keys`, `walk_correct`, `first_error_step`, `away_ms` / `away_events` (time the page lost focus, so distraction isn't counted as thinking), `score`.

## Changelog
- **v2.3:** 3 s price card before each round (the 12 s timer starts after it); deadline 7 s → 12 s (7 s ran out every round); rewards doubled (small ±4/8, big ±24/48), so clicks are relatively cheaper (pilot total was −64).
- **v2.2:** every round auto-saved in the browser (localStorage), by player ID and session; "Saved data on this device" panel on the start and end screens to show, copy or delete each ID's data.
- **v2.1:** red "−price" pop-up on every click (pilot: the click price went unnoticed).
- **v2:** random big-value position; random 6-step paths with varied nats; deadline block; click price mixed within blocks; focus-loss logging; player ID.
- **v1:** fixed 3 shapes (straight / one turn / zigzag), big values always at the last stop, 2 cost blocks. Pilot issues: leaf-only shortcut, memory too easy, zigzag chunkable as alternation, order confound, pauses that were really distraction.

## Run
Open `index.html` in a browser, or serve it with GitHub Pages (Settings → Pages → Deploy from branch → `main` / root).

> Note: data from anyone other than the author needs human-subjects approval first.
