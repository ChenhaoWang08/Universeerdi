from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Tuple

from .body import Body
from .physics import PhysicsBodyState, Vector2, step_bodies
from .render_scale import (
    RenderScalePolicy,
    map_physical_position_to_world,
    map_physical_radius_to_visible_px,
)
from .solar_system_data import SOLAR_SYSTEM_BODIES, SOLAR_SYSTEM_BODY_MAP
from .units import NEWTON_G_M3_KG_S2

SOLAR_SYSTEM_RENDER_SCALE_POLICY = RenderScalePolicy(
    meters_per_world_unit=1_000_000_000.0,
    min_body_radius_px=5.0,
    max_body_radius_px=28.0,
    body_radius_scale=3.5e-7,
)


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
        _render_body_from_physics(physics_body)
        for physics_body in state.physics_bodies
    )


def _render_body_from_physics(physics_body: PhysicsBodyState) -> Body:
    body_data = SOLAR_SYSTEM_BODY_MAP[physics_body.name]
    world_x, world_y = map_physical_position_to_world(
        (physics_body.position_m.x, physics_body.position_m.y),
        SOLAR_SYSTEM_RENDER_SCALE_POLICY,
    )
    render_radius_px = map_physical_radius_to_visible_px(
        body_data.mean_radius_m,
        SOLAR_SYSTEM_RENDER_SCALE_POLICY,
        fallback_radius_px=body_data.visual_radius_px,
    )
    return Body(
        data=body_data,
        world_x=world_x,
        world_y=world_y,
        render_radius_px=render_radius_px,
    )
