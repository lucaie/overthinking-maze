"""Fit the stopping threshold r (and choice precision beta) to a player's own click sequences.

At every decision point the model sees exactly what the player had revealed. It continues with
P(click) = sigmoid((max VOC - r * price) / s); the round's last decision is a stop (left out when
the deadline ended the round). Choice: softmax(beta * U) over p(I) * revealed reward.
Maximum likelihood over r, s (stopping) and beta (choice).
"""
import json, sys, numpy as np, pandas as pd
from scipy.optimize import minimize
from agents import p_correct

def vocs(revealed, vals, big_found, p, SMALL, BIG):
    ks = (vals * revealed).sum(1); U = p * ks; base = U.max(); out = []
    for k in range(3):
        n = (~revealed[k]).sum()
        if n == 0: out.append(-np.inf); continue
        pb = 0.0 if big_found[k] else 1.0 / n; oth = np.delete(U, k).max(); ev = 0
        for vs, pw in ((BIG, pb), (SMALL, 1 - pb)):
            if pw: ev += pw * np.maximum(p[k] * (ks[k] + vs), oth).mean()
        out.append(ev - base)
    return max(out), U

def decisions(df, SMALL, BIG):
    stop_rows, choice_rows = [], []
    L = ['low', 'mid', 'high']
    for _, r in df.iterrows():
        vals = np.array([json.loads(r.node_values)[k] for k in L], float)
        p = p_correct(np.array([r[f'nats_{k}'] for k in L]))
        bigpos = np.array([int(r[f'bigpos_{k}']) - 1 for k in L])
        rev = np.zeros((3, 6), bool); bf = np.zeros(3, bool)
        for c in json.loads(r.clicks):
            v, _ = vocs(rev, vals, bf, p, SMALL, BIG); stop_rows.append((v, r.click_cost, 1))
            k = L.index(''.join(ch for ch in c['node'] if ch.isalpha())); i = int(c['node'][-1]) - 1
            rev[k, i] = True; bf[k] |= (i == bigpos[k])
        v, U = vocs(rev, vals, bf, p, SMALL, BIG)
        if not bool(r.get('timed_out', False)): stop_rows.append((v, r.click_cost, 0))
        if isinstance(r.chosen_path, str) and r.chosen_path in L: choice_rows.append((U, L.index(r.chosen_path)))
    return np.array([(a, b, c) for a, b, c in stop_rows if np.isfinite(a)]), choice_rows

def fit(stop, choice):
    v, price, y = stop.T
    def nll_stop(th):
        r, ls = th; z = (v - r * price) / np.exp(ls); pc = 1 / (1 + np.exp(-z))
        return -np.sum(y * np.log(pc + 1e-9) + (1 - y) * np.log(1 - pc + 1e-9))
    best = min((minimize(nll_stop, [r0, 0.5], method='Nelder-Mead') for r0 in (0.1, 0.5, 1, 2)), key=lambda o: o.fun)
    def nll_choice(b):
        return -sum(b[0] * U[c] - np.log(np.exp(b[0] * (U - U.max())).sum()) - b[0] * U.max() for U, c in choice)
    bc = minimize(nll_choice, [0.2], method='Nelder-Mead')
    return dict(r=best.x[0], noise_s=np.exp(best.x[1]), beta=bc.x[0], n_decisions=len(y), n_choices=len(choice))

if __name__ == '__main__':
    path = sys.argv[1]; small = json.loads(sys.argv[2]); big = json.loads(sys.argv[3])
    d = pd.read_csv(path); d = d[d.block != 'practice']
    stop, choice = decisions(d, np.array(small), np.array(big))
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in fit(stop, choice).items()})
