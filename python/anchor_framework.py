"""
Anchor framework module (four-stock N/B specification).

Implements the institutional anchor framework for the supply side of time
preference (Rudd, 2026), in the form used in the manuscript:

  Laws of motion (Eqs. 4-7):
      N' = -delta_N(v) * N + sigma_N(N, D)      physical natural-capital stock
      B' = -delta_B(v) * B + sigma_B(N, D)      biophysical reference (discovered from N)
      I' = -delta_I(v) * I + sigma_I(D)         institutional anchor stock
      H' = -delta_H(v) * H + sigma_H(D)         historical anchor stock

  Depreciation (Eq. 8):
      delta_X(v) = delta_X0 + delta_X1 * v^alpha_X,     X in {N, B, I, H}

  Supply (Eqs. 9-11):
      sigma_N(N, D) = sigma_bar_N * N^gamma_N * (1 + beta_N * D^eta_N)   (0 < gamma_N < 1)
      sigma_B(N, D) = sigma_bar_B * N^gamma_B * (1 + beta_B * D^eta_B)   (discovery from N)
      sigma_I(D)    = sigma_bar_I + beta_I * D^eta_I
      sigma_H(D)    = sigma_bar_H + beta_H * D^eta_H

  Channels and effective time preference (Eqs. 12-14):
      rho*  = rho_0 * phi_E(B, I, H) * phi_Z(v, D)
      phi_E = B^(-a_B) * I^(-a_I) * H^(-a_H)        (a_B + a_I + a_H = 1)
      phi_Z = (v / (v_0 + D))^theta

  Steady states (Eqs. 15-18):
      N* = [sigma_bar_N (1 + beta_N D^eta_N) / delta_N(v)]^(1/(1-gamma_N))
      B* = sigma_bar_B (N*)^gamma_B (1 + beta_B D^eta_B) / delta_B(v)
      I* = sigma_I(D) / delta_I(v)
      H* = sigma_H(D) / delta_H(v)

Key modeling point: the biophysical anchor is split into the physical stock N
(natural capital) and the legible reference B that discovery produces from it.
The slow, remnant-dependent recovery lives in N via the concave regeneration
exponent gamma_N (0 < gamma_N < 1); the reference B has linear own-dynamics and
tracks N. Deliberation engages B, I, H, so phi_E carries those three; N enters
rho* only through its support of B. The asymmetric-recovery result is a rate
asymmetry to a unique stable steady state (recovery eigenvalue
lambda_N = -delta_N(v)(1 - gamma_N) < 0), not bistability.

Default parameters are illustrative, chosen so the figures are legible (at
v=1, D=1: N* ~ 49, B* ~ 23.5, I* ~ 3.5, H* ~ 2.0, rho* ~ 0.004). They are not
empirically calibrated; for applications the structural exponents should be set
against the best available evidence for the system in question.
"""

from dataclasses import dataclass


@dataclass
class FrameworkParameters:
    # Existence-channel Cobb-Douglas weights on B, I, H (sum to 1)
    a_B: float = 0.40
    a_I: float = 0.35
    a_H: float = 0.25

    # Baseline time preference and salience channel
    rho_0: float = 0.05
    theta: float = 1.0
    v_0: float = 1.0

    # Physical natural-capital stock N: depreciation
    delta_N0: float = 0.05
    delta_N1: float = 0.04
    alpha_N: float = 1.5          # convex physical depreciation

    # Biophysical reference stock B: depreciation (monitoring/assessment decay)
    delta_B0: float = 0.15
    delta_B1: float = 0.10
    alpha_B: float = 1.5

    # Institutional depreciation
    delta_I0: float = 0.10
    delta_I1: float = 0.157
    alpha_I: float = 1.0

    # Historical depreciation
    delta_H0: float = 0.10
    delta_H1: float = 0.20
    alpha_H: float = 1.0

    # Physical regeneration (concave, remnant-dependent): source of slow recovery
    sigma_bar_N: float = 0.45
    gamma_N: float = 0.5          # 0 < gamma_N < 1
    beta_N: float = 0.4
    eta_N: float = 0.7

    # Biophysical discovery from N (produces the reference stock B)
    sigma_bar_B: float = 0.6
    gamma_B: float = 0.5          # discovery exponent on the physical stock, 0 < gamma_B <= 1
    beta_B: float = 0.4
    eta_B: float = 0.7

    # Institutional supply
    sigma_bar_I: float = 0.5
    beta_I: float = 0.4
    eta_I: float = 0.7

    # Historical supply
    sigma_bar_H: float = 0.3
    beta_H: float = 0.3
    eta_H: float = 0.7


# ----------------------------- depreciation -----------------------------

def delta_N(v: float, p: FrameworkParameters) -> float:
    return p.delta_N0 + p.delta_N1 * v ** p.alpha_N


def delta_B(v: float, p: FrameworkParameters) -> float:
    return p.delta_B0 + p.delta_B1 * v ** p.alpha_B


def delta_I(v: float, p: FrameworkParameters) -> float:
    return p.delta_I0 + p.delta_I1 * v ** p.alpha_I


def delta_H(v: float, p: FrameworkParameters) -> float:
    return p.delta_H0 + p.delta_H1 * v ** p.alpha_H


# ------------------------------- supply --------------------------------

def sigma_N(N: float, D: float, p: FrameworkParameters) -> float:
    """Concave, remnant-dependent physical regeneration."""
    return p.sigma_bar_N * (N ** p.gamma_N) * (1 + p.beta_N * D ** p.eta_N)


def sigma_B(N: float, D: float, p: FrameworkParameters) -> float:
    """Discovery of the biophysical reference from the physical stock N."""
    return p.sigma_bar_B * (N ** p.gamma_B) * (1 + p.beta_B * D ** p.eta_B)


def sigma_I(D: float, p: FrameworkParameters) -> float:
    return p.sigma_bar_I + p.beta_I * D ** p.eta_I


def sigma_H(D: float, p: FrameworkParameters) -> float:
    return p.sigma_bar_H + p.beta_H * D ** p.eta_H


# ---------------------------- steady states ----------------------------

def steady_state_N(v: float, D: float, p: FrameworkParameters) -> float:
    """N* = [sigma_bar_N (1 + beta_N D^eta_N) / delta_N(v)]^(1/(1-gamma_N))."""
    numerator = p.sigma_bar_N * (1 + p.beta_N * D ** p.eta_N)
    return (numerator / delta_N(v, p)) ** (1.0 / (1.0 - p.gamma_N))


def steady_state_B(v: float, D: float, p: FrameworkParameters) -> float:
    """B* = sigma_bar_B (N*)^gamma_B (1 + beta_B D^eta_B) / delta_B(v) (linear in B given N*)."""
    N_star = steady_state_N(v, D, p)
    return p.sigma_bar_B * (N_star ** p.gamma_B) * (1 + p.beta_B * D ** p.eta_B) / delta_B(v, p)


def steady_state_I(v: float, D: float, p: FrameworkParameters) -> float:
    return sigma_I(D, p) / delta_I(v, p)


def steady_state_H(v: float, D: float, p: FrameworkParameters) -> float:
    return sigma_H(D, p) / delta_H(v, p)


# ----------------------------- channels --------------------------------

def phi_E(B: float, I: float, H: float, p: FrameworkParameters) -> float:
    """Existence channel: B^(-a_B) * I^(-a_I) * H^(-a_H). Engages B, I, H (not N)."""
    return B ** (-p.a_B) * I ** (-p.a_I) * H ** (-p.a_H)


def phi_Z(v: float, D: float, p: FrameworkParameters) -> float:
    """Salience channel: (v / (v_0 + D))^theta."""
    return (v / (p.v_0 + D)) ** p.theta


def rho_star(v: float, D: float, p: FrameworkParameters) -> float:
    """Steady-state effective time preference."""
    B = steady_state_B(v, D, p)
    I = steady_state_I(v, D, p)
    H = steady_state_H(v, D, p)
    return p.rho_0 * phi_E(B, I, H, p) * phi_Z(v, D, p)


def baseline_stocks(v: float, D: float, p: FrameworkParameters):
    """Convenience: steady-state (N*, B*, I*, H*) for use as simulation initial conditions."""
    return (steady_state_N(v, D, p), steady_state_B(v, D, p),
            steady_state_I(v, D, p), steady_state_H(v, D, p))


# ------------------------------ dynamics -------------------------------

def simulate_dynamics(v_schedule, D_schedule, N_0, B_0, I_0, H_0, p, dt=0.25):
    """
    Integrate the four laws of motion by forward Euler.

        N' = -delta_N(v) N + sigma_N(N, D)
        B' = -delta_B(v) B + sigma_B(N, D)
        I' = -delta_I(v) I + sigma_I(D)
        H' = -delta_H(v) H + sigma_H(D)

    Parameters
    ----------
    v_schedule, D_schedule : array-like (equal length)
        Information velocity and deliberative capacity at each step.
    N_0, B_0, I_0, H_0 : float
        Initial stock values (see ``baseline_stocks``).
    p : FrameworkParameters
    dt : float
        Forward-Euler step. Default 0.25.

    Returns
    -------
    dict with keys 'time', 'N', 'B', 'I', 'H', 'rho_eff'.
    """
    import numpy as np
    v_arr = np.asarray(v_schedule, dtype=float)
    D_arr = np.asarray(D_schedule, dtype=float)
    n = len(v_arr)
    if len(D_arr) != n:
        raise ValueError("v_schedule and D_schedule must have the same length")

    N = np.empty(n); B = np.empty(n); I = np.empty(n); H = np.empty(n); rho_eff = np.empty(n)
    N[0], B[0], I[0], H[0] = N_0, B_0, I_0, H_0

    for k in range(1, n):
        v_k, D_k = v_arr[k - 1], D_arr[k - 1]
        N_safe = max(N[k - 1], 1e-9)
        dN = -delta_N(v_k, p) * N_safe + sigma_N(N_safe, D_k, p)
        dB = -delta_B(v_k, p) * B[k - 1] + sigma_B(N_safe, D_k, p)
        dI = -delta_I(v_k, p) * I[k - 1] + sigma_I(D_k, p)
        dH = -delta_H(v_k, p) * H[k - 1] + sigma_H(D_k, p)
        N[k] = max(1e-9, N[k - 1] + dt * dN)
        B[k] = max(1e-9, B[k - 1] + dt * dB)
        I[k] = max(1e-9, I[k - 1] + dt * dI)
        H[k] = max(1e-9, H[k - 1] + dt * dH)

    for k in range(n):
        rho_eff[k] = p.rho_0 * phi_E(B[k], I[k], H[k], p) * phi_Z(v_arr[k], D_arr[k], p)

    time = np.arange(n) * dt
    return {'time': time, 'N': N, 'B': B, 'I': I, 'H': H, 'rho_eff': rho_eff}


if __name__ == "__main__":
    p = FrameworkParameters()
    for v, D in [(1, 1), (3, 1), (3, 2.5)]:
        print(f"v={v}, D={D}:  N*={steady_state_N(v, D, p):6.2f}  B*={steady_state_B(v, D, p):6.2f}  "
              f"I*={steady_state_I(v, D, p):5.2f}  H*={steady_state_H(v, D, p):5.2f}  "
              f"rho*={rho_star(v, D, p):.4f}")
