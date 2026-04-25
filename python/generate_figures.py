"""
Generate all seven figures for the institutional anchor framework paper.

Figure 1: Headline rho* vs v at multiple D values
Figure 2: Stock dynamics under a velocity shock (4-panel)
Figure 3: Convexity of biophysical depreciation
Figure 4: Hysteresis in biophysical stock recovery
Figure 5: phi_E surface across B and I
Figure 6: B investment cannot offset degraded I and H
Figure 7: Offset-condition iso-rho* contours

Figures 1, 2 retain the originally published structure.
Figures 3, 4 are split from a combined two-panel figure in earlier drafts.
Figures 5, 6 are split from a combined two-panel figure in earlier drafts.
Figure 7 is the offset-condition figure (single panel throughout).
"""

from dataclasses import replace
import numpy as np
import matplotlib.pyplot as plt

from anchor_framework import (
    FrameworkParameters,
    rho_star,
    simulate_dynamics,
    steady_state_B,
    steady_state_I,
    steady_state_H,
    phi_E,
    phi_Z,
)

# Publication style: clean grayscale, minimal embellishment
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 120,
    'savefig.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'grid.linewidth': 0.4,
    'grid.alpha': 0.3,
    'lines.linewidth': 1.5,
})

# Standard grayscale palette used throughout
GRAY_DARKEST = '#1a1a1a'
GRAY_DARK = '#505050'
GRAY_MED = '#808080'
GRAY_LIGHT = '#b0b0b0'


# =====================================================================
# Figure 1: rho* as a function of v at four levels of D
# =====================================================================
def figure_1_headline(p: FrameworkParameters, save_path: str = None):
    v_range = np.linspace(0.3, 6.0, 200)
    D_values = [0.5, 1.0, 2.0, 4.0]
    grays = [GRAY_DARKEST, GRAY_DARK, GRAY_MED, GRAY_LIGHT]
    linestyles = ['-', '--', '-.', ':']

    fig, ax = plt.subplots(figsize=(6.0, 4.2))

    for D, gray, ls in zip(D_values, grays, linestyles):
        rhos = [rho_star(v, D, p) for v in v_range]
        ax.plot(v_range, rhos, color=gray, linestyle=ls, label=f'D = {D:.1f}')

    ax.set_xlabel('Information velocity, $v$')
    ax.set_ylabel(r'Steady-state effective time preference, $\rho^*$')
    ax.legend(title='Deliberative capacity', frameon=False, loc='upper left')
    ax.grid(True, which='both', linestyle='-', alpha=0.2)
    ax.set_ylim(0, 0.25)
    ax.set_xlim(v_range.min(), v_range.max())

    ax.axhline(y=p.rho_0, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
    ax.annotate(r'$\rho_0$ baseline', xy=(v_range.max() * 0.95, p.rho_0),
                xytext=(v_range.max() * 0.95, p.rho_0 + 0.008),
                ha='right', fontsize=8, color='gray')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


# =====================================================================
# Figure 2: Stock dynamics under a velocity shock (4-panel)
# =====================================================================
def figure_2_dynamics(p: FrameworkParameters, save_path: str = None):
    T = 150
    dt = 0.5
    t_shock = 60  # shock at index 60 (time = 30)

    v_init, D_init = 1.0, 1.0
    B_0 = steady_state_B(v_init, D_init, p)
    I_0 = steady_state_I(v_init, D_init, p)
    H_0 = steady_state_H(v_init, D_init, p)

    v_A = np.concatenate([np.full(t_shock, v_init), np.full(T - t_shock, 3.0)])
    D_A = np.full(T, D_init)
    v_B = np.concatenate([np.full(t_shock, v_init), np.full(T - t_shock, 3.0)])
    D_B = np.concatenate([np.full(t_shock, D_init), np.full(T - t_shock, 2.5)])

    sim_A = simulate_dynamics(v_A, D_A, B_0, I_0, H_0, p, dt=dt)
    sim_B = simulate_dynamics(v_B, D_B, B_0, I_0, H_0, p, dt=dt)

    fig, axes = plt.subplots(2, 2, figsize=(8.5, 6.0), sharex=True)
    time = sim_A['time']

    color_A = GRAY_DARKEST
    color_B = GRAY_DARK

    panels = [
        (axes[0, 0], 'B', 'Biophysical stock, $B$', '(a) Biophysical anchor stock'),
        (axes[0, 1], 'I', 'Institutional stock, $I$', '(b) Institutional commitment devices'),
        (axes[1, 0], 'H', 'Historical stock, $H$', '(c) Historical reference infrastructure'),
        (axes[1, 1], 'rho_eff', r'Effective time preference, $\rho$', r'(d) Effective time preference'),
    ]
    for ax, key, ylabel, title in panels:
        ax.plot(time, sim_A[key], color=color_A, linestyle='-',
                label='No deliberative response' if key == 'B' else None)
        ax.plot(time, sim_B[key], color=color_B, linestyle='--',
                label='Compensating response' if key == 'B' else None)
        ax.axvline(x=t_shock * dt, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc='left', fontsize=10)
        ax.grid(True, alpha=0.2)
        if key == 'B':
            ax.legend(frameon=False, fontsize=8, loc='upper right')

    axes[1, 0].set_xlabel('Time')
    axes[1, 1].set_xlabel('Time')

    axes[0, 0].annotate('velocity\nshock', xy=(t_shock * dt, 8),
                        xytext=(t_shock * dt - 8, 6),
                        fontsize=8, color='gray', ha='right',
                        arrowprops=dict(arrowstyle='->', color='gray', lw=0.6))

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


# =====================================================================
# Figure 3: Convexity of biophysical depreciation
# =====================================================================
def figure_3_convexity(p_base: FrameworkParameters, save_path: str = None):
    v_range = np.linspace(0.3, 5.0, 250)
    alpha_B_values = [1.0, 1.5, 2.0, 2.5]
    grays = [GRAY_LIGHT, GRAY_MED, GRAY_DARK, GRAY_DARKEST]
    linestyles = [':', '-.', '--', '-']

    fig, ax = plt.subplots(figsize=(6.0, 4.2))

    for alpha_B, gray, ls in zip(alpha_B_values, grays, linestyles):
        p = replace(p_base, alpha_B=alpha_B)
        rhos = [rho_star(v, 1.0, p) for v in v_range]
        ax.plot(v_range, rhos, color=gray, linestyle=ls,
                label=fr'$\alpha_B = {alpha_B:.1f}$')

    ax.set_xlabel('Information velocity, $v$')
    ax.set_ylabel(r'Steady-state effective time preference, $\rho^*$')
    ax.legend(title=r'Depreciation convexity', frameon=False, loc='upper left')
    ax.grid(True, alpha=0.2)
    ax.set_ylim(0, 0.35)
    ax.set_xlim(v_range.min(), v_range.max())

    ax.axhline(y=p_base.rho_0, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
    ax.annotate(r'$\rho_0$ baseline', xy=(v_range.max() * 0.97, p_base.rho_0),
                xytext=(v_range.max() * 0.97, p_base.rho_0 + 0.012),
                ha='right', fontsize=8, color='gray')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


# =====================================================================
# Figure 4: Hysteresis in biophysical stock recovery
# =====================================================================
def figure_4_hysteresis(p: FrameworkParameters, save_path: str = None):
    dt = 0.25
    T_up = 200
    T_hold = 80
    T_down = 200
    T = T_up + T_hold + T_down

    v_min, v_max = 1.0, 4.5

    v_schedule = np.concatenate([
        np.linspace(v_min, v_max, T_up),
        np.full(T_hold, v_max),
        np.linspace(v_max, v_min, T_down),
    ])
    D_schedule = np.full(T, 1.0)

    B_0 = steady_state_B(v_min, 1.0, p)
    I_0 = steady_state_I(v_min, 1.0, p)
    H_0 = steady_state_H(v_min, 1.0, p)

    sim = simulate_dynamics(v_schedule, D_schedule, B_0, I_0, H_0, p, dt=dt)

    v_smooth = np.linspace(v_min, v_max, 100)
    B_ss_smooth = [steady_state_B(v, 1.0, p) for v in v_smooth]

    B_rising = sim['B'][:T_up + T_hold]
    v_rising = v_schedule[:T_up + T_hold]
    B_falling = sim['B'][T_up + T_hold:]
    v_falling = v_schedule[T_up + T_hold:]

    fig, ax = plt.subplots(figsize=(6.0, 4.5))

    ax.plot(v_smooth, B_ss_smooth, color=GRAY_LIGHT, linestyle=':',
            linewidth=1.0, label='Steady-state locus')
    ax.plot(v_rising, B_rising, color=GRAY_DARKEST, linestyle='-',
            label='Depletion path ($v$ rising)')
    ax.plot(v_falling, B_falling, color=GRAY_DARK, linestyle='--',
            label='Recovery path ($v$ falling)')

    # Direction arrows
    idx_up = len(v_rising) // 3
    ax.annotate('', xy=(v_rising[idx_up + 5], B_rising[idx_up + 5]),
                xytext=(v_rising[idx_up], B_rising[idx_up]),
                arrowprops=dict(arrowstyle='->', color=GRAY_DARKEST, lw=1.2))
    idx_down = len(v_falling) // 3
    ax.annotate('', xy=(v_falling[idx_down + 5], B_falling[idx_down + 5]),
                xytext=(v_falling[idx_down], B_falling[idx_down]),
                arrowprops=dict(arrowstyle='->', color=GRAY_DARK, lw=1.2))

    ax.set_xlabel('Information velocity, $v$')
    ax.set_ylabel('Biophysical anchor stock, $B$')
    ax.legend(frameon=False, loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


# =====================================================================
# Figure 5: phi_E surface across B and I (with H fixed)
# =====================================================================
def figure_5_phi_E_surface(p: FrameworkParameters, save_path: str = None):
    B_range = np.linspace(0.5, 20.0, 100)
    I_range = np.linspace(0.5, 5.0, 100)
    B_grid, I_grid = np.meshgrid(B_range, I_range)
    H_fixed = 2.0

    Phi = np.zeros_like(B_grid)
    for i in range(B_grid.shape[0]):
        for j in range(B_grid.shape[1]):
            Phi[i, j] = phi_E(B_grid[i, j], I_grid[i, j], H_fixed, p)

    fig, ax = plt.subplots(figsize=(6.5, 4.8))

    # Standard grayscale: high values dark
    levels_fill = np.linspace(0, np.percentile(Phi, 95), 20)
    cs_fill = ax.contourf(B_grid, I_grid, np.clip(Phi, 0, levels_fill[-1]),
                          levels=levels_fill, cmap='Greys')

    contour_levels = [0.15, 0.20, 0.30, 0.50]
    cs = ax.contour(B_grid, I_grid, Phi, levels=contour_levels,
                    colors='black', linewidths=1.0)
    ax.clabel(cs, inline=True, fontsize=8, fmt='%.2f', inline_spacing=4)

    cbar = fig.colorbar(cs_fill, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label(r'Existence channel, $\phi_E$' + '\n(higher = stronger discounting)',
                   fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    ax.annotate('Both stocks low:\nstrong discounting',
                xy=(2.0, 1.0), xytext=(1.0, 0.7),
                fontsize=8, color='black', ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='none', alpha=0.85))
    ax.annotate('Both stocks high:\nweak discounting',
                xy=(17.0, 4.5), xytext=(13.0, 4.5),
                fontsize=8, color='black', ha='left',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='none', alpha=0.85))

    ax.set_xlabel(r'Biophysical stock, $B$')
    ax.set_ylabel(r'Institutional stock, $I$')
    ax.grid(True, alpha=0.2)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


# =====================================================================
# Figure 6: B investment cannot offset degraded I and H
# =====================================================================
def figure_6_complementarity(p: FrameworkParameters, save_path: str = None):
    B_range = np.linspace(0.5, 30.0, 200)

    scenarios = [
        {'I': 0.5, 'H': 0.5, 'label': r'Degraded $I$, $H$ ($I = H = 0.5$)',
         'color': GRAY_DARKEST, 'ls': '-'},
        {'I': 2.0, 'H': 1.5, 'label': r'Moderate $I$, $H$ ($I = 2.0$, $H = 1.5$)',
         'color': GRAY_DARK, 'ls': '--'},
        {'I': 4.0, 'H': 2.5, 'label': r'Robust $I$, $H$ ($I = 4.0$, $H = 2.5$)',
         'color': GRAY_MED, 'ls': '-.'},
    ]

    v_fixed, D_fixed = 1.5, 1.0
    pz = phi_Z(v_fixed, D_fixed, p)

    fig, ax = plt.subplots(figsize=(6.0, 4.5))

    for sc in scenarios:
        rho_values = [p.rho_0 * phi_E(B, sc['I'], sc['H'], p) * pz for B in B_range]
        ax.plot(B_range, rho_values, color=sc['color'], linestyle=sc['ls'],
                label=sc['label'])

    ax.axhline(y=p.rho_0, color='gray', linestyle=':', linewidth=0.7, alpha=0.6)
    ax.annotate(r'$\rho_0$ baseline', xy=(7.5, p.rho_0),
                xytext=(7.5, p.rho_0 - 0.003),
                ha='left', fontsize=8, color='gray')

    ax.set_xlabel(r'Biophysical stock, $B$')
    ax.set_ylabel(r'Effective time preference, $\rho$')
    ax.legend(frameon=False, loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.2)
    ax.set_xlim(B_range.min(), B_range.max())
    ax.set_ylim(0, 0.05)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


# =====================================================================
# Figure 7: Offset-condition iso-rho* contours
# =====================================================================
def figure_7_offset(p: FrameworkParameters, save_path: str = None):
    v_grid = np.linspace(0.3, 5.0, 150)
    D_grid = np.linspace(0.3, 6.0, 150)
    V, D = np.meshgrid(v_grid, D_grid)

    Rho = np.zeros_like(V)
    for i in range(V.shape[0]):
        for j in range(V.shape[1]):
            Rho[i, j] = rho_star(V[i, j], D[i, j], p)

    fig, ax = plt.subplots(figsize=(6.5, 4.8))

    levels_fill = np.linspace(0, 0.15, 16)
    cs_fill = ax.contourf(V, D, np.clip(Rho, 0, 0.15), levels=levels_fill,
                          cmap='Greys', alpha=0.5)

    contour_levels = [0.005, 0.01, 0.02, 0.05, 0.10]
    cs = ax.contour(V, D, Rho, levels=contour_levels,
                    colors='black', linewidths=1.2)
    fmt = {level: f'{level:.3f}' for level in contour_levels}
    ax.clabel(cs, inline=True, fontsize=8, fmt=fmt, inline_spacing=4)

    cbar = fig.colorbar(cs_fill, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label(r'Effective time preference, $\rho^*$', fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    ax.annotate(r'Holding $\rho^*$ at $\rho_0 = 0.05$' + '\n' +
                r'requires $D$ rising in $v$',
                xy=(3.5, 0.9), xytext=(0.4, 3.5),
                fontsize=9, color='black',
                arrowprops=dict(arrowstyle='->', color='black',
                                lw=0.8, connectionstyle='arc3,rad=-0.3'))

    ax.set_xlabel(r'Information velocity, $v$')
    ax.set_ylabel(r'Deliberative capacity, $D$')
    ax.grid(True, alpha=0.2)
    ax.set_xlim(v_grid.min(), v_grid.max())
    ax.set_ylim(D_grid.min(), D_grid.max())

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    return fig


if __name__ == "__main__":
    p = FrameworkParameters()

    print("Generating Figure 1 (rho* vs v at varying D)...")
    figure_1_headline(p, save_path='figure_1_headline.png')

    print("Generating Figure 2 (stock dynamics under shock)...")
    figure_2_dynamics(p, save_path='figure_2_dynamics.png')

    print("Generating Figure 3 (convexity of biophysical depreciation)...")
    figure_3_convexity(p, save_path='figure_3_convexity.png')

    print("Generating Figure 4 (hysteresis in biophysical stock recovery)...")
    figure_4_hysteresis(p, save_path='figure_4_hysteresis.png')

    print("Generating Figure 5 (phi_E surface)...")
    figure_5_phi_E_surface(p, save_path='figure_5_phi_E.png')

    print("Generating Figure 6 (complementarity)...")
    figure_6_complementarity(p, save_path='figure_6_complementarity.png')

    print("Generating Figure 7 (offset condition)...")
    figure_7_offset(p, save_path='figure_7_offset.png')

    print("\nAll seven figures generated.")
    plt.close('all')
