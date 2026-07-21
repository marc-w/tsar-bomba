# MF64 — Midi Fighter 64 Ableton Live 11 Control Surface

## Setup

- Copy the `MF64` folder to `~/Music/Ableton/User Library/Remote Scripts/`
- In Live Preferences → Link/MIDI, select **MF64** as a Control Surface with Input/Output set to the Midi Fighter 64
- Enable **Track** and **Remote** on the Midi Fighter input row

---

## MIDI Config

| Setting | Value |
|---|---|
| MIDI Channel | 3 (0-indexed: 2 in script) |
| Grid | 4 tracks × 6 scenes |

---

## Button Map

### Clip Launch Grid

4 wide × 6 tall. Notes run left-to-right, bottom-to-top on the hardware (E1 = lower-left, D#3 = upper-right). Mapped top-to-bottom in Live scene order (scene 0 = top row = highest notes).

| Scene (Live) | Track 1 | Track 2 | Track 3 | Track 4 |
|---|---|---|---|---|
| 0 (top) | C3 / 60 | C#3 / 61 | D3 / 62 | D#3 / 63 |
| 1 | G#2 / 56 | A2 / 57 | A#2 / 58 | B2 / 59 |
| 2 | E2 / 52 | F2 / 53 | F#2 / 54 | G2 / 55 |
| 3 | C2 / 48 | C#2 / 49 | D2 / 50 | D#2 / 51 |
| 4 | G#1 / 44 | A1 / 45 | A#1 / 46 | B1 / 47 |
| 5 (bottom) | E1 / 40 | F1 / 41 | F#1 / 42 | G1 / 43 |

### Scene Navigation

| Button | Note | MIDI # |
|---|---|---|
| Scene Up | G#5 | 92 |
| Scene Down | E5 | 88 |

### Stop Buttons (per track)

| Constant | Note | MIDI # | Action |
|---|---|---|---|
| `STOP_NOTE_TRACK_1` | E3 | 64 | stop_all_clips() on visible track 1 |
| `STOP_NOTE_TRACK_2` | F3 | 65 | stop_all_clips() on visible track 2 |
| `STOP_NOTE_TRACK_3` | F#3 | 66 | stop_all_clips() on visible track 3 |
| `STOP_NOTE_TRACK_4` | G3 | 67 | stop_all_clips() on visible track 4 |

---

## LED Behavior

All LED velocity values are script constants — edit them at the top of `midifighter64_funhogdotme.py` to match your firmware's color map.

### Nav Buttons (Up / Down)

| Constant | Default Value | State |
|---|---|---|
| `LED_NAV_CAN_SCROLL` | 64 | Green — more scenes available in this direction |
| `LED_NAV_CANNOT_SCROLL` | 1 | Red — already at the scroll limit |

The framework drives these automatically — no manual listener needed.

### Clip Grid

| Constant | Default Value | State |
|---|---|---|
| `LED_CLIP_EMPTY` | 0 | Off — no clip in slot |
| `LED_CLIP_STOPPED` | 45 | Blue — clip exists, not playing |
| `LED_CLIP_PLAYING` | 64 | Green — clip is playing |
| `LED_CLIP_TRIGGERED` | 1 | Blink / red — clip is queued to launch. Use a firmware blink velocity if supported, otherwise set to a red value. |

### Stop Buttons

| Constant | Default Value | State |
|---|---|---|
| `LED_STOP_IDLE` | 1 | Red — always lit while script is active |
| `LED_STOP_ACTIVE` | 64 | Blink / alternate color — lit from button press until track fully stops (`playing_slot_index == -1`) |

Stop buttons restore to `LED_STOP_IDLE` automatically once the track's playing slot index returns to -1 (no active clip).

---

## Files

| File | Purpose |
|---|---|
| `__init__.py` | Live entry point — calls `create_instance()` |
| `midifighter64_funhogdotme.py` | Main script — session, grid, stop buttons, LED values |
| `README.md` | This file |
