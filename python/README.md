# Python implementation of the institutional-anchor framework

This directory contains the Python implementation of the framework developed in Rudd (2026) and the script that reproduces all figures in the paper.

## Files

- **`anchor_framework.py`** — Core module. Implements the framework's equations: depreciation functions $\delta_X(v)$, supply functions $\sigma_X(\cdot)$, steady-state stocks $B^*, I^*, H^*$, existence channel $\phi_E$, salience channel $\phi_Z$, and steady-state effective time preference $\rho^*$. Provides `FrameworkParameters` (a dataclass with all parameter defaults) and callable functions for each quantity.
- **`generate_figures.py`** — Reproduces Figures 1 through 7 of the paper. Each figure is a single panel; each function returns a `matplotlib.figure.Figure` and optionally saves a PNG.
- **`requirements.txt`** — Dependencies: `numpy`, `scipy`, `matplotlib`.

## Installation and usage

Requires Python 3.8 or later.

```bash
pip install -r requirements.txt
python generate_figures.py
```

This produces PNG files in the working directory. To use the framework programmatically:

```python
from anchor_framework import FrameworkParameters, rho_star, steady_state_B

p = FrameworkParameters()  # default calibration
rho = rho_star(v=2.0, D=1.5, p=p)
B = steady_state_B(v=2.0, D=1.5, p=p)
```

To run sensitivity analyses, modify parameters via `dataclasses.replace`:

```python
from dataclasses import replace
p_high_convexity = replace(p, alpha_B=2.5)
rho_high = rho_star(v=2.0, D=1.5, p=p_high_convexity)
```

## Parameter calibration

The default parameter values in `FrameworkParameters` are calibrated to reproduce the paper's published figures. At $v=1, D=1$, the calibration produces:

- $B^* \approx 16.0$
- $I^* \approx 3.5$
- $H^* \approx 2.0$
- $\rho^* \approx 0.005$

Under a velocity shock from $v=1$ to $v=3$ at $t=30$, $\rho^*$ rises to approximately $0.05$ without a deliberative response, or to approximately $0.02$ with $D$ raised to $2.5$. These values match Figure 2 of the paper.

The depreciation parameters are calibrated as follows. The biophysical convexity exponent is $\alpha_B = 1.5$, sufficient to generate the threshold structure visible in Figure 3. The state-dependence exponent is $\gamma_B = 0.5$, sufficient to generate the hysteresis visible in Figure 4. The Cobb-Douglas weights $a_B, a_I, a_H$ are set at $0.40, 0.35, 0.25$, weighted toward the biophysical channel since biophysical anchors carry the threshold-and-hysteresis structure that is the framework's distinctive contribution.

These parameter choices are illustrative rather than empirically calibrated. For applications to specific cases, the framework's structural parameters ($\alpha_B$, $\gamma_B$, the diminishing-returns exponents, the salience exponent $\theta$, and the Cobb-Douglas weights) should be calibrated against the best available evidence for the system in question. The framework itself is agnostic to specific parameter values; the qualitative results (positive $\partial \rho^*/\partial v$, negative $\partial \rho^*/\partial D$, threshold structure when $\alpha_B > 1$, hysteresis when $\gamma_B > 0$) hold across a wide parameter range.

## Reference

Rudd, M.A. (2026). An institutional framework for modeling the supply side of time preference. *SSRN preprint*. <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6630139>
