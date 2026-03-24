import numpy as np


class System:
    name = "Base system"

    def dqdt(self, q, p):
        raise NotImplementedError

    def dpdt(self, q, p):
        raise NotImplementedError

    def energy(self, q, p):
        raise NotImplementedError

    def state_labels(self):
        return "q", "p"


class HarmonicOscillator(System):
    name = "Simple Harmonic Oscillator"

    def dqdt(self, q, p):
        return p

    def dpdt(self, q, p):
        return -q

    def energy(self, q, p):
        return 0.5 * (np.asarray(q) ** 2 + np.asarray(p) ** 2)

    def state_labels(self):
        return "q", "p"


class Pendulum(System):
    name = "Pendulum"

    def dqdt(self, q, p):
        return p

    def dpdt(self, q, p):
        return -np.sin(q)

    def energy(self, q, p):
        return 0.5 * (np.asarray(p) ** 2) + (1.0 - np.cos(np.asarray(q)))

    def state_labels(self):
        return "theta", "p"


class Kepler2D(System):
    name = "Two-Body / Kepler Problem"

    def __init__(self, mu=1.0):
        self.mu = mu

    def dqdt(self, q, p):
        return np.asarray(p)

    def dpdt(self, q, p):
        q = np.asarray(q)
        r = np.linalg.norm(q)
        return -self.mu * q / (r**3 + 1e-14)

    def energy(self, q, p):
        q = np.asarray(q)
        p = np.asarray(p)
        r = np.linalg.norm(q)
        return 0.5 * np.dot(p, p) - self.mu / (r + 1e-14)

    def state_labels(self):
        return "q", "p"


SYSTEMS = {
    "Simple Harmonic Oscillator": HarmonicOscillator,
    "Pendulum": Pendulum,
    "Two-Body / Kepler Problem": Kepler2D,
}
