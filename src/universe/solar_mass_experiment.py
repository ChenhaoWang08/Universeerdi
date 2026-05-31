from __future__ import annotations

from dataclasses import dataclass, replace

DEFAULT_SOLAR_MASS_MULTIPLIER = 1.0
DEFAULT_MIN_SOLAR_MASS_MULTIPLIER = 1.0
DEFAULT_MAX_SOLAR_MASS_MULTIPLIER = 50.0
DEFAULT_SOLAR_MASS_MULTIPLIER_STEP = 1.0


@dataclass(frozen=True)
class SolarMassExperimentState:
    solar_mass_multiplier: float = DEFAULT_SOLAR_MASS_MULTIPLIER
    min_multiplier: float = DEFAULT_MIN_SOLAR_MASS_MULTIPLIER
    max_multiplier: float = DEFAULT_MAX_SOLAR_MASS_MULTIPLIER
    step: float = DEFAULT_SOLAR_MASS_MULTIPLIER_STEP


def increase_solar_mass_multiplier(
    state: SolarMassExperimentState,
) -> SolarMassExperimentState:
    return replace(
        state,
        solar_mass_multiplier=min(
            state.max_multiplier,
            state.solar_mass_multiplier + state.step,
        ),
    )


def decrease_solar_mass_multiplier(
    state: SolarMassExperimentState,
) -> SolarMassExperimentState:
    return replace(
        state,
        solar_mass_multiplier=max(
            state.min_multiplier,
            state.solar_mass_multiplier - state.step,
        ),
    )


def reset_solar_mass_multiplier(
    state: SolarMassExperimentState,
) -> SolarMassExperimentState:
    return replace(state, solar_mass_multiplier=DEFAULT_SOLAR_MASS_MULTIPLIER)


def solar_mass_experiment_status_text(
    state: SolarMassExperimentState,
    *,
    active_body_count: int,
) -> str:
    return (
        f"Sun Gravity: x{state.solar_mass_multiplier:.1f} | "
        f"Absorb: ON | Bodies: {active_body_count}"
    )
