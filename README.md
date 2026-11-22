# overthinking-maze

A small browser task for studying **overthinking as deliberation beyond the value of computation**. It's part of a COGS 188D final project (Option 3, Project B: policy compression, Prof. Lucy Lai, UCSD, fall 2026).

The design is Mouselab-MDP style (Callaway, Lieder, Krueger & Griffiths, 2017) with an added **memory phase**, so one task measures both cognitive costs:

- **Computation:** clicks that reveal hidden rewards (each click costs points), plus planning time.
- **Policy complexity (memory):** the chosen path must be walked from memory. Its cost is the turn-coded policy complexity *I(S;A)* in nats.

## One round
1. **Plan:** three equal-length paths (straight = 0 nats, one turn ≈ 0.56, zigzag ≈ 1.04) with hidden rewards. Click stops to reveal them.
2. **Choose:** pick a path.
3. **Remember:** the maze disappears for 2 s.
4. **Walk:** reproduce the path with the arrow keys. A correct walk earns the path's reward minus click costs. A wrong turn earns only the minus.

There are 2 practice rounds, then 2 blocks of 8 rounds with a cheap (1 pt) or expensive (3 pt) click price, in random order. Layouts are rotated and mirrored each round.

## Data
At the end, the page shows one CSV row per round to copy. Key columns:
`click_cost`, `n_clicks`, `clicks` (node, value, time), `leader_after_each_click`, `inter_click_ms`, `planning_time_ms`, `chosen_path`, `chosen_nats`, `best_path`, `walk_keys`, `walk_correct`, `first_error_step`, `score`.

## Run
Open `index.html` in a browser, or serve it with GitHub Pages (Settings → Pages → Deploy from branch → `main` / root).

> Note: data from anyone other than the author needs human-subjects approval first.
