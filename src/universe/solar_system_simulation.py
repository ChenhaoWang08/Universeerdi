from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Tuple

from .body import Body
from .physics import PhysicsBodyState, Vector2, step_bodies
from .solar_system_data import SOLAR_SYSTEM_BODIES, SOLAR_SYSTEM_BODY_MAP
from .units import NEWTON_G_M3_KG_S2

# Real SI distances are very large; this scale keeps initial bodies visible in the viewer.
SOLAR_SYSTEM_METERS_TO_WORLD = 1e-9


@dataclass(frozen=True)
class SolarSystemSimulationState:
    physics_bodies: Tuple[PhysicsBodyState, ...]


def build_solar_system_body_states() -> Tuple[PhysicsBodyState, ...]:
    """Build deterministic SI initial conditions from the existing dataset.

    Policy for PR9:
    - Sun starts at origin with zero velocity.
    - Planets start on +x using mean orbital radius.
    - Planet initial velocity is +y using sqrt(G * M_sun / r) estimate.
    """
    sun = SOLAR_SYSTEM_BODY_MAP["Sun"]
    states = []
    for body in SOLAR_SYSTEM_BODIES:
        if body.name == "Sun":
            position = Vector2(0.0, 0.0)
            velocity = Vector2(0.0, 0.0)
        else:
            radius_m = body.mean_orbital_radius_m
            position = Vector2(radius_m, 0.0)
            if radius_m > 0.0 and sun.mass_kg > 0.0:
                speed_m_s = sqrt((NEWTON_G_M3_KG_S2 * sun.mass_kg) / radius_m)
            else:
                # Fallback for malformed inputs: keep deterministic zero velocity.
                speed_m_s = 0.0
            velocity = Vector2(0.0, speed_m_s)

        states.append(
            PhysicsBodyState(
                name=body.name,
                mass_kg=body.mass_kg,
                position_m=position,
                velocity_m_s=velocity,
            )
        )
    return tuple(states)


def create_solar_system_simulation_state() -> SolarSystemSimulationState:
    return SolarSystemSimulationState(physics_bodies=build_solar_system_body_states())


def step_solar_system_simulation_state(
    state: SolarSystemSimulationState,
    dt_seconds: float,
) -> SolarSystemSimulationState:
    return SolarSystemSimulationState(
        physics_bodies=step_bodies(state.physics_bodies, dt_seconds=dt_seconds)
    )


def solar_system_to_render_bodies(state: SolarSystemSimulationState) -> Tuple[Body, ...]:
    return tuple(
        Body(
            data=SOLAR_SYSTEM_BODY_MAP[physics_body.name],
            world_x=physics_body.position_m.x * SOLAR_SYSTEM_METERS_TO_WORLD,
            world_y=physics_body.position_m.y * SOLAR_SYSTEM_METERS_TO_WORLD,
        )
        for physics_body in state.physics_bodies
    )
