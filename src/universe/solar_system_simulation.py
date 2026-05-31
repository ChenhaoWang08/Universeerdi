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

SUN_NAME = "Sun"
BASELINE_SOLAR_MASS_KG = SOLAR_SYSTEM_BODY_MAP[SUN_NAME].mass_kg
SUN_ABSORPTION_RADIUS_M = SOLAR_SYSTEM_BODY_MAP[SUN_NAME].mean_radius_m

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
    _ = BASELINE_SOLAR_MASS_KG
    states = []
    for body in SOLAR_SYSTEM_BODIES:
        if body.name == SUN_NAME:
            position = Vector2(0.0, 0.0)
            velocity = Vector2(0.0, 0.0)
        else:
            radius_m = body.mean_orbital_radius_m
            position = Vector2(radius_m, 0.0)
            if radius_m > 0.0 and BASELINE_SOLAR_MASS_KG > 0.0:
                speed_m_s = sqrt((NEWTON_G_M3_KG_S2 * BASELINE_SOLAR_MASS_KG) / radius_m)
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
    *,
    solar_mass_multiplier: float = 1.0,
    absorb_into_sun: bool = True,
) -> SolarSystemSimulationState:
    if solar_mass_multiplier <= 0.0:
        raise ValueError("solar_mass_multiplier must be positive")

    stepping_bodies = _with_effective_solar_mass(
        state.physics_bodies, solar_mass_multiplier=solar_mass_multiplier
    )
    stepped = step_bodies(stepping_bodies, dt_seconds=dt_seconds)
    restored = _with_baseline_solar_mass(stepped)
    if absorb_into_sun:
        restored = _apply_solar_absorption(restored)
    return SolarSystemSimulationState(
        physics_bodies=restored
    )


def solar_system_to_render_bodies(
    state: SolarSystemSimulationState,
    policy: RenderScalePolicy = SOLAR_SYSTEM_RENDER_SCALE_POLICY,
) -> Tuple[Body, ...]:
    return tuple(
        _render_body_from_physics(physics_body, policy)
        for physics_body in state.physics_bodies
    )


def _render_body_from_physics(
    physics_body: PhysicsBodyState,
    policy: RenderScalePolicy,
) -> Body:
    body_data = SOLAR_SYSTEM_BODY_MAP[physics_body.name]
    world_x, world_y = map_physical_position_to_world(
        (physics_body.position_m.x, physics_body.position_m.y),
        policy,
    )
    render_radius_px = map_physical_radius_to_visible_px(
        body_data.mean_radius_m,
        policy,
        fallback_radius_px=body_data.visual_radius_px,
    )
    return Body(
        data=body_data,
        world_x=world_x,
        world_y=world_y,
        render_radius_px=render_radius_px,
    )


def _with_effective_solar_mass(
    bodies: Tuple[PhysicsBodyState, ...], *, solar_mass_multiplier: float
) -> Tuple[PhysicsBodyState, ...]:
    next_bodies = []
    for body in bodies:
        if body.name == SUN_NAME:
            next_bodies.append(
                PhysicsBodyState(
                    name=body.name,
                    mass_kg=BASELINE_SOLAR_MASS_KG * solar_mass_multiplier,
                    position_m=body.position_m,
                    velocity_m_s=body.velocity_m_s,
                )
            )
        else:
            next_bodies.append(body)
    return tuple(next_bodies)


def _with_baseline_solar_mass(
    bodies: Tuple[PhysicsBodyState, ...],
) -> Tuple[PhysicsBodyState, ...]:
    next_bodies = []
    for body in bodies:
        if body.name == SUN_NAME:
            next_bodies.append(
                PhysicsBodyState(
                    name=body.name,
                    mass_kg=BASELINE_SOLAR_MASS_KG,
                    position_m=body.position_m,
                    velocity_m_s=body.velocity_m_s,
                )
            )
        else:
            next_bodies.append(body)
    return tuple(next_bodies)


def _apply_solar_absorption(
    bodies: Tuple[PhysicsBodyState, ...],
) -> Tuple[PhysicsBodyState, ...]:
    sun = next((body for body in bodies if body.name == SUN_NAME), None)
    if sun is None:
        return bodies

    kept_bodies = []
    radius_squared = SUN_ABSORPTION_RADIUS_M * SUN_ABSORPTION_RADIUS_M
    for body in bodies:
        if body.name == SUN_NAME:
            kept_bodies.append(body)
            continue
        offset = body.position_m - sun.position_m
        if offset.squared_magnitude() <= radius_squared:
            continue
        kept_bodies.append(body)
    return tuple(kept_bodies)
