from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .body import Body, CelestialBody
from .physics import PhysicsBodyState, Vector2, step_bodies

# Demo-only scale that converts SI meter positions into viewer world units.
DEMO_METERS_TO_WORLD = 0.0015


@dataclass(frozen=True)
class ControlledDemoState:
    physics_bodies: Tuple[PhysicsBodyState, ...]


DEMO_ANCHOR = CelestialBody(
    name="DemoAnchor",
    category="star",
    mass_kg=8.0e23,
    mean_radius_m=45_000.0,
    mean_orbital_radius_m=0.0,
    orbital_period_s=0.0,
    rotation_period_s=0.0,
    color_rgb=(246, 186, 112),
    visual_radius_px=16.0,
    source_note=(
        "Controlled demo body for PR5 physics visualization. Not real solar-system data."
    ),
)

DEMO_RUNNER_A = CelestialBody(
    name="DemoRunnerA",
    category="terrestrial_planet",
    mass_kg=5.0e20,
    mean_radius_m=12_000.0,
    mean_orbital_radius_m=120_000.0,
    orbital_period_s=0.0,
    rotation_period_s=0.0,
    color_rgb=(124, 184, 250),
    visual_radius_px=9.0,
    source_note=(
        "Controlled demo body for PR5 physics visualization. Not real solar-system data."
    ),
)

DEMO_RUNNER_B = CelestialBody(
    name="DemoRunnerB",
    category="terrestrial_planet",
    mass_kg=2.0e20,
    mean_radius_m=10_000.0,
    mean_orbital_radius_m=180_000.0,
    orbital_period_s=0.0,
    rotation_period_s=0.0,
    color_rgb=(167, 226, 183),
    visual_radius_px=8.0,
    source_note=(
        "Controlled demo body for PR5 physics visualization. Not real solar-system data."
    ),
)

DEMO_BODY_DATA_BY_NAME: Dict[str, CelestialBody] = {
    DEMO_ANCHOR.name: DEMO_ANCHOR,
    DEMO_RUNNER_A.name: DEMO_RUNNER_A,
    DEMO_RUNNER_B.name: DEMO_RUNNER_B,
}


def create_controlled_demo_state() -> ControlledDemoState:
    """Create PR5 demo-only SI physics states (not real solar-system states)."""
    return ControlledDemoState(
        physics_bodies=(
            PhysicsBodyState(
                name=DEMO_ANCHOR.name,
                mass_kg=DEMO_ANCHOR.mass_kg,
                position_m=Vector2(0.0, 0.0),
                velocity_m_s=Vector2(0.0, 0.0),
            ),
            PhysicsBodyState(
                name=DEMO_RUNNER_A.name,
                mass_kg=DEMO_RUNNER_A.mass_kg,
                position_m=Vector2(120_000.0, 0.0),
                velocity_m_s=Vector2(0.0, 21_000.0),
            ),
            PhysicsBodyState(
                name=DEMO_RUNNER_B.name,
                mass_kg=DEMO_RUNNER_B.mass_kg,
                position_m=Vector2(-180_000.0, 0.0),
                velocity_m_s=Vector2(0.0, -15_000.0),
            ),
        )
    )


def step_controlled_demo_state(
    state: ControlledDemoState, dt_seconds: float
) -> ControlledDemoState:
    return ControlledDemoState(
        physics_bodies=step_bodies(state.physics_bodies, dt_seconds=dt_seconds)
    )


def controlled_demo_to_render_bodies(state: ControlledDemoState) -> Tuple[Body, ...]:
    return tuple(
        Body(
            data=DEMO_BODY_DATA_BY_NAME[physics_body.name],
            world_x=physics_body.position_m.x * DEMO_METERS_TO_WORLD,
            world_y=physics_body.position_m.y * DEMO_METERS_TO_WORLD,
        )
        for physics_body in state.physics_bodies
    )
