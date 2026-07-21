"""Tests for tremor_simulator module."""

import numpy as np
import pytest

from tremor_simulator import TremorSimulator, TremorDetection
from allan_variance import NoiseParameters


class TestTremorSimulator:
    """Test suite for TremorSimulator."""

    def test_tremor_generation(self):
        """Generated signal should contain tremor frequency."""
        params = NoiseParameters(
            angle_random_walk=0.001,
            bias_instability=0.0001
        )
        sim = TremorSimulator(params, fs=200.0)

        signal = sim.generate_tremor(frequency=6.0, amplitude=1.0, duration=10.0)

        assert len(signal) == int(200.0 * 10.0)
        assert np.std(signal) > 0  # Should have variation

    def test_detection_snr_positive(self):
        """Strong tremor should have positive SNR."""
        params = NoiseParameters(
            angle_random_walk=0.0001,  # Low noise
            bias_instability=0.00001
        )
        sim = TremorSimulator(params, fs=200.0, detection_threshold=6.0)

        signal = sim.generate_tremor(frequency=6.0, amplitude=2.0, duration=10.0)
        detected, snr = sim.detect_tremor(signal, frequency=6.0)

        assert snr > 0
        assert detected  # Strong signal should be detected

    def test_detection_weak_signal(self):
        """Weak tremor may not be detected."""
        params = NoiseParameters(
            angle_random_walk=0.01,  # High noise
            bias_instability=0.001
        )
        sim = TremorSimulator(params, fs=200.0, detection_threshold=6.0)

        signal = sim.generate_tremor(frequency=6.0, amplitude=0.01, duration=10.0)
        detected, snr = sim.detect_tremor(signal, frequency=6.0)

        # Weak signal in high noise should not be detected
        assert not detected or snr < 6.0

    def test_validation_runs(self):
        """Full validation should return results."""
        params = NoiseParameters(
            angle_random_walk=0.001,
            bias_instability=0.0001
        )
        sim = TremorSimulator(params, fs=200.0)

        results = sim.run_validation(
            tremor_frequencies=[4.0, 6.0],
            amplitudes=[0.1, 0.5, 1.0],
            duration=5.0
        )

        assert len(results) == 6  # 2 freqs × 3 amplitudes
        assert all(isinstance(r, TremorDetection) for r in results)

    def test_calibrated_better_than_uncalibrated(self):
        """Calibrated detection should outperform uncalibrated."""
        params = NoiseParameters(
            angle_random_walk=0.001,
            bias_instability=0.0001
        )
        sim = TremorSimulator(params, fs=200.0)

        results = sim.run_validation(
            tremor_frequencies=[6.0],
            amplitudes=[0.5],
            duration=10.0
        )

        r = results[0]
        assert r.snr_calibrated >= r.snr_uncalibrated

    def test_threshold_calculation(self):
        """Thresholds should be returned for valid frequency."""
        params = NoiseParameters(
            angle_random_walk=0.001,
            bias_instability=0.0001
        )
        sim = TremorSimulator(params, fs=200.0)

        results = sim.run_validation(
            tremor_frequencies=[6.0],
            amplitudes=[0.1, 0.5, 1.0],
            duration=5.0
        )

        cal, uncal = sim.get_detection_thresholds(results, frequency=6.0)

        assert cal > 0
        assert uncal > 0
        assert cal <= uncal  # Calibrated should be equal or better
