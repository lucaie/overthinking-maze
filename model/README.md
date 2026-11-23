# Model v1: search-side overthinking agents

`agents.py`: one round of the maze task (3 paths × 6 stops, small ±4/8 values, one big ±24/48 per path at a random position; walk accuracy p(I) falls with turn-coded nats). The agent reveals stops while `kappa · VOC > w · price` (myopic value of computation) and time is left, then chooses with softmax over p(I) × estimated reward.

`simulate.py`: balanced, overthinking and under-thinking agents × price 2/4 × no deadline / per-agent deadline (60% of its own planning time), on 3,000 matched mazes. `figure.py` → `deadline_effect.png`.

## v1 findings
- **Only the ratio r = w/κ matters**, so cost blindness and belief error predict identical behaviour: they can't be told apart from choices and clicks with this rule.
- **The payoff-maximising threshold is r ≈ 0.5**, not 1: myopic VOC under-rates a click (one reveal rarely flips the choice, several together can). Overthinking is therefore defined against r ≈ 0.5.
- **The overthinker (r = 0.05)** clicks ~8 times vs ~5–6, picks the best path more often (88% vs 70–76%) but earns less at price 4 (−2.3 vs +3.8 points).
- **The deadline costs the overthinker least**, and at price 4 it *raises* its payoff (+1.3), while the balanced agent loses 5–10 points.
- **Chosen path complexity is unchanged** (~0.72–0.75 nats for every agent), so in this model overthinking is wasted computation, not inflated policy complexity.
