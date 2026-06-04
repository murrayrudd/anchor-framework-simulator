# Python implementation of the institutional-anchor framework

This directory contains the Python implementation of the framework developed in Rudd (2026) and the script that reproduces all figures in the paper.

## Files

- **`anchor_framework.py`** — Core module. Implements the framework's equations: depreciation functions $\delta_X(v)$, supply functions $\sigma_X(\cdot)$, steady-state stocks $N^*, B^*, I^*, H^*$, existence channel $\phi_E$, salience channel $\phi_Z$, and steady-state effective time preference $\rho^*$. Provides `FrameworkParameters` (a dataclass with all parameter defaults) and callable functions for each quantity.
- **`generate_figures.py`** — Reproduces Figures 1 through 7 of the paper. Each function returns a `matplotlib.figure.Figure` and saves PNG and SVG to the working directory.
- **`requirements.txt`** — Dependencies: `numpy`, `scipy`, `matplotlib`.

## Model structure

The biophysical anchor is split into two state variables. A **physical natural-capital stock** $N$ (fish biomass, aquifer volume, atmospheric composition) underlies a **legible biophysical reference** $B$ — the baselines, indicators, and assessed conditions that monitoring and discovery produce from $N$ and that valuation actually engages. The framework therefore carries four stocks:

```
N' = -delta_N(v) * N + sigma_N(N, D)      physical natural capital
B' = -delta_B(v) * B + sigma_B(N, D)      biophysical reference (discovered from N)
I' = -delta_I(v) * I + sigma_I(D)         institutional anchor stock
H' = -delta_H(v) * H + sigma_H(D)         historical anchor stock
```

The three anchors that deliberation engages remain $B$, $I$, $H$, so the existence channel is $\phi_E = B^{-a_B} I^{-a_I} H^{-a_H}$; $N$ enters $\rho^*$ only through its support of $B$. The slow, remnant-dependent recovery lives in $N$ through the **concave** regeneration exponent $\gamma_N$ ($0 < \gamma_N < 1$): a depleted system regenerates from its own remnant, so recovery is slower than depletion. This is a *rate* asymmetry to a unique stable steady state (recovery eigenvalue $\lambda_N = -\delta_N(v)(1-\gamma_N) < 0$), **not** bistability; the genuinely bistable case (critical depensation) is discussed in the paper as an extension.

## Installation and usage

Requires Python 3.8 or later.

```bash
pip install -r requirements.txt
python generate_figures.py
```

This produces PNG and SVG files in the working directory. To use the framework programmatically:

```python
from anchor_framework import FrameworkParameters, rho_star, baseline_stocks, simulate_dynamics

p = FrameworkParameters()                 # default calibration
rho = rho_star(v=2.0, D=1.5, p=p)         # steady-state effective time preference

# steady-state stocks, useful as simulation initial conditions
N0, B0, I0, H0 = baseline_stocks(1.0, 1.0, p)

# integrate a velocity shock from v=1 to v=3 at t=30 (D held at 1)
import numpy as np
t = np.arange(0, 120, 0.25)
v = np.where(t < 30, 1.0, 3.0)
D = np.full_like(t, 1.0)
traj = simulate_dynamics(v, D, N0, B0, I0, H0, p, dt=0.25)   # keys: N, B, I, H, rho_eff, time
```

To run sensitivity analyses, modify parameters via `dataclasses.replace`:

```python
from dataclasses import replace
p_high_convexity = replace(p, alpha_N=2.5)   # steeper physical depreciation
rho_high = rho_star(v=2.0, D=1.5, p=p_high_convexity)
```

## Parameter calibration

The default parameter values in `FrameworkParameters` are illustrative, chosen so the figures are legible rather than empirically estimated. At $v=1, D=1$ the calibration produces:

- $N^* \approx 49.0$
- $B^* \approx 23.5$
- $I^* \approx 3.5$
- $H^* \approx 2.0$
- $\rho^* \approx 0.004$

Under a velocity shock from $v=1$ to $v=3$ at $t=30$, $\rho^*$ rises to approximately $0.043$ without a deliberative response (a more-than-tenfold increase), or to approximately $0.016$ with $D$ raised to $2.5$ (about a third of the uncompensated rise). These values match Figure 2.

The depreciation convexity exponents are $\alpha_N = \alpha_B = 1.5$, generating the threshold structure in Figure 3 (which varies $\alpha_N$). The physical regeneration concavity is $\gamma_N = 0.5$, generating the slow, asymmetric recovery in Figure 4; the discovery exponent on the physical stock is $\gamma_B = 0.5$. The Cobb-Douglas weights $a_B, a_I, a_H$ are $0.40, 0.35, 0.25$.

These choices are illustrative. For applications to specific cases the structural parameters — the convexity exponents $\alpha_N, \alpha_B$, the regeneration concavity $\gamma_N$, the discovery exponent $\gamma_B$, the diminishing-returns exponents $\eta_X$, the salience exponent $\theta$, and the Cobb-Douglas weights — should be calibrated against the best available evidence for the system in question. The qualitative results hold across a wide parameter range: $\partial \rho^*/\partial v > 0$, $\partial \rho^*/\partial D < 0$, convex acceleration when $\alpha_N, \alpha_B > 1$, and slow asymmetric recovery when $0 < \gamma_N < 1$.

## Reference

Rudd, M.A. (2026). Keeping the future visible: institutional anchors and time preference in ecosystem service valuation. *SSRN preprint*. *[URL to follow]*
