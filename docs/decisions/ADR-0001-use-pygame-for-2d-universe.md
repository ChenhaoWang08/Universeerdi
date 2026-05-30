# ADR-0001: Use Pygame for 2D Universe

## Status

Accepted

## Context

The project needs a simple Python-based way to build an interactive 2D simulator with windowing, input, and rendering support.

## Decision

Use Python plus Pygame for the first interactive viewer and simulator foundation.

## Consequences

- interactive rendering is straightforward to bootstrap
- physics and rendering should stay separated
- tests should avoid display dependency when possible
- real physics should be added in later phases
