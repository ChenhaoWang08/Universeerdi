from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

Point = Tuple[float, float]


@dataclass(frozen=True)
class RenderScalePolicy:
    meters_per_world_unit: float
    min_body_radius_px: float
    max_body_radius_px: float
    body_radius_scale: float
    fallback_body_radius_px: float = 6.0


def map_physical_position_to_world(position_m: Point, policy: RenderScalePolicy) -> Point:
    if policy.meters_per_world_unit <= 0.0:
        raise ValueError("meters_per_world_unit must be positive")
    return (
        position_m[0] / policy.meters_per_world_unit,
        position_m[1] / policy.meters_per_world_unit,
    )


def map_physical_radius_to_visible_px(
    radius_m: Optional[float],
    policy: RenderScalePolicy,
    *,
    fallback_radius_px: Optional[float] = None,
) -> float:
    if policy.min_body_radius_px <= 0.0:
        raise ValueError("min_body_radius_px must be positive")
    if policy.max_body_radius_px < policy.min_body_radius_px:
        raise ValueError("max_body_radius_px must be >= min_body_radius_px")
    if policy.body_radius_scale <= 0.0:
        raise ValueError("body_radius_scale must be positive")

    if radius_m is None or radius_m <= 0.0:
        base_radius = (
            policy.fallback_body_radius_px
            if fallback_radius_px is None
            else fallback_radius_px
        )
    else:
        base_radius = radius_m * policy.body_radius_scale

    return max(policy.min_body_radius_px, min(policy.max_body_radius_px, base_radius))
