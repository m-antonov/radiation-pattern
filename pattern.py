import numpy as np
import matplotlib.pyplot as plt

_c = 3 * np.power(10, 8)
_f = 26 * np.power(10, 6)
_lambda = _c / _f
_k = 2 * (np.pi / _lambda)
_len = 2 * _lambda
_phi_cap = 35 * (np.pi / 180)


def _f0(theta, phi):
    _left_side = _k * _len * (1 - np.sin(theta) * np.sin(_phi_cap + phi))
    _right_side = _k * _len * (1 - np.sin(theta) * np.sin(_phi_cap - phi))
    return np.sinc(_left_side / 2) * np.sinc(_right_side / 2)


def _f1(theta, phi):
    return np.power(np.cos(theta) * np.sin(phi) * _f0(theta, phi), 2)


def _f2(theta, phi):
    return np.power((np.cos(phi) - np.sin(theta) * np.sin(_phi_cap)) * _f0(theta, phi), 2)


def _f3(theta, phi):
    return _f1(theta, phi) + _f2(theta, phi)


_theta = np.arange(-np.pi, np.pi, 0.01)
_r = _f3(_theta, np.pi)

ax = plt.subplot(111, projection='polar')
ax.plot(_theta, _r)
plt.show()
