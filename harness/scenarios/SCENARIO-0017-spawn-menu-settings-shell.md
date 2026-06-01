# Scenario 0017: Spawn Menu + Settings Shell

## Goal

Verify PR28 UI shell flow:

- right-click background opens spawn menu
- click template opens settings panel shell
- no preview and no spawn happen

## Steps

1. Launch `python3 -m src.main`.
2. Right-click empty background.
3. Confirm spawn menu appears and lists Sun/planets/Black Hole placeholder.
4. Scroll wheel over menu; menu scrolls and camera does not zoom.
5. Click a template row.
6. Confirm menu closes and read-only settings panel opens.
7. Confirm panel shows default fields and derived volume/density.
8. Click `Set`; confirm no preview/spawn, only pending note.
9. Click `Cancel`; panel closes and draft is discarded.

## Expected

- UI shell works as above.
- Existing controls keep behavior.
- Physics/simulation state remains unchanged by shell interactions.
