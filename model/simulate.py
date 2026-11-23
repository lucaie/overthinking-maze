import numpy as np, pandas as pd, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from agents import play, make_maze

# Only the ratio r = w / kappa matters (click while VOC > r * price), so cost blindness (w<1) and
# belief error (kappa>1) predict the same behaviour. Payoff-maximising threshold in this task: r ~ 0.5
# (myopic VOC under-rates a click), so r = 0.5 is the balanced benchmark.
AGENTS = {'Balanced (r=0.5)': dict(w=0.5, kappa=1), 'Overthinker (r=0.05)': dict(w=0.05, kappa=1),
          'Under-thinker (r=1.5)': dict(w=1.5, kappa=1)}
N, DL_FRAC = 3000, 0.6

def run(seed=1):
    rows = []
    for name, par in AGENTS.items():
        for price in (2, 4):
            rng = np.random.default_rng(seed)
            mazes = [make_maze(rng) for _ in range(N)]          # identical mazes in both conditions (matched pairs)
            free = [play(rng, price=price, maze=m, **par) for m in mazes]
            natural = np.mean([r['time'] for r in free])
            budget = max(1.0, DL_FRAC * natural)                # per-agent deadline, like the game
            dl = [play(rng, price=price, maze=m, budget=budget, **par) for m in mazes]
            for cond, res in (('none', free), ('deadline', dl)):
                for j, r in enumerate(res):
                    rows.append(dict(agent=name, price=price, deadline=cond, maze=j, budget=budget, **r))
    return pd.DataFrame(rows)

if __name__ == '__main__':
    df = run()
    df.to_csv(__file__.rsplit('/', 1)[0] + '/sim_results.csv', index=False)
    s = df.groupby(['agent', 'price', 'deadline']).agg(clicks=('clicks', 'mean'), payoff=('exp_payoff', 'mean'),
        best=('chose_best', 'mean'), same_gut=('same_as_gut', 'mean'), nats=('chosen_nats', 'mean')).round(2)
    print(s.to_string())
    piv = df.pivot_table(index=['agent', 'price', 'maze'], columns='deadline', values='choice')
    print('\nmatched pairs, same choice with vs without deadline:')
    print((piv['none'] == piv['deadline']).groupby(level=[0, 1]).mean().round(2).to_string())
