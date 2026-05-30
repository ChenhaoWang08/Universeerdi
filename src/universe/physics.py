from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence, Tuple

from .body import Body
from .units import NEWTON_G_M3_KG_S2

ZERO_DISTANCE_EPSILON_M = 1e-3


@dataclass(frozen=True)
class Vector2:
    x: float
    y: float

    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vector2":
        if scalar == 0.0:
            raise ZeroDivisionError("cannot divide vector by zero")
        return Vector2(self.x / scalar, self.y / scalar)

    def squared_magnitude(self) -> float:
        return (self.x * self.x) + (self.y * self.y)

    def magnitude(self) -> float:
        return sqrt(self.squared_magnitude())

    def safe_normalized(self, epsilon: float = 1e-12) -> "Vector2":
        size = self.magnitude()
        if size <= epsilon:
            return Vector2(0.0, 0.0)
        return self / size


@dataclass(frozen=True)
class PhysicsBodyState:
    name: str
    mass_kg: float
    position_m: Vector2
    velocity_m_s: Vector2


def acceleration_from_source(
    target: PhysicsBodyState,
    source: PhysicsBodyState,
    epsilon_m: float = ZERO_DISTANCE_EPSILON_M,
) -> Vector2:
    """Return acceleration on ``target`` caused by ``source`` in SI units.

    Zero or near-zero separation returns a zero vector to avoid unstable force spikes.
    """
    if target is source:
        return Vector2(0.0, 0.0)

    offset = source.position_m - target.position_m
    distance_squared = offset.squared_magnitude()
    if distance_squared <= (epsilon_m * epsilon_m):
        return Vector2(0.0, 0.0)

    direction = offset.safe_normalized()
    magnitude = (NEWTON_G_M3_KG_S2 * source.mass_kg) / distance_squared
    return direction * magnitude


def compute_net_accelerations(
    bodies: Sequence[PhysicsBodyState],
    epsilon_m: float = ZERO_DISTANCE_EPSILON_M,
) -> Tuple[Vector2, ...]:
    accelerations = []
    for target_index, target in enumerate(bodies):
        net = Vector2(0.0, 0.0)
        for source_index, source in enumerate(bodies):
            if target_index == source_index:
                continue
            net = net + acceleration_from_source(target, source, epsilon_m=epsilon_m)
        accelerations.append(net)
    return tuple(accelerations)


def update_velocity(
    velocity_m_s: Vector2, acceleration_m_s2: Vector2, dt_seconds: float
) -> Vector2:
    return velocity_m_s + (acceleration_m_s2 * dt_seconds)


def update_position(position_m: Vector2, velocity_m_s: Vector2, dt_seconds: float) -> Vector2:
    return position_m + (velocity_m_s * dt_seconds)


def step_bodies(
    bodies: Sequence[PhysicsBodyState],
    dt_seconds: float,
    epsilon_m: float = ZERO_DISTANCE_EPSILON_M,
) -> Tuple[PhysicsBodyState, ...]:
    """Advance bodies by one semi-implicit Euler step and return new states."""
    if dt_seconds <= 0.0:
        raise ValueError("dt_seconds must be positive")

    accelerations = compute_net_accelerations(bodies, epsilon_m=epsilon_m)
    next_bodies = []
    for body, acceleration in zip(bodies, accelerations):
        next_velocity = update_velocity(body.velocity_m_s, acceleration, dt_seconds)
        next_position = update_position(body.position_m, next_velocity, dt_seconds)
        next_bodies.append(
            PhysicsBodyState(
                name=body.name,
                mass_kg=body.mass_kg,
                position_m=next_position,
                velocity_m_s=next_velocity,
            )
        )
    return tuple(next_bodies)


def step_placeholder_bodies(
    bodies: Sequence[Body], delta_seconds: float
) -> Tuple[Body, ...]:
    """PR4 keeps viewer placeholder stepping separate from physics foundation code."""
    _ = delta_seconds
    return tuple(bodies)
