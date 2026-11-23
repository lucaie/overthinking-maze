"""Overthinking-maze model, v1 (search side).

Each round: 3 paths x 6 stops. Each stop hides a small value (+-4/8); one stop per
path, at a random position, hides a big value (+-24/48). Paths differ in turn-coded
policy complexity I (nats). A path is walked from memory afterwards: correct with
probability p(I), which falls with I. Payoff = p(I) * path reward - price * clicks.

Agent: reveals stops one at a time. Before each reveal it computes the myopic value
of computation (VOC) of every unrevealed stop: how much one reveal is expected to
raise the value of the path it would choose. It clicks while
    kappa * max VOC > w * price      and time is left,
then chooses with softmax(beta * U), U_k = p(I_k) * estimated reward_k.
  balanced      w=1,   kappa=1
  cost-blind    w<1    (feels only part of the cost of thinking)
  belief error  kappa>1 (over-values thinking);  kappa<1 = under-thinker
Time: each click takes tau seconds; a deadline is a time budget, never a click cap.
"""
import numpy as np

SMALL = np.array([-8, -4, 4, 8]); BIG = np.array([-48, -24, 24, 48])
NATS = {'low': [0.451], 'mid': [0.637, 0.868], 'high': [1.011, 1.099]}
STEPS = 6

def p_correct(I, a=5.0, b=3.0):
    """Walk accuracy vs complexity (a, b set so ~97% at 0.45 nats, ~86% at 1.05; pilots: 100% vs 84-92%)."""
    return 1 / (1 + np.exp(-(a - b * I)))

def make_maze(rng):
    nats = np.array([rng.choice(NATS[k]) for k in ('low', 'mid', 'high')])
    vals = rng.choice(SMALL, size=(3, STEPS))
    big_at = rng.integers(0, STEPS, size=3)
    vals[np.arange(3), big_at] = rng.choice(BIG, size=3)
    return vals, nats, big_at

def path_values(known_sum, p):
    return p * known_sum                       # unrevealed stops have expected value 0

def vocs(revealed, vals_known, big_found, p):
    """Myopic VOC of revealing each unrevealed stop."""
    known_sum = (vals_known * revealed).sum(1)
    U = path_values(known_sum, p); base = U.max()
    out = np.full((3, STEPS), -np.inf)
    for k in range(3):
        unrev = np.where(~revealed[k])[0]
        if len(unrev) == 0: continue
        pbig = 0.0 if big_found[k] else 1.0 / len(unrev)
        others = np.delete(U, k).max()
        ev = 0.0
        for v_set, pw in ((BIG, pbig), (SMALL, 1 - pbig)):
            if pw == 0: continue
            newU = p[k] * (known_sum[k] + v_set)
            ev += pw * np.maximum(newU, others).mean()
        out[k, unrev] = ev - base               # same value for every unrevealed stop on a path
    return out

def play(rng, w=1.0, kappa=1.0, beta=0.3, price=2, budget=np.inf, tau=1.0, maze=None, r_bal=0.5):
    vals, nats, big_at = maze if maze is not None else make_maze(rng)
    p = p_correct(nats)
    revealed = np.zeros((3, STEPS), bool); big_found = np.zeros(3, bool)
    clicks = 0; t = 0.0; gut = None
    while t + tau <= budget:
        V = vocs(revealed, vals, big_found, p)
        best = V.max()
        if best == -np.inf: break
        if gut is None and not (best > r_bal * price):  # where the balanced agent would stop
            gut = int(np.argmax(path_values((vals * revealed).sum(1), p)))
        if not (kappa * best > w * price): break
        k, i = np.unravel_index(np.argmax(V + rng.random(V.shape) * 1e-6), V.shape)
        revealed[k, i] = True; big_found[k] |= (i == big_at[k]); clicks += 1; t += tau
    U = path_values((vals * revealed).sum(1), p)
    if gut is None: gut = int(np.argmax(U))
    pr = np.exp(beta * (U - U.max())); pr /= pr.sum()
    choice = rng.choice(3, p=pr)
    true_U = p * vals.sum(1)
    return dict(clicks=clicks, time=t, choice=choice, gut=gut, same_as_gut=choice == gut,
                chose_best=choice == int(np.argmax(true_U)), chosen_nats=nats[choice],
                exp_payoff=true_U[choice] - price * clicks)
