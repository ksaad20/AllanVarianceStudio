"""Tremor signal simulation for pre-clinical validation.

Generates realistic biological tremor signals with calibrated and
uncalibrated sensor noise for detection threshold comparison.
"""

import numpy as np
from scipy.signal import butter, filtfilt
from dataclasses import dataclass
from typing import List, Dict, Tuple
from allan_variance import NoiseParameters


@dataclass
class TremorDetection:
    """Result of tremor detection simulation.

    Attributes:
        frequency: Tremor frequency in Hz
        amplitude: Tremor amplitude in mm
        detected_calibrated: Whether detected with calibrated noise
        detected_uncalibrated: Whether detected with factory noise
        snr_calibrated: Signal-to-noise ratio with calibration (dB)
        snr_uncalibrated: Signal-to-noise ratio without calibration (dB)
    """
    frequency: float
    amplitude: float
    detected_calibrated: bool
    detected_uncalibrated: bool
    snr_calibrated: float
    snr_uncalibrated: float


class TremorSimulator:
    """Simulate tremor signals with realistic sensor noise.

    Args:
        noise_params: Calibrated noise parameters
        fs: Sampling frequency in Hz
        detection_threshold: SNR threshold in dB for positive detection
    """

    def __init__(self, noise_params: NoiseParameters, fs: float = 200.0,
                 detection_threshold: float = 6.0):
        self.noise_params = noise_params
        self.fs = float(fs)
        self.dt = 1.0 / self.fs
        self.detection_threshold = float(detection_threshold)

    def generate_tremor(self, frequency: float, amplitude: float,
                        duration: float = 60.0) -> np.ndarray:
        """Generate tremor signal with sensor noise.

        Args:
            frequency: Tremor frequency in Hz
            amplitude: Tremor amplitude in mm
            duration: Signal duration in seconds

        Returns:
            Simulated sensor signal with tremor + noise
        """
        t = np.arange(0, duration, self.dt)
        n_samples = len(t)

        # Pure tremor signal (sinusoidal)
        tremor = amplitude * np.sin(2 * np.pi * frequency * t)

        # Add sensor noise based on calibrated parameters
        noise = self._generate_sensor_noise(n_samples)

        return tremor + noise

    def _generate_sensor_noise(self, n_samples: int) -> np.ndarray:
        """Generate realistic sensor noise from calibrated parameters.

        Components:
        - Angle random walk: white noise scaled by N * sqrt(dt)
        - Bias instability: low-frequency correlated noise
        - Quantization noise: uniform discretization noise
        """
        noise = np.zeros(n_samples)

        # Angle random walk (white noise)
        if self.noise_params.angle_random_walk > 0:
            arw_std = self.noise_params.angle_random_walk * np.sqrt(self.dt)
            noise += np.random.normal(0, arw_std, n_samples)

        # Bias instability (correlated, 1/f-like)
        if self.noise_params.bias_instability > 0:
            # Simple approximation: random walk with damping
            bias_noise = np.zeros(n_samples)
            bias_state = 0.0
            tau_b = 100.0  # Bias correlation time (seconds)
            alpha = np.exp(-self.dt / tau_b)
            bias_std = self.noise_params.bias_instability * np.sqrt(1 - alpha**2)

            for i in range(n_samples):
                bias_state = alpha * bias_state + np.random.normal(0, bias_std)
                bias_noise[i] = bias_state

            noise += bias_noise

        # Quantization noise
        if self.noise_params.quantization_noise > 0:
            q = self.noise_params.quantization_noise
            noise += np.random.uniform(-q/2, q/2, n_samples)

        return noise

    def detect_tremor(self, signal: np.ndarray, frequency: float,
                      bandwidth: float = 2.0) -> Tuple[bool, float]:
        """Band-pass filter and compute SNR.

        Args:
            signal: Sensor signal
            frequency: Target tremor frequency
            bandwidth: Filter bandwidth in Hz

        Returns:
            (detected, snr_db)
        """
        nyq = self.fs / 2
        low = max((frequency - bandwidth/2) / nyq, 0.01)
        high = min((frequency + bandwidth/2) / nyq, 0.99)

        if low >= high:
            return False, -np.inf

        # Band-pass filter
        b, a = butter(4, [low, high], btype='band')
        filtered = filtfilt(b, a, signal)

        # Signal power in band
        signal_power = np.mean(filtered**2)

        # Noise power outside band (total - signal)
        total_power = np.mean(signal**2)
        noise_power = max(total_power - signal_power, 1e-12)

        snr = 10 * np.log10(signal_power / noise_power)
        detected = snr > self.detection_threshold

        return detected, snr

    def run_validation(self, tremor_frequencies: List[float],
                       amplitudes: List[float],
                       duration: float = 60.0) -> List[TremorDetection]:
        """Run full tremor detection validation.

        Args:
            tremor_frequencies: List of frequencies to test (Hz)
            amplitudes: List of amplitudes to test (mm)
            duration: Duration per condition (seconds)

        Returns:
            List of TremorDetection results
        """
        results = []

        # Uncalibrated parameters (3× worse ARW, 2× worse bias)
        uncal_params = NoiseParameters(
            quantization_noise=self.noise_params.quantization_noise,
            angle_random_walk=self.noise_params.angle_random_walk * 3,
            bias_instability=self.noise_params.bias_instability * 2,
            rate_random_walk=self.noise_params.rate_random_walk,
            rate_ramp=self.noise_params.rate_ramp
        )

        for freq in tremor_frequencies:
            for amp in amplitudes:
                # Calibrated detection
                signal_cal = self.generate_tremor(freq, amp, duration)
                detected_cal, snr_cal = self.detect_tremor(signal_cal, freq)

                # Uncalibrated detection
                sim_uncal = TremorSimulator(uncal_params, self.fs, self.detection_threshold)
                signal_uncal = sim_uncal.generate_tremor(freq, amp, duration)
                detected_uncal, snr_uncal = sim_uncal.detect_tremor(signal_uncal, freq)

                results.append(TremorDetection(
                    frequency=freq,
                    amplitude=amp,
                    detected_calibrated=detected_cal,
                    detected_uncalibrated=detected_uncal,
                    snr_calibrated=snr_cal,
                    snr_uncalibrated=snr_uncal
                ))

        return results

    def get_detection_thresholds(self, results: List[TremorDetection],
                                  frequency: float) -> Tuple[float, float]:
        """Get minimum detectable amplitude at a given frequency.

        Args:
            results: Validation results
            frequency: Target frequency

        Returns:
            (calibrated_threshold, uncalibrated_threshold) in mm
        """
        freq_results = [r for r in results if r.frequency == frequency]

        cal_detected = [r.amplitude for r in freq_results if r.detected_calibrated]
        uncal_detected = [r.amplitude for r in freq_results if r.detected_uncalibrated]

        cal_threshold = min(cal_detected) if cal_detected else float('inf')
        uncal_threshold = min(uncal_detected) if uncal_detected else float('inf')

        return cal_threshold, uncal_threshold
