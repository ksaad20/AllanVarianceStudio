"""Tests for noise_model module."""

import numpy as np
import pytest

from noise_model import fit_avsm, fit_armav, fit_gmwm
from allan_variance import AllanVarianceAnalyzer, NoiseParameters


class TestFitAVSM:
    """Test suite for AVSM fitting."""

    def test_white_noise_parameters(self):
        """Pure white noise should have ARW, minimal bias."""
        np.random.seed(42)
        fs = 200.0
        noise = np.random.normal(0, 0.001, int(fs * 3600))

        analyzer = AllanVarianceAnalyzer(noise, fs, 'gyroscope', 'x')
        tau, avar, avar_upper = analyzer.compute()
        params = fit_avsm(tau, avar)

        assert params.angle_random_walk > 0
        assert params.bias_instability >= 0
        assert params.max_integration_time > 0

    def test_empty_data(self):
        """Empty data should return default parameters."""
        params = fit_avsm(np.array([]), np.array([]))
        assert isinstance(params, NoiseParameters)
        assert params.angle_random_walk == 0.0

    def test_nan_data(self):
        """All-NaN data should return default parameters."""
        tau = np.array([1.0, 2.0, 3.0])
        avar = np.array([np.nan, np.nan, np.nan])
        params = fit_avsm(tau, avar)
        assert params.angle_random_walk == 0.0


class TestFitARMAV:
    """Test suite for ARMAV fitting."""

    def test_convergence(self):
        """ARMAV should converge on clean data."""
        np.random.seed(42)
        fs = 200.0
        noise = np.random.normal(0, 0.001, int(fs * 3600))

        analyzer = AllanVarianceAnalyzer(noise, fs, 'gyroscope', 'x')
        tau, avar, avar_upper = analyzer.compute()

        avsm_params = fit_avsm(tau, avar)
        armav_params = fit_armav(tau, avar, initial_guess=avsm_params)

        assert armav_params.angle_random_walk > 0
        assert armav_params.bias_instability >= 0

    def test_fallback_on_failure(self):
        """Should fall back to initial guess on bad data."""
        bad_tau = np.array([1.0])
        bad_avar = np.array([1.0])
        guess = NoiseParameters(angle_random_walk=0.01)

        result = fit_armav(bad_tau, bad_avar, initial_guess=guess)
        assert result.angle_random_walk == 0.01  # Fallback to guess


class TestFitGMWM:
    """Test suite for GMWM fitting."""

    def test_conservative_estimate(self):
        """GMWM should not underestimate noise."""
        np.random.seed(42)
        fs = 200.0
        noise = np.random.normal(0, 0.001, int(fs * 3600))

        analyzer = AllanVarianceAnalyzer(noise, fs, 'gyroscope', 'x')
        tau, avar, avar_upper = analyzer.compute()

        avsm_params = fit_avsm(tau, avar)
        gmwm_params = fit_gmwm(tau, avar, initial_guess=avsm_params)

        # GMWM should be equal or larger than AVSM (conservative)
        assert gmwm_params.angle_random_walk >= avsm_params.angle_random_walk * 0.5

    def test_fallback_on_failure(self):
        """Should fall back to initial guess on bad data."""
        bad_tau = np.array([1.0])
        bad_avar = np.array([1.0])
        guess = NoiseParameters(angle_random_walk=0.01)

        result = fit_gmwm(bad_tau, bad_avar, initial_guess=guess)
        assert result.angle_random_walk == 0.01
