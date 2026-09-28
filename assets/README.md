# Forklift Certified — original asset pack

A modular starter asset pack for the **2D, interval-overlap version** of Forklift Certified. Matches the cream / charcoal / pastel warehouse direction in `../mockups/forklift-certified.svg`.

**Included:** 111 SVG game assets, 16 synthesized WAV sound effects, a visual contact sheet, palette, UI theme metadata, asset manifest, and a reproducible generator. No downloads, stock illustrations, external sound samples, or paid asset dependencies.

Open **`contact-sheet.svg`** in a browser to browse the artwork. The contact sheet is a reference, not a runtime texture.

## Inventory

| Folder | Contents / use |
|---|---|
| `sprites/crates/` | Wood + six player-colored crates; separate crack overlay |
| `sprites/debris/` | Three cosmetic wood fragments |
| `sprites/forklift/` | Forklift body and separate rotating wheel |
| `sprites/players/` | Six player colors × neutral, panic, smug expressions |
| `sprites/props/` | Pallet, lamp, traffic cone, warning sign |
| `environment/` | Repeating wall, concrete, hazard stripe; optional warehouse backdrop |
| `ui/` | Nine-slice panels, five button states, keycap, turn pointer, support interval, sweep rail, drop guide, penalty pip |
| `ui/icons/` | Twenty icons in dark and light variants: navigation, audio, connection, lobby, results, settings |
| `fx/` | Six dust frames, four impact frames, shadow, six confetti colors |
| `audio/sfx/` | UI, lobby, turn, countdown, drop, landing, collapse, timeout, results, forklift movement |

`manifest.json` lists each runtime asset, dimensions or audio metadata, intended usage, and normalized pivots. Collider and assembly details appear in the relevant asset descriptions. `palette.json` contains colors; `ui/theme.json` contains sizing and animation hints.

## Import and assembly

### Godot 4

- Import SVG files as textures. They are vector sources, but Godot rasterizes them on import; select suitable import scale for your target display resolution.
- Use `Sprite2D` for crates, props, forklift, and avatars. Use `TextureRect` / `StyleBoxTexture` for UI.
- Panels and buttons use **18px nine-slice margins**; keycaps use **14px**. Metadata is informational, not an automatically installed Godot theme.
- Use a 1200×760 design reference with responsive anchors / containers. This is not a requirement to ship at that resolution.
- All individual sprites have transparent backgrounds. No external SVG fonts, filters, linked images, or JavaScript are required.
- WAVs are mono, 44.1kHz, signed 16-bit PCM, nonlooping. Route through separate UI and game-SFX buses and expose volume controls.
- Exclude `generate.py`, this documentation, and `contact-sheet.svg` from runtime export if not needed.

### Other engines

SVG-capable engines can use these sources directly, subject to their renderer's support. If an engine requires PNG, rasterize with a vector graphics tool at the needed dimensions. **PNG exports and engine-specific scene/resource files are not included.**

### Crate geometry: important

A crate texture is **208×74**, with the intended gameplay rectangle at **(4, 4, 200, 66)**. The extra border is artwork padding. Position stacking surfaces using the gameplay rectangle, not the full texture height.

Use mathematical interval overlap to validate drops. The screenshot's green support strip and dashed guides are overlays driven by game state. Decide the precise surviving-width rule in gameplay code; no asset prescribes it.

Keep intact crates at a consistent visual scale. If the game clips unsupported sections, implement clipping / fragment spawning in code. Arbitrarily stretching the whole crate will distort the label and planks.

For a centered sprite, the gameplay rectangle is `x = -100…100`, `y = -33…33`. A centered crate resting on surface `Y` has center `Y - 33`. A pallet's top surface is at local `y = 4` in its 320×48 image.

### Forklift assembly

Within `sprites/forklift/body.svg`'s 176×144 coordinate space:

- Wheel centers: `(32, 124)` and `(96, 124)`; wheel artwork is 40×40.
- Driver head center: `(61, 53)`; avatar artwork is 56×56 and can be scaled to about 36×36.
- Draw driver behind the body, then body, then wheels.
- Flip the whole assembly to face left. Slight bobbing and wheel rotation are sufficient; no skeletal animation is needed.

### Effects and feedback

- Dust: `dust_00` → `dust_05`, **12 fps**, hide/free when finished.
- Impact: `impact_00` → `impact_03`, **16 fps**, hide/free when finished.
- Debris: animate the three fragments on simple arcs after a collapse. They should not change authoritative game results.
- Collapse: rotate and drop existing crate sprites with staggered timing. A full tower-collapse sprite sheet is intentionally unnecessary.
- Optional well-centered placement sound does **not** imply a scoring bonus.
- Keep screen shake optional. Disable nonessential particles under reduced-motion settings.

## UI and text

The pack deliberately **does not bake text into UI art**. Render player names, scores, timers, room codes, button labels, input bindings, errors, and localization strings with the engine's text system.

An engine default font is sufficient for the prototype. No third-party font is bundled here. Before choosing a custom release font, verify its license and include its required notices.

Suggested first screens: title, create/join room, lobby, gameplay, results, settings, disconnect/error modal. Reuse these panels and icons rather than authoring one flat image per screen.

Do not identify players by color alone: show their name / number on the HUD and turn marker. Pair the green landing region with visible bounds, not color alone. Use readable text contrast and keyboard focus states.

## Audio notes

Sound effects are procedural one-shots generated from tones and deterministic noise. They have short envelopes and bounded peaks, but still need **in-game loudness mixing and listening tests**. `forklift_motor.wav` is a movement cue, not a seamless ambience loop.

Suggested mapping:

- `your_turn` once when local control begins; `countdown_tick` for the final few seconds.
- `crate_drop` on accepted drop, `crate_land` on contact.
- `wood_collapse` once per failure; limit `debris_hit` instances to avoid noise overload.
- `shift_end` and `match_win` on the appropriate results transition, not simultaneously by default.

Music, voice, and continuous ambience are intentionally omitted: none is required by the current game loop. No commercial music or human voice recordings are included.

## Rebuild

From the repository root:

```sh
python3 assets/generate.py
```

Uses only the Python standard library. Rebuild overwrites generated artwork, sounds, and metadata. Edit the generator for persistent changes; keep hand-authored additions in separate files. Generation does not remove obsolete files if you later rename assets.

## Scope and remaining release work

This covers the visual and SFX needs of a **playable MVP**, not an implemented game or a final Steam submission package. Still required elsewhere:

- Gameplay, networking, menus, layout, text, and animation code.
- In-engine visual checks, audio mixing, accessibility testing, and resolution testing.
- Any later content-specific artwork or controller-specific prompts.
- Final logo / wordmark, Steam capsules and library assets, trailer, store screenshots, and platform icons, prepared against current Steam specifications after branding is settled.
- Review of the provisional game title for availability; no clearance is implied.

See `PROVENANCE.md` for generation and dependency notes.
