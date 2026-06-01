from __future__ import annotations

from dataclasses import dataclass

from .units import AU_M


@dataclass(frozen=True)
class ScaleRuler:
    pixel_length: int
    distance_m: float
    label: str


def format_distance_label(distance_m: float) -> str:
    if distance_m < 0.0:
        raise ValueError("distance_m must be non-negative")
    if distance_m < 1_000.0:
        return f"{int(round(distance_m)):,} m"

    distance_au = distance_m / AU_M
    if distance_au >= 0.1:
        if abs(distance_au - round(distance_au)) <= 1e-9:
            return f"{int(round(distance_au)):,} AU"
        if distance_au < 1.0:
            return f"{distance_au:.2f} AU"
        if distance_au < 10.0:
            return f"{distance_au:.1f} AU"
        return f"{distance_au:.0f} AU"

    distance_km = distance_m / 1_000.0
    if abs(distance_km - round(distance_km)) <= 1e-9:
        return f"{int(round(distance_km)):,} km"
    if distance_km < 10.0:
        return f"{distance_km:.2f} km"
    if distance_km < 100.0:
        return f"{distance_km:.1f} km"
    return f"{distance_km:.0f} km"


def build_scale_ruler(
    *,
    camera_zoom: float,
    meters_per_world_unit: float,
    target_pixel_length: int = 120,
) -> ScaleRuler:
    if camera_zoom <= 0.0:
        raise ValueError("camera_zoom must be positive")
    if meters_per_world_unit <= 0.0:
        raise ValueError("meters_per_world_unit must be positive")
    if target_pixel_length <= 0:
        raise ValueError("target_pixel_length must be positive")

    world_units_visible_in_ruler = target_pixel_length / camera_zoom
    distance_m = world_units_visible_in_ruler * meters_per_world_unit
    return ScaleRuler(
        pixel_length=target_pixel_length,
        distance_m=distance_m,
        label=format_distance_label(distance_m),
    )
