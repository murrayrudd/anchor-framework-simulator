"""
Reproduce Figures 1-7 of the paper from the four-stock (N/B) anchor framework.

Each function returns a matplotlib Figure and saves PNG + SVG to the working
directory. Run as a script to regenerate all figures:

    python generate_figures.py
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import replace

from anchor_framework import (
    FrameworkParameters, rho_star, phi_E, phi_Z,
    steady_state_N, steady_state_B, steady_state_I, steady_state_H,
    delta_N, baseline_stocks, simulate_dynamics,
)

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 10, 'axes.labelsize': 10, 'axes.titlesize': 10,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 8.5,
    'figure.dpi': 120, 'savefig.dpi': 300, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.linewidth': 0.8, 'lines.linewidth': 1.6,
})
GK = ['#1a1a1a', '#454545', '#7a7a7a', '#aeaeae']


def _save(fig, name):
    for ext in ('png', 'svg'):
        fig.savefig(f'{name}.{ext}', bbox_inches='tight')


def figure_1(p=None):
    """rho* vs v at four levels of deliberative capacity D."""
    p = p or FrameworkParameters()
    v = np.linspace(0.3, 6.0, 300)
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    for D, c, ls in zip([0.5, 1.0, 2.0, 4.0], GK, ['-', '--', '-.', ':']):
        ax.plot(v, [rho_star(x, D, p) for x in v], color=c, linestyle=ls, label=f'$D={D}$')
    ax.axhline(p.rho_0, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
    ax.annotate(r'$\rho_0$ baseline', xy=(5.9, p.rho_0), xytext=(5.9, p.rho_0 + 0.012),
                ha='right', fontsize=8, color='gray')
    ax.set_xlabel('Information velocity, $v$')
    ax.set_ylabel(r'Steady-state effective time preference, $\rho^*$')
    ax.legend(title='Deliberative capacity', frameon=False, loc='upper left')
    ax.set_xlim(0.3, 6.0); ax.set_ylim(0, max(rho_star(6, 0.5, p), 0.25) * 1.05)
    ax.grid(True, alpha=0.2)
    fig.tight_layout(); _save(fig, 'figure_1'); return fig


def figure_2(p=None):
    """Response to a velocity shock: four stocks (panel a) and rho* (panel b)."""
    p = p or FrameworkParameters()
    dt = 0.25; T = 120; n = int(T / dt); t = np.arange(n) * dt; ts = 30
    vA = np.where(t < ts, 1.0, 3.0); DA = np.full(n, 1.0)
    vB = vA.copy(); DB = np.where(t < ts, 1.0, 2.5)
    N0, B0, I0, H0 = baseline_stocks(1, 1, p)
    A = simulate_dynamics(vA, DA, N0, B0, I0, H0, p, dt)
    Bsc = simulate_dynamics(vB, DB, N0, B0, I0, H0, p, dt)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 7.0),
                                   gridspec_kw={'height_ratios': [1, 1], 'hspace': 0.62})
    ax1.plot(t, A['N'] / N0, color=GK[0], label='Physical stock $N$')
    ax1.plot(t, A['B'] / B0, color=GK[1], ls='--', label='Biophysical reference $B$')
    ax1.plot(t, A['I'] / I0, color=GK[2], ls='-.', label='Institutional $I$')
    ax1.plot(t, A['H'] / H0, color=GK[3], ls=':', label='Historical $H$')
    ax1.axvline(ts, color='gray', lw=0.6, alpha=0.5)
    ax1.set_xlabel('Time'); ax1.set_ylabel('Stock (fraction of baseline)')
    ax1.set_xlim(0, T); ax1.set_ylim(0, 1.05)
    ax1.set_title('(a) Anchor stocks, no deliberative response', fontsize=9, loc='left')
    ax1.legend(frameon=False, ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.20))
    ax2.plot(t, A['rho_eff'], color=GK[0], label='No response ($D=1$)')
    ax2.plot(t, Bsc['rho_eff'], color=GK[1], ls='--', label='Compensating response ($D\\to2.5$)')
    ax2.axvline(ts, color='gray', lw=0.6, alpha=0.5)
    ax2.set_xlabel('Time'); ax2.set_ylabel(r'Effective time preference $\rho^*$')
    ax2.set_xlim(0, T); ax2.set_ylim(0, 0.05)
    ax2.set_title('(b) Effective time preference', fontsize=9, loc='left')
    ax2.legend(frameon=False, ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.20))
    _save(fig, 'figure_2'); return fig


def figure_3(p=None):
    """rho* vs v under four values of the physical depreciation convexity alpha_N."""
    p = p or FrameworkParameters()
    v = np.linspace(0.3, 5.0, 300)
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    for aN, c, ls in zip([1.0, 1.5, 2.0, 2.5], GK[::-1], [':', '-.', '--', '-']):
        pp = replace(p, alpha_N=aN)
        ax.plot(v, [rho_star(x, 1.0, pp) for x in v], color=c, linestyle=ls,
                label=fr'$\alpha_N={aN:.1f}$')
    ax.axhline(p.rho_0, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
    ax.annotate(r'$\rho_0$ baseline', xy=(4.85, p.rho_0), xytext=(4.85, p.rho_0 + 0.018),
                ha='right', fontsize=8, color='gray')
    ax.set_xlabel('Information velocity, $v$')
    ax.set_ylabel(r'Steady-state effective time preference, $\rho^*$')
    ax.legend(title='Physical depreciation convexity', frameon=False, loc='upper left')
    ax.set_xlim(0.3, 5.0); ax.set_ylim(0, max(rho_star(5, 1, replace(p, alpha_N=2.5)), 0.3) * 1.05)
    ax.grid(True, alpha=0.2)
    fig.tight_layout(); _save(fig, 'figure_3'); return fig


def figure_4(p=None):
    """Asymmetric recovery: N and B under a symmetric velocity pulse."""
    p = p or FrameworkParameters()
    dt = 0.25; T = 140; n = int(T / dt); t = np.arange(n) * dt
    v = np.ones(n); v[(t >= 10) & (t < 40)] = 4.5; D = np.ones(n)
    N0, B0, I0, H0 = baseline_stocks(1, 1, p)
    s = simulate_dynamics(v, D, N0, B0, I0, H0, p, dt)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    rec = t >= 40
    ax.fill_between(t[rec], s['N'][rec] / N0, 1.0, color=GK[3], alpha=0.20, lw=0,
                    label='recovery deficit, $N$')
    ax.plot(t, s['N'] / N0, color=GK[0], lw=1.9, label='Physical stock $N$ (slow recovery)')
    ax.plot(t, s['B'] / B0, color=GK[1], lw=1.6, ls='--', label='Biophysical reference $B$ (tracks $N$)')
    ax.axhline(1.0, color=GK[2], lw=0.9, ls=':', label='Undisturbed baseline')
    ax.set_xlabel('Time'); ax.set_ylabel('Stock (fraction of baseline)')
    ax.set_xlim(0, T); ax.set_ylim(0, 1.08)
    ax2 = ax.twinx(); ax2.plot(t, v, color=GK[2], lw=1.0, alpha=0.8)
    ax2.set_ylabel('Information velocity, $v$', color=GK[2]); ax2.set_ylim(0, 5.2)
    ax2.tick_params(axis='y', colors=GK[2])
    ax2.spines['right'].set_visible(True); ax2.spines['top'].set_visible(False)
    ax.text(24, 0.74, 'fast depletion', fontsize=8.5, ha='center', style='italic')
    ax.text(98, 0.50, 'slow recovery of $N$', fontsize=8.5, ha='center', style='italic')
    ax.legend(frameon=False, ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.16))
    fig.subplots_adjust(bottom=0.26, top=0.97, left=0.11, right=0.89)
    _save(fig, 'figure_4'); return fig


def figure_5(p=None):
    """Existence-channel multiplier phi_E over (B, I) at H = 2.0."""
    p = p or FrameworkParameters()
    B = np.linspace(1, 30, 200); I = np.linspace(0.5, 6, 200)
    BB, II = np.meshgrid(B, I)
    Z = phi_E(BB, II, 2.0, p)
    fig, ax = plt.subplots(figsize=(6.0, 4.4))
    levels = np.linspace(Z.min(), np.percentile(Z, 95), 12)
    cf = ax.contourf(BB, II, Z, levels=levels, cmap='Greys')
    cs = ax.contour(BB, II, Z, levels=[0.15, 0.20, 0.30, 0.50], colors='black', linewidths=0.7)
    ax.clabel(cs, fmt='%.2f', fontsize=7)
    fig.colorbar(cf, ax=ax, label=r'Existence multiplier $\phi_E$ (lower = weaker discounting)')
    ax.set_xlabel('Biophysical reference stock, $B$')
    ax.set_ylabel('Institutional stock, $I$')
    fig.tight_layout(); _save(fig, 'figure_5'); return fig


def figure_6(p=None):
    """rho vs biophysical stock B under three configurations of complementary stocks."""
    p = p or FrameworkParameters()
    B = np.linspace(0.5, 30, 300); pz = phi_Z(1.5, 1.0, p)
    cfgs = [('Degraded $I$, $H$ ($I=H=0.5$)', 0.5, 0.5, GK[0], '-'),
            ('Moderate $I$, $H$ ($I=2.0$, $H=1.5$)', 2.0, 1.5, GK[1], '--'),
            ('Robust $I$, $H$ ($I=4.0$, $H=2.5$)', 4.0, 2.5, GK[2], '-.')]
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    for lab, Iv, Hv, c, ls in cfgs:
        ax.plot(B, [p.rho_0 * phi_E(b, Iv, Hv, p) * pz for b in B], color=c, linestyle=ls, label=lab)
    ax.axhline(p.rho_0, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
    ax.annotate(r'$\rho_0$ baseline', xy=(28, p.rho_0), xytext=(28, p.rho_0 + 0.003),
                ha='right', fontsize=8, color='gray')
    ax.set_xlabel('Biophysical reference stock, $B$')
    ax.set_ylabel(r'Effective time preference, $\rho$')
    ax.set_xlim(0.5, 30); ax.set_ylim(0, 0.08); ax.grid(True, alpha=0.2)
    ax.legend(frameon=False, loc='upper right', fontsize=8.5)
    fig.tight_layout(); _save(fig, 'figure_6'); return fig


def figure_7(p=None):
    """Iso-rho* contours on the (v, D) plane (the offset condition)."""
    p = p or FrameworkParameters()
    v = np.linspace(0.5, 5.0, 220); D = np.linspace(0.2, 5.0, 220)
    VV, DD = np.meshgrid(v, D)
    Z = np.vectorize(lambda x, y: rho_star(x, y, p))(VV, DD)
    fig, ax = plt.subplots(figsize=(6.0, 4.4))
    levels = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16]
    cs = ax.contour(VV, DD, Z, levels=levels, colors='black', linewidths=0.9)
    ax.clabel(cs, fmt=r'$\rho^*=%.3f$', fontsize=7)
    ax.set_xlabel('Information velocity, $v$')
    ax.set_ylabel('Deliberative capacity, $D$')
    ax.set_xlim(0.5, 5.0); ax.set_ylim(0.2, 5.0)
    fig.tight_layout(); _save(fig, 'figure_7'); return fig


def main():
    for fn in (figure_1, figure_2, figure_3, figure_4, figure_5, figure_6, figure_7):
        fn(); plt.close('all')
        print(f"saved {fn.__name__}")


if __name__ == "__main__":
    main()
