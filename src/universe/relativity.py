from __future__ import annotations

from math import hypot, inf, sqrt

SPEED_OF_LIGHT_M_S = 299_792_458.0


def lorentz_factor(speed_m_s: float) -> float:
    """Return Lorentz gamma for a scalar speed in m/s.

    Behavior policy:
    - speed < 0: raise ValueError
    - speed >= c: return +inf
    """
    if speed_m_s < 0.0:
        raise ValueError("speed_m_s must be non-negative")
    if speed_m_s >= SPEED_OF_LIGHT_M_S:
        return inf

    beta_squared = (speed_m_s / SPEED_OF_LIGHT_M_S) ** 2
    return 1.0 / sqrt(1.0 - beta_squared)


def lorentz_factor_from_velocity(vx_m_s: float, vy_m_s: float) -> float:
    speed_m_s = hypot(vx_m_s, vy_m_s)
    return lorentz_factor(speed_m_s)
