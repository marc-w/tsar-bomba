import time

from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from _Framework.SessionComponent import SessionComponent

# ── Grid dimensions ──────────────────────────────────────────────────────────

MIDI_CHANNEL = 2   # 0-indexed; Midi Fighter channel 3
BOX_WIDTH    = 4
BOX_HEIGHT   = 6

# ── Note assignments ─────────────────────────────────────────────────────────
# All note numbers are easily editable here.

# 4×6 launch grid, left-to-right / top-to-bottom (scene 0 = top of Live session)
LAUNCH_NOTES = [
    60, 61, 62, 63,  # scene 0 (top):    C3   C#3  D3   D#3
    56, 57, 58, 59,  # scene 1:          G#2  A2   A#2  B2
    52, 53, 54, 55,  # scene 2:          E2   F2   F#2  G2
    48, 49, 50, 51,  # scene 3:          C2   C#2  D2   D#2
    44, 45, 46, 47,  # scene 4:          G#1  A1   A#1  B1
    40, 41, 42, 43,  # scene 5 (bottom): E1   F1   F#1  G1
]

SCENE_UP_NOTE   = 92  # G#5 — scroll session up
SCENE_DOWN_NOTE = 88  # E5  — scroll session down

# Stop-track buttons, one per column (track 1–4)
STOP_NOTE_TRACK_1 = 64  # E3
STOP_NOTE_TRACK_2 = 65  # F3
STOP_NOTE_TRACK_3 = 66  # F#3
STOP_NOTE_TRACK_4 = 67  # G3
STOP_NOTES = [STOP_NOTE_TRACK_1, STOP_NOTE_TRACK_2, STOP_NOTE_TRACK_3, STOP_NOTE_TRACK_4]  # noqa: E501

# ── LED velocity values ──────────────────────────────────────────────────────
# Midi Fighter 64 selects LED color via note-on velocity.
# All values are placeholders — tune to your firmware's color map.

# Nav buttons (up / down)
LED_NAV_CAN_SCROLL    = 64  # green — more scenes available in this direction
LED_NAV_CANNOT_SCROLL = 1   # red   — already at the limit

# Clip grid
LED_CLIP_EMPTY     = 0   # off   — no clip in slot
LED_CLIP_STOPPED   = 45  # blue  — clip exists but is not playing
LED_CLIP_PLAYING   = 64  # green — clip is currently playing
LED_CLIP_TRIGGERED = 120  # queued to launch — placeholder, tune to firmware blink/red velocity  # noqa: E501

# Stop buttons
LED_STOP_IDLE = 127  # red — always illuminated while script is active (tune to firmware color map)


# ── Session component ─────────────────────────────────────────────────────────

class MF64SessionComponent(SessionComponent):
    def __init__(self, num_tracks, num_scenes, parent):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self._parent = parent

    def disconnect(self):
        SessionComponent.disconnect(self)
        self._parent = None


# ── Main control surface ──────────────────────────────────────────────────────

class MidiFighter64(ControlSurface):
    __module__ = __name__
    __doc__    = 'DJ Tech Tools Midi Fighter 64 control surface'

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            self.log_message('MF64 loading ' + time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()))
            self._suppress_session_highlight = True
            self._suppress_send_midi         = True
            self._setup_session()
            self._suppress_session_highlight = False
            self.log_message('MF64 loaded')

    def _button(self, note):
        return ButtonElement(True, MIDI_NOTE_TYPE, MIDI_CHANNEL, note)

    # ── Session / grid setup ─────────────────────────────────────────────────

    def _setup_session(self):
        session = MF64SessionComponent(BOX_WIDTH, BOX_HEIGHT, self)
        session.name = 'Session_Control'

        # Nav buttons — on_value = green (can scroll), off_value = red (at limit)
        up   = self._button(SCENE_UP_NOTE)
        down = self._button(SCENE_DOWN_NOTE)
        up.name   = 'Scene_Up'
        down.name = 'Scene_Down'
        # set_on_value/set_off_value don't exist in this _Framework version;
        # set the private attributes directly instead.
        up._on_value    = LED_NAV_CAN_SCROLL
        up._off_value   = LED_NAV_CANNOT_SCROLL
        down._on_value  = LED_NAV_CAN_SCROLL
        down._off_value = LED_NAV_CANNOT_SCROLL
        session.set_scene_bank_buttons(down, up)

        # Clip launch grid
        for scene_index in range(BOX_HEIGHT):
            scene = session.scene(scene_index)
            scene.name = 'Scene_{}'.format(scene_index)
            for track_index in range(BOX_WIDTH):
                note   = LAUNCH_NOTES[scene_index * BOX_WIDTH + track_index]
                button = self._button(note)
                button.name = 'Clip_{}_{}'.format(track_index, scene_index)
                slot = scene.clip_slot(track_index)
                slot.name = 'Slot_{}_{}'.format(track_index, scene_index)
                slot.set_stopped_value(LED_CLIP_STOPPED)            # blue — stopped
                slot.set_started_value(LED_CLIP_PLAYING)            # green — playing
                slot.set_triggered_to_play_value(LED_CLIP_TRIGGERED)  # blink/red — queued
                slot.set_launch_button(button)

        self.set_highlighting_session_component(session)
        self._session = session

        # Stop buttons — wired via SessionComponent's native stop API so the
        # component framework handles LED output (same path as clip grid LEDs).
        stop_buttons = [self._button(note) for note in STOP_NOTES]
        for i, button in enumerate(stop_buttons):
            button.name = 'Stop_{}'.format(i)
            button._on_value  = LED_STOP_IDLE
            button._off_value = LED_STOP_IDLE  # always red regardless of state
        session.set_stop_track_clip_buttons(stop_buttons)
        self._stop_buttons = stop_buttons

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def disconnect(self):
        self.log_message('MF64 unloaded ' + time.strftime('%d.%m.%Y %H:%M:%S', time.localtime()))
        ControlSurface.disconnect(self)
