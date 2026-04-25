"""
Reconstruction of the anchor framework module from the paper specifications.

Implements the equations from Rudd's institutional anchor framework paper
(2026 v2 draft):
- Eq. (4)-(6): laws of motion
- Eq. (7) [first]: depreciation function delta_X(v) = delta_X0 + delta_X1 * v^alpha_X
- Eq. (7) [second, to be renumbered (8)]: biophysical supply
  sigma_B(B,D) = sigma_bar_B * B^gamma_B * (1 + beta_B * D^eta_B)
- Eq. (8) [to be renumbered (9)]: institutional and historical supply
  sigma_I(D) = sigma_bar_I + beta_I * D^eta_I
  sigma_H(D) = sigma_bar_H + beta_H * D^eta_H
- Eq. (9) [to be renumbered (10)]: rho* = rho_0 * phi_E * phi_Z
- Eq. (10) [to be renumbered (11)]: phi_E = B^(-a_B) * I^(-a_I) * H^(-a_H)
- Eq. (11) [to be renumbered (12)]: phi_Z = (v / (v_0 + D))^theta
- Eq. (12) [to be renumbered (13)]: steady-state expressions

Default parameters chosen to reproduce the paper's existing figures:
- rho_0 baseline visible at 0.05 in figure 1 (eta from D making rho* drop below)
- B_steady-state ~16-17 at v=1, D=1 (visible in figure 2)
- I_steady-state ~3.5 at v=1, D=1 (visible in figure 2)
- H_steady-state ~2.0 at v=1, D=1 (visible in figure 2)
"""

from dataclasses import dataclass


@dataclass
class FrameworkParameters:
    # Cobb-Douglas weights for existence channel; sum to 1
    a_B: float = 0.4
    a_I: float = 0.35
    a_H: float = 0.25

    # Baseline time preference
    rho_0: float = 0.05

    # Salience channel (phi_Z)
    theta: float = 1.0
    v_0: float = 1.0

    # Biophysical depreciation (calibrated to figure 2: B*(v=1,D=1)=16, B*(v=3,D=1)=2)
    delta_B0: float = 0.1058
    delta_B1: float = 0.0817
    alpha_B: float = 1.5  # convexity exponent

    # Institutional depreciation (calibrated to figure 2: I*(v=1,D=1)=3.5)
    delta_I0: float = 0.1
    delta_I1: float = 0.157
    alpha_I: float = 1.0

    # Historical depreciation (calibrated to figure 2: H*(v=1,D=1)=2.0)
    delta_H0: float = 0.1
    delta_H1: float = 0.2
    alpha_H: float = 1.0

    # Biophysical supply (state-dependent)
    sigma_bar_B: float = 0.5    # scale parameter
    gamma_B: float = 0.5         # state-dependence exponent
    beta_B: float = 0.5          # deliberative amplification coefficient
    eta_B: float = 0.7           # deliberative amplification exponent

    # Institutional supply
    sigma_bar_I: float = 0.5
    beta_I: float = 0.4
    eta_I: float = 0.7

    # Historical supply
    sigma_bar_H: float = 0.3
    beta_H: float = 0.3
    eta_H: float = 0.7


def delta_B(v: float, p: FrameworkParameters) -> float:
    return p.delta_B0 + p.delta_B1 * v ** p.alpha_B


def delta_I(v: float, p: FrameworkParameters) -> float:
    return p.delta_I0 + p.delta_I1 * v ** p.alpha_I


def delta_H(v: float, p: FrameworkParameters) -> float:
    return p.delta_H0 + p.delta_H1 * v ** p.alpha_H


def sigma_B(B: float, D: float, p: FrameworkParameters) -> float:
    """State-dependent biophysical supply."""
    return p.sigma_bar_B * (B ** p.gamma_B) * (1 + p.beta_B * D ** p.eta_B)


def sigma_I(D: float, p: FrameworkParameters) -> float:
    return p.sigma_bar_I + p.beta_I * D ** p.eta_I


def sigma_H(D: float, p: FrameworkParameters) -> float:
    return p.sigma_bar_H + p.beta_H * D ** p.eta_H


def steady_state_B(v: float, D: float, p: FrameworkParameters) -> float:
    """B* = [sigma_bar_B * (1 + beta_B * D^eta_B) / delta_B(v)]^(1/(1-gamma_B))"""
    numerator = p.sigma_bar_B * (1 + p.beta_B * D ** p.eta_B)
    denominator = delta_B(v, p)
    return (numerator / denominator) ** (1.0 / (1.0 - p.gamma_B))


def steady_state_I(v: float, D: float, p: FrameworkParameters) -> float:
    return sigma_I(D, p) / delta_I(v, p)


def steady_state_H(v: float, D: float, p: FrameworkParameters) -> float:
    return sigma_H(D, p) / delta_H(v, p)


def phi_E(B: float, I: float, H: float, p: FrameworkParameters) -> float:
    """Existence channel: B^(-a_B) * I^(-a_I) * H^(-a_H)."""
    return B ** (-p.a_B) * I ** (-p.a_I) * H ** (-p.a_H)


def phi_Z(v: float, D: float, p: FrameworkParameters) -> float:
    """Salience channel: (v / (v_0 + D))^theta."""
    return (v / (p.v_0 + D)) ** p.theta


def rho_star(v: float, D: float, p: FrameworkParameters) -> float:
    """Steady-state effective time preference."""
    B = steady_state_B(v, D, p)
    I = steady_state_I(v, D, p)
    H = steady_state_H(v, D, p)
    phi_e = phi_E(B, I, H, p)
    phi_z = phi_Z(v, D, p)
    return p.rho_0 * phi_e * phi_z


def simulate_dynamics(v_schedule, D_schedule, B_0, I_0, H_0, p, dt=0.5):
    """
    Simulate stock dynamics under prescribed schedules of v and D.

    Integrates the laws of motion (eqs. 4-6) by forward Euler:
        B' = -delta_B(v) * B + sigma_B(B, D)
        I' = -delta_I(v) * I + sigma_I(D)
        H' = -delta_H(v) * H + sigma_H(D)

    Parameters
    ----------
    v_schedule : array-like
        Information velocity at each time step.
    D_schedule : array-like
        Deliberative capacity at each time step. Must be same length as v_schedule.
    B_0, I_0, H_0 : float
        Initial stock values.
    p : FrameworkParameters
        Framework parameters.
    dt : float, optional
        Time step for forward Euler integration. Default 0.5.

    Returns
    -------
    dict with keys 'time', 'B', 'I', 'H', 'rho_eff'.
        time : array of time values (length = len(v_schedule))
        B, I, H : arrays of stock trajectories
        rho_eff : array of effective time preferences along trajectory
    """
    import numpy as np
    v_arr = np.asarray(v_schedule, dtype=float)
    D_arr = np.asarray(D_schedule, dtype=float)
    n = len(v_arr)
    if len(D_arr) != n:
        raise ValueError("v_schedule and D_schedule must have the same length")

    B = np.empty(n)
    I = np.empty(n)
    H = np.empty(n)
    rho_eff = np.empty(n)

    B[0], I[0], H[0] = B_0, I_0, H_0
    rho_eff[0] = p.rho_0 * phi_E(B[0], I[0], H[0], p) * phi_Z(v_arr[0], D_arr[0], p)

    for k in range(1, n):
        v_k, D_k = v_arr[k - 1], D_arr[k - 1]
        B_safe = max(B[k - 1], 1e-6)
        dB = -delta_B(v_k, p) * B_safe + sigma_B(B_safe, D_k, p)
        dI = -delta_I(v_k, p) * I[k - 1] + sigma_I(D_k, p)
        dH = -delta_H(v_k, p) * H[k - 1] + sigma_H(D_k, p)
        B[k] = max(1e-6, B[k - 1] + dt * dB)
        I[k] = max(1e-6, I[k - 1] + dt * dI)
        H[k] = max(1e-6, H[k - 1] + dt * dH)
        rho_eff[k] = p.rho_0 * phi_E(B[k], I[k], H[k], p) * phi_Z(v_arr[k], D_arr[k], p)

    time = np.arange(n) * dt
    return {'time': time, 'B': B, 'I': I, 'H': H, 'rho_eff': rho_eff}
