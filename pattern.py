import numpy as np


class RadiationPattern:
    """  """
    def __init__(self):
        super(RadiationPattern, self).__init__()

        self._c = 3 * np.power(10, 8)
        self._f = 26 * np.power(10, 6)
        self._lambda = self._c / self._f
        self._k = 2 * (np.pi / self._lambda)
        self._len = 2 * self._lambda
        self._phi_cap = 35 * (np.pi / 180)

    def _f0(self, theta, phi):
        _left_side = self._k * self._len * (1 - np.sin(theta) * np.sin(self._phi_cap + phi))
        _right_side = self._k * self._len * (1 - np.sin(theta) * np.sin(self._phi_cap - phi))
        return np.sinc(_left_side / 2) * np.sinc(_right_side / 2)

    def _f1(self, theta, phi):
        return np.power(np.cos(theta) * np.sin(phi) * self._f0(theta, phi), 2)

    def _f2(self, theta, phi):
        return np.power((np.cos(phi) - np.sin(theta) * np.sin(self._phi_cap)) * self._f0(theta, phi), 2)

    def _f3(self, theta, phi):
        return self._f1(theta, phi) + self._f2(theta, phi)

    def set_phi(self, value):
        self._phi_cap = value * (np.pi / 180)

    def get_theta_r(self):
        _theta = np.arange(-np.pi, np.pi, 0.01)
        _r = self._f3(_theta, np.pi)
        return _theta, _r
