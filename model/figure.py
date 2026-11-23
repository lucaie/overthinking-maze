import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
df = pd.read_csv(__file__.rsplit('/', 1)[0] + '/sim_results.csv')
m = df.groupby(['agent', 'price', 'deadline']).exp_payoff.mean().unstack('deadline')
d = (m['deadline'] - m['none']).unstack('price')
order = ['Overthinker (r=0.05)', 'Balanced (r=0.5)', 'Under-thinker (r=1.5)']
labels = ['Overthinker', 'Balanced', 'Under-thinker']
d = d.loc[order]
BG, INK, SOFT = '#FAF7F0', '#2B1E16', '#5A4B40'; C = {2: '#A86A1F', 4: '#2E7DB8'}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 15})
fig, ax = plt.subplots(figsize=(12, 6.2), dpi=150); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
x = np.arange(3); wd = 0.34
for j, price in enumerate((2, 4)):
    xs = x + (j - 0.5) * (wd + 0.02)
    ax.bar(xs, d[price], wd, color=C[price], label=f'Click price {price} pts', zorder=3)
    for xi, v in zip(xs, d[price]):
        ax.text(xi, v + (0.4 if v >= 0 else -0.4), f'{v:+.1f}', ha='center', va='bottom' if v >= 0 else 'top', color=INK, fontsize=14)
ax.axhline(0, color=SOFT, lw=1, zorder=2); ax.set_ylim(-12.5, 3)
ax.set_xticks(x, labels, color=INK, fontsize=16)
ax.set_ylabel('Change in points per round\nwith a deadline (vs. none)', color=SOFT)
ax.yaxis.grid(True, color='#E4DCCF', lw=1, zorder=0); ax.set_axisbelow(True)
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.spines['bottom'].set_visible(False); ax.tick_params(colors=SOFT, length=0)
ax.legend(frameon=False, loc='lower left', fontsize=14, labelcolor=INK)
ax.set_title('A deadline costs the overthinker least, and at a high click price it helps',
             loc='left', color=INK, fontsize=18, pad=16)
fig.text(0.01, 0.01, 'Simulated agents, 3,000 matched mazes per condition. Deadline = 60% of each agent’s own planning time; 1 s per click.',
         color=SOFT, fontsize=11)
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(__file__.rsplit('/', 1)[0] + '/deadline_effect.png', facecolor=BG)
print(d.round(2))
