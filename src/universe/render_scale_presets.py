from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Dict, Literal

from .render_scale import RenderScalePolicy

RenderScalePresetName = Literal["readable", "realistic", "overview"]

READABLE_RENDER_SCALE_POLICY = RenderScalePolicy(
    meters_per_world_unit=250_000_000.0,
    min_body_radius_px=0.8,
    max_body_radius_px=90.0,
    body_radius_scale=1.0 / 4_000_000.0,
    fallback_body_radius_px=6.0,
)

REALISTIC_RENDER_SCALE_POLICY = RenderScalePolicy(
    meters_per_world_unit=250_000_000.0,
    min_body_radius_px=0.05,
    max_body_radius_px=10_000.0,
    body_radius_scale=1.0 / 250_000_000.0,
    fallback_body_radius_px=0.05,
)

OVERVIEW_RENDER_SCALE_POLICY = RenderScalePolicy(
    meters_per_world_unit=1_000_000_000.0,
    min_body_radius_px=2.0,
    max_body_radius_px=60.0,
    body_radius_scale=1.0 / 6_000_000.0,
    fallback_body_radius_px=6.0,
)

RENDER_SCALE_PRESET_POLICIES: Dict[RenderScalePresetName, RenderScalePolicy] = {
    "readable": READABLE_RENDER_SCALE_POLICY,
    "realistic": REALISTIC_RENDER_SCALE_POLICY,
    "overview": OVERVIEW_RENDER_SCALE_POLICY,
}

RENDER_SCALE_PRESET_CYCLE = ("readable", "realistic", "overview")
RENDER_SCALE_PRESET_EXPLANATIONS: Dict[RenderScalePresetName, str] = {
    "readable": "Scale note: readable = enlarged bodies",
    "realistic": "Scale note: realistic = closer real proportions",
    "overview": "Scale note: overview = compressed layout",
}


@dataclass(frozen=True)
class RenderScalePresetState:
    preset: RenderScalePresetName = "readable"


def cycle_render_scale_preset(state: RenderScalePresetState) -> RenderScalePresetState:
    current_index = RENDER_SCALE_PRESET_CYCLE.index(state.preset)
    next_index = (current_index + 1) % len(RENDER_SCALE_PRESET_CYCLE)
    return replace(state, preset=RENDER_SCALE_PRESET_CYCLE[next_index])


def render_scale_policy_for_preset(preset: RenderScalePresetName) -> RenderScalePolicy:
    return RENDER_SCALE_PRESET_POLICIES[preset]


def render_scale_preset_status_text(state: RenderScalePresetState) -> str:
    return f"Scale: {state.preset}"


def render_scale_preset_explanation(preset: RenderScalePresetName) -> str:
    return RENDER_SCALE_PRESET_EXPLANATIONS[preset]
