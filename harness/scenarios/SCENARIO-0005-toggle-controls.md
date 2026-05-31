# SCENARIO-0005: In-Window Overlay Toggle Controls

## Goal

Verify that Labels and Trails toggles are clickable in-window controls and affect rendering visibility only.

## Steps

1. Launch the viewer.
2. Confirm Labels and Trails controls are visible in the top-left overlay area.
3. Click Labels and confirm label rendering toggles.
4. Click Trails and confirm trail rendering toggles.
5. Click controls and confirm camera does not start dragging.
6. Drag background outside controls and confirm camera still pans.
7. Scroll wheel and confirm zoom still works.

## Expected Result

- both toggles are visible and clickable
- overlays toggle on/off without changing simulation correctness
- clicking UI controls does not pan camera
- camera drag and zoom remain functional outside control interactions
