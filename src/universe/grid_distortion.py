from __future__ import annotations

from dataclasses import dataclass, replace
from math import sqrt
from typing import Mapping, Sequence, Tuple

from .body import Body
from .solar_system_data import SUN

Point = Tuple[float, float]

DISTORTION_CENTER_EPSILON = 1e-12
DEFAULT_REFERENCE_MASS_KG = SUN.mass_kg


@dataclass(frozen=True)
class GridDistortionState:
    enabled: bool = False
    strength: float = 1.0


@dataclass(frozen=True)
class DistortionSource:
    name: str
    position: Point
    mass_kg: float


@dataclass(frozen=True)
class GridWarpPolicy:
    reference_mass_kg: float = DEFAULT_REFERENCE_MASS_KG
    strength: float = 1.0
    mass_exponent: float = 0.35
    min_visible_relative_mass: float = 1e-4
    overview_small_body_cutoff: float = 1e-4
    base_influence_radius_world: float = 800.0
    min_influence_radius_world: float = 20.0
    max_influence_radius_world: float = 900.0
    max_displacement_world: float = 45.0
    local_zoom_threshold: float = 2.0
    local_zoom_fade_start: float = 1.2
    local_zoom_fade_full: float = 2.4
    local_min_visible_relative_mass: float = 1e-7
    local_visual_factor_floor: float = 0.18
    local_influence_radius_px: float = 220.0
    local_max_displacement_px: float = 34.0
    soft_core_px: float = 24.0
    smooth_falloff_power: float = 1.0
    max_sources_per_point: int = 2


@dataclass(frozen=True)
class SourceInfluence:
    displacement: Point
    strength: float


def toggle_grid_distortion(state: GridDistortionState) -> GridDistortionState:
    return replace(state, enabled=not state.enabled)


def grid_distortion_status_text(state: GridDistortionState) -> str:
    if not state.enabled:
        return "Grid warp: off"
    return f"Grid warp: on x{state.strength:.1f}"


def distort_grid_point(
    point: Point,
    sources: Sequence[DistortionSource],
    *,
    policy: GridWarpPolicy,
    camera_zoom: float,
) -> Point:
    validate_grid_warp_policy(policy)
    if camera_zoom <= 0.0:
        raise ValueError("camera_zoom must be positive")
    if not sources or policy.strength == 0.0 or policy.max_displacement_world == 0.0:
        return point

    point_x, point_y = point
    influences: list[SourceInfluence] = []
    local_zoom_fade = compute_local_zoom_fade(camera_zoom, policy)
    soft_core_world = compute_soft_core_world(camera_zoom, policy)
    local_max_displacement_world = compute_local_max_displacement_world(camera_zoom, policy)
    total_displacement_cap_world = max(policy.max_displacement_world, local_max_displacement_world)

    for source in sources:
        relative_mass = compute_relative_mass(source.mass_kg, policy)
        source_kind = classify_warp_source(
            relative_mass=relative_mass,
            camera_zoom=camera_zoom,
            policy=policy,
        )
        if source_kind == "hidden":
            continue

        is_local = source_kind == "local"
        if is_local and local_zoom_fade <= 0.0:
            continue

        visual_mass_factor = compute_visual_mass_factor(
            source.mass_kg,
            policy,
            allow_local=is_local,
        )
        if is_local:
            visual_mass_factor *= local_zoom_fade
            influence_radius_world = compute_local_influence_radius_world(camera_zoom, policy)
            source_max_displacement_world = local_max_displacement_world
        else:
            influence_radius_world = compute_influence_radius_world(visual_mass_factor, policy)
            source_max_displacement_world = policy.max_displacement_world

        if influence_radius_world <= 0.0:
            continue

        source_x, source_y = source.position
        delta_x = point_x - source_x
        delta_y = point_y - source_y
        distance = sqrt((delta_x * delta_x) + (delta_y * delta_y))
        if distance >= influence_radius_world:
            continue

        soft_distance = sqrt((distance * distance) + (soft_core_world * soft_core_world))
        if soft_distance <= DISTORTION_CENTER_EPSILON:
            continue

        unit_x = delta_x / soft_distance
        unit_y = delta_y / soft_distance
        falloff = compute_smooth_falloff(distance, influence_radius_world, policy)
        if falloff <= 0.0:
            continue

        raw_amount = (
            falloff
            * visual_mass_factor
            * policy.strength
            * source_max_displacement_world
        )
        amount = min(source_max_displacement_world, raw_amount)
        displacement = (-unit_x * amount, -unit_y * amount)
        influences.append(SourceInfluence(displacement=displacement, strength=amount))

    if not influences:
        return point

    top_influences = sorted(
        influences,
        key=lambda influence: influence.strength,
        reverse=True,
    )[: policy.max_sources_per_point]

    displacement_x = sum(influence.displacement[0] for influence in top_influences)
    displacement_y = sum(influence.displacement[1] for influence in top_influences)
    total_displacement = sqrt((displacement_x * displacement_x) + (displacement_y * displacement_y))
    if total_displacement > total_displacement_cap_world and total_displacement > 0.0:
        clamp = total_displacement_cap_world / total_displacement
        displacement_x *= clamp
        displacement_y *= clamp

    return (point_x + displacement_x, point_y + displacement_y)


def build_distortion_sources_from_bodies(
    bodies: Sequence[Body],
    *,
    effective_masses_by_name: Mapping[str, float] | None = None,
) -> Tuple[DistortionSource, ...]:
    sources = []
    for body in bodies:
        base_mass = body.data.mass_kg
        effective_mass = (
            effective_masses_by_name.get(body.name, base_mass)
            if effective_masses_by_name is not None
            else base_mass
        )
        if effective_mass <= 0.0:
            continue
        sources.append(
            DistortionSource(
                name=body.name,
                position=body.position,
                mass_kg=effective_mass,
            )
        )
    return tuple(sources)


def validate_grid_warp_policy(policy: GridWarpPolicy) -> None:
    if policy.reference_mass_kg <= 0.0:
        raise ValueError("reference_mass_kg must be positive")
    if policy.strength < 0.0:
        raise ValueError("strength must be non-negative")
    if policy.mass_exponent <= 0.0:
        raise ValueError("mass_exponent must be positive")
    if policy.min_visible_relative_mass < 0.0:
        raise ValueError("min_visible_relative_mass must be non-negative")
    if policy.overview_small_body_cutoff < 0.0:
        raise ValueError("overview_small_body_cutoff must be non-negative")
    if policy.base_influence_radius_world <= 0.0:
        raise ValueError("base_influence_radius_world must be positive")
    if policy.min_influence_radius_world < 0.0:
        raise ValueError("min_influence_radius_world must be non-negative")
    if policy.max_influence_radius_world < policy.min_influence_radius_world:
        raise ValueError("max_influence_radius_world must be >= min_influence_radius_world")
    if policy.max_displacement_world < 0.0:
        raise ValueError("max_displacement_world must be non-negative")
    if policy.local_zoom_threshold <= 0.0:
        raise ValueError("local_zoom_threshold must be positive")
    if policy.local_zoom_fade_start <= 0.0:
        raise ValueError("local_zoom_fade_start must be positive")
    if policy.local_zoom_fade_full <= policy.local_zoom_fade_start:
        raise ValueError("local_zoom_fade_full must be > local_zoom_fade_start")
    if policy.local_min_visible_relative_mass < 0.0:
        raise ValueError("local_min_visible_relative_mass must be non-negative")
    if policy.local_visual_factor_floor < 0.0:
        raise ValueError("local_visual_factor_floor must be non-negative")
    if policy.local_influence_radius_px <= 0.0:
        raise ValueError("local_influence_radius_px must be positive")
    if policy.local_max_displacement_px < 0.0:
        raise ValueError("local_max_displacement_px must be non-negative")
    if policy.soft_core_px < 0.0:
        raise ValueError("soft_core_px must be non-negative")
    if policy.smooth_falloff_power <= 0.0:
        raise ValueError("smooth_falloff_power must be positive")
    if policy.max_sources_per_point < 1:
        raise ValueError("max_sources_per_point must be >= 1")


def compute_relative_mass(mass_kg: float, policy: GridWarpPolicy) -> float:
    if mass_kg <= 0.0:
        return 0.0
    return mass_kg / policy.reference_mass_kg


def compute_visual_mass_factor(
    mass_kg: float,
    policy: GridWarpPolicy,
    *,
    allow_local: bool = False,
) -> float:
    relative_mass = compute_relative_mass(mass_kg, policy)
    if relative_mass <= 0.0:
        return 0.0
    if allow_local:
        if relative_mass < policy.local_min_visible_relative_mass:
            return 0.0
        return max(relative_mass**policy.mass_exponent, policy.local_visual_factor_floor)

    if relative_mass < policy.min_visible_relative_mass:
        return 0.0
    return relative_mass**policy.mass_exponent


def compute_influence_radius_world(
    visual_mass_factor: float,
    policy: GridWarpPolicy,
) -> float:
    if visual_mass_factor <= 0.0:
        return 0.0
    raw = policy.base_influence_radius_world * visual_mass_factor
    return max(
        policy.min_influence_radius_world,
        min(policy.max_influence_radius_world, raw),
    )


def should_render_distortion_source(
    *,
    relative_mass: float,
    camera_zoom: float,
    policy: GridWarpPolicy,
) -> bool:
    if relative_mass <= 0.0:
        return False
    return classify_warp_source(
        relative_mass=relative_mass,
        camera_zoom=camera_zoom,
        policy=policy,
    ) != "hidden"


def classify_warp_source(
    *,
    relative_mass: float,
    camera_zoom: float,
    policy: GridWarpPolicy,
) -> str:
    if relative_mass >= policy.min_visible_relative_mass:
        return "global"
    if (
        camera_zoom >= policy.local_zoom_fade_start
        and relative_mass >= policy.local_min_visible_relative_mass
    ):
        return "local"
    return "hidden"


def compute_local_influence_radius_world(
    camera_zoom: float,
    policy: GridWarpPolicy,
) -> float:
    if camera_zoom <= 0.0:
        raise ValueError("camera_zoom must be positive")
    return policy.local_influence_radius_px / camera_zoom


def compute_local_max_displacement_world(
    camera_zoom: float,
    policy: GridWarpPolicy,
) -> float:
    if camera_zoom <= 0.0:
        raise ValueError("camera_zoom must be positive")
    return policy.local_max_displacement_px / camera_zoom


def compute_soft_core_world(
    camera_zoom: float,
    policy: GridWarpPolicy,
) -> float:
    if camera_zoom <= 0.0:
        raise ValueError("camera_zoom must be positive")
    return policy.soft_core_px / camera_zoom


def smoothstep(t: float) -> float:
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    return t * t * (3.0 - (2.0 * t))


def smoothstep_between(start: float, end: float, value: float) -> float:
    if end <= start:
        raise ValueError("end must be > start")
    normalized = (value - start) / (end - start)
    return smoothstep(normalized)


def compute_local_zoom_fade(
    camera_zoom: float,
    policy: GridWarpPolicy,
) -> float:
    return smoothstep_between(
        policy.local_zoom_fade_start,
        policy.local_zoom_fade_full,
        camera_zoom,
    )


def compute_smooth_falloff(
    distance: float,
    influence_radius_world: float,
    policy: GridWarpPolicy,
) -> float:
    if influence_radius_world <= 0.0:
        raise ValueError("influence_radius_world must be positive")
    if distance >= influence_radius_world:
        return 0.0
    t = distance / influence_radius_world
    return (1.0 - smoothstep(t)) ** policy.smooth_falloff_power
