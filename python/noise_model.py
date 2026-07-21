"""Noise model fitting methods for Allan variance analysis.

Implements multiple fitting approaches for the five-parameter noise model:
- AVSM: Allan Variance Slope Method (legacy, fast)
- ARMAV: Autonomous Regression Method for Allan Variance (log-domain NLS)
- GMWM: Generalized Method of Wavelet Moments (linear domain constrained)

References:
    IEEE Std 1293-2018
    NAVIGATION, Vol. 70, No. 3 (2023)
"""

import numpy as np
from scipy import optimize
from typing import Tuple
from allan_variance import NoiseParameters


def fit_avsm(tau: np.ndarray, avar: np.ndarray) -> NoiseParameters:
    """Allan Variance Slope Method.

    Fast initial parameter estimation using characteristic slopes.
    Suitable for real-time applications and initial guesses.

    Args:
        tau: Cluster times in seconds
        avar: Allan variance estimates

    Returns:
        NoiseParameters with estimated coefficients
    """
    valid = ~(np.isnan(avar) | np.isnan(tau) | (avar <= 0) | (tau <= 0))
    if not np.any(valid):
        return NoiseParameters()

    tau_fit = tau[valid]
    adev = np.sqrt(avar[valid])

    # Quantization noise (slope -1, shortest tau)
    q_idx = 0
    if len(adev) > 0:
        Q = adev[q_idx] * tau_fit[q_idx] / np.sqrt(3)
    else:
        Q = 0.0

    # Angle random walk (slope -1/2 region)
    arw_idx = min(len(tau_fit) // 10, len(tau_fit) - 1)
    if arw_idx > 0:
        N = adev[arw_idx] * np.sqrt(tau_fit[arw_idx])
    else:
        N = adev[0] * np.sqrt(tau_fit[0]) if len(adev) > 0 else 0.0

    # Bias instability (minimum of curve)
    min_idx = np.argmin(adev) if len(adev) > 0 else 0
    B = adev[min_idx] * 0.6648 if len(adev) > 0 else 0.0

    # Rate random walk (slope +1/2, longest tau)
    rrw_idx = max(len(tau_fit) * 3 // 4, min_idx + 1)
    if rrw_idx < len(adev):
        K = adev[rrw_idx] * np.sqrt(3.0 / tau_fit[rrw_idx])
    else:
        K = 0.0

    # Rate ramp (slope +1, very long tau)
    R = 0.0  # Often negligible for short recordings

    # Maximum integration time
    max_tau = _find_max_integration_time(tau_fit, adev, B)

    return NoiseParameters(
        quantization_noise=Q,
        angle_random_walk=N,
        bias_instability=B,
        rate_random_walk=K,
        rate_ramp=R,
        max_integration_time=max_tau
    )


def fit_armav(tau: np.ndarray, avar: np.ndarray,
              initial_guess: NoiseParameters = None) -> NoiseParameters:
    """Autonomous Regression Method for Allan Variance.

    Nonlinear least squares in log domain. More accurate than AVSM
    but computationally expensive.

    Args:
        tau: Cluster times in seconds
        avar: Allan variance estimates
        initial_guess: Starting parameters (default: AVSM estimate)

    Returns:
        NoiseParameters with optimized coefficients
    """
    if initial_guess is None:
        initial_guess = fit_avsm(tau, avar)

    valid = ~(np.isnan(avar) | np.isnan(tau) | (avar <= 0) | (tau <= 0))
    if not np.any(valid):
        return initial_guess

    tau_fit = tau[valid]
    avar_fit = avar[valid]

    # Initial parameters
    p0 = np.array([
        initial_guess.quantization_noise,
        initial_guess.angle_random_walk,
        initial_guess.bias_instability,
        initial_guess.rate_random_walk,
        initial_guess.rate_ramp
    ])

    def model(params, t):
        """Five-parameter noise model."""
        Q, N, B, K, R = params
        return (
            3 * Q**2 / t**2 +
            N**2 / t +
            (B / 0.6648)**2 +
            K**2 * t / 3 +
            R**2 * t**2 / 2
        )

    def residuals(params, t, y):
        """Log-domain residuals."""
        return np.log10(model(params, t)) - np.log10(y)

    try:
        result = optimize.least_squares(
            residuals, p0,
            args=(tau_fit, avar_fit),
            bounds=(0, np.inf),
            method='trf',
            max_nfev=10000
        )

        Q, N, B, K, R = result.x

        # Recalculate max integration time with fitted parameters
        adev_pred = np.sqrt(model(result.x, tau_fit))
        max_tau = _find_max_integration_time(tau_fit, adev_pred, B)

        return NoiseParameters(
            quantization_noise=Q,
            angle_random_walk=N,
            bias_instability=B,
            rate_random_walk=K,
            rate_ramp=R,
            max_integration_time=max_tau
        )
    except (optimize.OptimizeWarning, ValueError, RuntimeError):
        # Fall back to initial guess if optimization fails
        return initial_guess


def fit_gmwm(tau: np.ndarray, avar: np.ndarray,
             initial_guess: NoiseParameters = None) -> NoiseParameters:
    """Generalized Method of Wavelet Moments.

    Linear domain constrained optimization. Conservative estimates
    that never underestimate true noise.

    Args:
        tau: Cluster times in seconds
        avar: Allan variance estimates
        initial_guess: Starting parameters (default: AVSM estimate)

    Returns:
        NoiseParameters with conservative coefficients
    """
    if initial_guess is None:
        initial_guess = fit_avsm(tau, avar)

    valid = ~(np.isnan(avar) | np.isnan(tau) | (avar <= 0) | (tau <= 0))
    if not np.any(valid):
        return initial_guess

    tau_fit = tau[valid]
    avar_fit = avar[valid]

    p0 = np.array([
        initial_guess.quantization_noise,
        initial_guess.angle_random_walk,
        initial_guess.bias_instability,
        initial_guess.rate_random_walk,
        initial_guess.rate_ramp
    ])

    def model(params, t):
        """Five-parameter noise model."""
        Q, N, B, K, R = params
        return (
            3 * Q**2 / t**2 +
            N**2 / t +
            (B / 0.6648)**2 +
            K**2 * t / 3 +
            R**2 * t**2 / 2
        )

    def objective(params, t, y):
        """Objective with conservative penalty."""
        predicted = model(params, t)
        # Penalize underestimation (predicted < observed)
        penalty = np.sum(np.maximum(0, y - predicted)**2) * 1000
        return np.sum((predicted - y)**2) + penalty

    try:
        result = optimize.minimize(
            objective, p0,
            args=(tau_fit, avar_fit),
            method='L-BFGS-B',
            bounds=[(0, None)] * 5
        )

        Q, N, B, K, R = result.x
        adev_pred = np.sqrt(model(result.x, tau_fit))
        max_tau = _find_max_integration_time(tau_fit, adev_pred, B)

        return NoiseParameters(
            quantization_noise=Q,
            angle_random_walk=N,
            bias_instability=B,
            rate_random_walk=K,
            rate_ramp=R,
            max_integration_time=max_tau
        )
    except (ValueError, RuntimeError):
        return initial_guess


def _find_max_integration_time(tau: np.ndarray, adev: np.ndarray,
                                bias_instability: float) -> float:
    """Find maximum integration time before drift exceeds threshold."""
    if bias_instability <= 0 or len(adev) == 0:
        return 10.0

    threshold = 2.0 * bias_instability / 0.6648

    for i in reversed(range(len(adev))):
        if adev[i] < threshold and not np.isnan(adev[i]):
            return tau[i]

    return tau[-1] if len(tau) > 0 else 10.0
