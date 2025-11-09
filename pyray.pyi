from typing import Any, List, Optional, Tuple

# --- Window Flags ---
FLAG_VSYNC_HINT: int
FLAG_FULLSCREEN_MODE: int
FLAG_WINDOW_RESIZABLE: int
FLAG_WINDOW_UNDECORATED: int
FLAG_WINDOW_HIDDEN: int
FLAG_WINDOW_MINIMIZED: int
FLAG_WINDOW_MAXIMIZED: int
FLAG_WINDOW_UNFOCUSED: int
FLAG_WINDOW_TOPMOST: int
FLAG_WINDOW_ALWAYS_RUN: int
FLAG_WINDOW_TRANSPARENT: int
FLAG_MSAA_4X_HINT: int
FLAG_INTERLACED_HINT: int

# --- Keyboard Keys ---
KEY_NULL: int
KEY_APOSTROPHE: int
KEY_COMMA: int
KEY_MINUS: int
KEY_PERIOD: int
KEY_SLASH: int
KEY_ZERO: int
KEY_ONE: int
KEY_TWO: int
KEY_THREE: int
KEY_FOUR: int
KEY_FIVE: int
KEY_SIX: int
KEY_SEVEN: int
KEY_EIGHT: int
KEY_NINE: int
KEY_SEMICOLON: int
KEY_EQUAL: int
KEY_A: int
KEY_B: int
KEY_C: int
KEY_D: int
KEY_E: int
KEY_F: int
KEY_G: int
KEY_H: int
KEY_I: int
KEY_J: int
KEY_K: int
KEY_L: int
KEY_M: int
KEY_N: int
KEY_O: int
KEY_P: int
KEY_Q: int
KEY_R: int
KEY_S: int
KEY_T: int
KEY_U: int
KEY_V: int
KEY_W: int
KEY_X: int
KEY_Y: int
KEY_Z: int
KEY_SPACE: int
KEY_ESCAPE: int
KEY_ENTER: int
KEY_TAB: int
KEY_BACKSPACE: int
KEY_INSERT: int
KEY_DELETE: int
KEY_RIGHT: int
KEY_LEFT: int
KEY_DOWN: int
KEY_UP: int
KEY_F1: int
KEY_F2: int
KEY_F3: int
KEY_F4: int
KEY_F5: int
KEY_F6: int
KEY_F7: int
KEY_F8: int
KEY_F9: int
KEY_F10: int
KEY_F11: int
KEY_F12: int

# --- Mouse Buttons ---
MOUSE_BUTTON_LEFT: int
MOUSE_BUTTON_RIGHT: int
MOUSE_BUTTON_MIDDLE: int
MOUSE_BUTTON_SIDE: int
MOUSE_BUTTON_EXTRA: int
MOUSE_BUTTON_FORWARD: int
MOUSE_BUTTON_BACK: int

# --- Gamepad Buttons ---
GAMEPAD_PLAYER1: int
GAMEPAD_PLAYER2: int
GAMEPAD_PLAYER3: int
GAMEPAD_PLAYER4: int
GAMEPAD_BUTTON_LEFT_FACE_UP: int
GAMEPAD_BUTTON_LEFT_FACE_RIGHT: int
GAMEPAD_BUTTON_LEFT_FACE_DOWN: int
GAMEPAD_BUTTON_LEFT_FACE_LEFT: int

# --- Colors ---
class Color:
    r: int
    g: int
    b: int
    a: int

    def __init__(self, r: int, g: int, b: int, a: int): ...

WHITE: Color
BLACK: Color
RED: Color
GREEN: Color
BLUE: Color
YELLOW: Color
GRAY: Color
LIGHTGRAY: Color
DARKGRAY: Color
MAGENTA: Color
ORANGE: Color
PURPLE: Color
SKYBLUE: Color
RAYWHITE: Color

# --- Basic Types ---
class Vector2:
    x: float
    y: float
    def __init__(self, x: float = 0, y: float = 0): ...

class Vector3:
    x: float
    y: float
    z: float
    def __init__(self, x: float = 0, y: float = 0, z: float = 0): ...

class Rectangle:
    x: float
    y: float
    width: float
    height: float
    def __init__(
        self, x: float, y: float, width: float, height: float
    ): ...

class Texture:
    id: int
    width: int
    height: int
    mipmaps: int
    format: int

class Font:
    baseSize: int
    glyphCount: int

class Camera2D:
    offset: Vector2
    target: Vector2
    rotation: float
    zoom: float

# --- Window Management ---
def init_window(width: int, height: int, title: bytes) -> None: ...
def window_should_close() -> bool: ...
def close_window() -> None: ...
def is_window_ready() -> bool: ...
def is_window_fullscreen() -> bool: ...
def toggle_fullscreen() -> None: ...
def set_window_title(title: bytes) -> None: ...
def set_window_size(width: int, height: int) -> None: ...
def get_screen_width() -> int: ...
def get_screen_height() -> int: ...

# --- Drawing ---
def begin_drawing() -> None: ...
def end_drawing() -> None: ...
def clear_background(color: Color) -> None: ...
def draw_text(
    text: bytes, posX: int, posY: int, fontSize: int, color: Color
) -> None: ...
def draw_rectangle(
    x: int, y: int, width: int, height: int, color: Color
) -> None: ...
def draw_circle(
    x: int, y: int, radius: float, color: Color
) -> None: ...
def draw_texture(
    texture: Texture, x: int, y: int, tint: Color
) -> None: ...

# --- Input ---
def is_key_pressed(key: int) -> bool: ...
def is_key_down(key: int) -> bool: ...
def is_mouse_button_pressed(button: int) -> bool: ...
def is_mouse_button_down(button: int) -> bool: ...
def get_mouse_position() -> Vector2: ...
def get_mouse_wheel_move() -> float: ...

# --- Files and Drag-Drop ---
class FilePathList:
    count: int
    paths: List[bytes]

def is_file_dropped() -> bool: ...
def load_dropped_files() -> FilePathList: ...
def unload_dropped_files(files: FilePathList) -> None: ...
def gui_label(bounds: Rectangle, text: bytes) -> None: ...
def gui_button(bounds: Rectangle, text: bytes) -> bool: ...
def gui_panel(bounds: Rectangle, text: Optional[bytes]) -> int: ...
def gui_scroll_panel(
    bounds: Rectangle,
    text: Optional[bytes],
    content: Rectangle,
    scroll: Vector2,
    view: Rectangle,
) -> Tuple[int, Rectangle]: ...
def gui_text_box(
    bounds: Rectangle, text: bytes, text_size: int, edit_mode: bool
) -> bool: ...
def gui_text_input_box(
    bounds: Rectangle,
    title: bytes,
    message: bytes,
    buttons: bytes,
    text: bytes,
    text_size: int,
    secret_view_active: Optional[bool],
) -> int: ...
def gui_window_box(bounds: Rectangle, title: bytes) -> bool: ...
def gui_grid(
    bounds: Rectangle,
    text: Optional[bytes],
    spacing: float,
    subdivs: int,
    mouse_cell: Optional[Vector2],
) -> bool: ...

# --- Timing ---
def get_frame_time() -> float: ...
def set_target_fps(fps: int) -> None: ...
def get_fps() -> int: ...

# --- Audio System ---
def init_audio_device() -> None: ...
def close_audio_device() -> None: ...
def is_audio_device_ready() -> bool: ...
def set_master_volume(volume: float) -> None: ...
def get_master_volume() -> float: ...

# --- Wave / Sound ---
class Wave:
    frameCount: int
    sampleRate: int
    sampleSize: int
    channels: int
    data: Any

class Sound:
    frameCount: int
    stream: Any

def load_wave(fileName: bytes) -> Wave: ...
def load_wave_from_memory(
    fileType: bytes, fileData: bytes, dataSize: int
) -> Wave: ...
def unload_wave(wave: Wave) -> None: ...
def export_wave(wave: Wave, fileName: bytes) -> bool: ...
def export_wave_as_code(wave: Wave, fileName: bytes) -> bool: ...
def load_sound(fileName: bytes) -> Sound: ...
def load_sound_from_wave(wave: Wave) -> Sound: ...
def update_sound(
    sound: Sound, data: Any, sampleCount: int
) -> None: ...
def unload_sound(sound: Sound) -> None: ...
def is_sound_ready(sound: Sound) -> bool: ...

# --- Play Control ---
def play_sound(sound: Sound) -> None: ...
def stop_sound(sound: Sound) -> None: ...
def pause_sound(sound: Sound) -> None: ...
def resume_sound(sound: Sound) -> None: ...
def is_sound_playing(sound: Sound) -> bool: ...
def set_sound_volume(sound: Sound, volume: float) -> None: ...
def set_sound_pitch(sound: Sound, pitch: float) -> None: ...
def set_sound_pan(sound: Sound, pan: float) -> None: ...

# --- Wave Data Operations ---
def wave_copy(wave: Wave) -> Wave: ...
def wave_crop(
    wave: Wave, initSample: int, finalSample: int
) -> None: ...
def wave_format(
    wave: Wave, sampleRate: int, sampleSize: int, channels: int
) -> None: ...
def load_wave_samples(wave: Wave) -> Any: ...
def unload_wave_samples(samples: Any) -> None: ...

# --- Music ---
class Music:
    stream: Any
    frameCount: int
    looping: bool
    ctxType: int
    ctxData: Any

def load_music_stream(fileName: bytes) -> Music: ...
def load_music_stream_from_memory(
    fileType: bytes, data: bytes, dataSize: int
) -> Music: ...
def unload_music_stream(music: Music) -> None: ...
def is_music_ready(music: Music) -> bool: ...
def play_music_stream(music: Music) -> None: ...
def is_music_stream_playing(music: Music) -> bool: ...
def update_music_stream(music: Music) -> None: ...
def stop_music_stream(music: Music) -> None: ...
def pause_music_stream(music: Music) -> None: ...
def resume_music_stream(music: Music) -> None: ...
def seek_music_stream(music: Music, position: float) -> None: ...
def set_music_volume(music: Music, volume: float) -> None: ...
def set_music_pitch(music: Music, pitch: float) -> None: ...
def set_music_pan(music: Music, pan: float) -> None: ...
def get_music_time_length(music: Music) -> float: ...
def get_music_time_played(music: Music) -> float: ...

# --- AudioStream ---
class AudioStream:
    buffer: Any
    sampleRate: int
    sampleSize: int
    channels: int

def load_audio_stream(
    sampleRate: int, sampleSize: int, channels: int
) -> AudioStream: ...
def unload_audio_stream(stream: AudioStream) -> None: ...
def is_audio_stream_ready(stream: AudioStream) -> bool: ...
def play_audio_stream(stream: AudioStream) -> None: ...
def pause_audio_stream(stream: AudioStream) -> None: ...
def resume_audio_stream(stream: AudioStream) -> None: ...
def is_audio_stream_playing(stream: AudioStream) -> bool: ...
def stop_audio_stream(stream: AudioStream) -> None: ...
def set_audio_stream_volume(
    stream: AudioStream, volume: float
) -> None: ...
def set_audio_stream_pitch(
    stream: AudioStream, pitch: float
) -> None: ...
def set_audio_stream_pan(stream: AudioStream, pan: float) -> None: ...
def update_audio_stream(
    stream: AudioStream, data: Any, frameCount: int
) -> None: ...
def is_audio_stream_processed(stream: AudioStream) -> bool: ...
def attach_audio_stream_processor(
    stream: AudioStream, processor: Any
) -> None: ...
def detach_audio_stream_processor(
    stream: AudioStream, processor: Any
) -> None: ...
def attach_audio_mixed_processor(processor: Any) -> None: ...
def detach_audio_mixed_processor(processor: Any) -> None: ...
def set_config_flags(flags: int) -> None: ...

# --- Setup / Style ---
def gui_enable() -> None: ...
def gui_disable() -> None: ...
def gui_lock() -> None: ...
def gui_unlock() -> None: ...
def gui_is_locked() -> bool: ...
def gui_set_state(state: int) -> None: ...
def gui_get_state() -> int: ...
def gui_set_alpha(alpha: float) -> None: ...
def gui_get_alpha() -> float: ...
def gui_set_style(
    control: int, property: int, value: int
) -> None: ...
def gui_get_style(control: int, property: int) -> int: ...
def gui_load_style(fileName: bytes) -> None: ...
def gui_load_style_default() -> None: ...

# --- Basic Controls ---
def gui_label_button(bounds: Rectangle, text: bytes) -> bool: ...
def gui_toggle(
    bounds: Rectangle, text: bytes, active: bool
) -> bool: ...
def gui_toggle_group(
    bounds: Rectangle, text: bytes, active: int
) -> int: ...
def gui_toggle_slider(
    bounds: Rectangle, text: bytes, active: int
) -> int: ...
def gui_check_box(
    bounds: Rectangle, text: bytes, checked: bool
) -> bool: ...
def gui_combo_box(
    bounds: Rectangle, text: bytes, active: int
) -> int: ...
def gui_dropdown_box(
    bounds: Rectangle, text: bytes, active: int, editMode: bool
) -> Tuple[int, bool]: ...
def gui_spinner(
    bounds: Rectangle,
    text: bytes,
    value: int,
    minValue: int,
    maxValue: int,
    editMode: bool,
) -> Tuple[int, bool]: ...
def gui_value_box(
    bounds: Rectangle,
    text: bytes,
    value: int,
    minValue: int,
    maxValue: int,
    editMode: bool,
) -> Tuple[int, bool]: ...
def gui_text_box_multi(
    bounds: Rectangle, text: bytes, textSize: int, editMode: bool
) -> bool: ...
def gui_slider(
    bounds: Rectangle,
    textLeft: bytes,
    textRight: bytes,
    value: float,
    minValue: float,
    maxValue: float,
) -> float: ...
def gui_slider_bar(
    bounds: Rectangle,
    textLeft: bytes,
    textRight: bytes,
    value: float,
    minValue: float,
    maxValue: float,
) -> float: ...
def gui_progress_bar(
    bounds: Rectangle,
    textLeft: bytes,
    textRight: bytes,
    value: float,
    minValue: float,
    maxValue: float,
) -> float: ...
def gui_status_bar(bounds: Rectangle, text: bytes) -> None: ...
def gui_dummy_rec(bounds: Rectangle, text: bytes) -> None: ...

# --- Advance Controls ---
def gui_list_view(
    bounds: Rectangle, text: bytes, scrollIndex: int, active: int
) -> Tuple[int, int]: ...
def gui_list_view_ex(
    bounds: Rectangle,
    text: Tuple[bytes, ...],
    count: int,
    focus: int,
    scrollIndex: int,
    active: int,
) -> Tuple[int, int, int]: ...
def gui_message_box(
    bounds: Rectangle, title: bytes, message: bytes, buttons: bytes
) -> int: ...
def gui_color_picker(
    bounds: Rectangle, text: Optional[bytes], color: Color
) -> Color: ...
def gui_color_panel(
    bounds: Rectangle, text: Optional[bytes], color: Color
) -> Color: ...
def gui_color_bar_alpha(
    bounds: Rectangle, text: Optional[bytes], alpha: float
) -> float: ...
def gui_color_bar_hue(
    bounds: Rectangle, text: Optional[bytes], value: float
) -> float: ...
def gui_text_box_dropdown(
    bounds: Rectangle, text: bytes, active: int, editMode: bool
) -> Tuple[int, bool]: ...

# --- Containers ---
def gui_group_box(bounds: Rectangle, text: bytes) -> None: ...
def gui_line(bounds: Rectangle, text: bytes) -> None: ...
def gui_tab_bar(
    bounds: Rectangle, text: bytes, active: int
) -> int: ...
def gui_scroll_bar(
    bounds: Rectangle, value: int, minValue: int, maxValue: int
) -> int: ...
def gui_combo_button(
    bounds: Rectangle, text: bytes, active: int
) -> int: ...

# --- Icons ---
def gui_draw_icon(
    iconId: int,
    positionX: int,
    positionY: int,
    pixelSize: int,
    color: Color,
) -> None: ...
def gui_set_icon_scale(scale: int) -> None: ...
def gui_get_icon_data(iconId: int) -> bytes: ...
def gui_set_icon_data(iconId: int, data: bytes) -> None: ...
def gui_set_icon_pixel(iconId: int, x: int, y: int) -> None: ...
def gui_clear_icon_pixel(iconId: int, x: int, y: int) -> None: ...
def gui_check_icon_pixel(iconId: int, x: int, y: int) -> bool: ...

# --- Constants (control states & enums) ---
STATE_NORMAL: int
STATE_FOCUSED: int
STATE_PRESSED: int
STATE_DISABLED: int

TEXT_ALIGN_LEFT: int
TEXT_ALIGN_CENTER: int
TEXT_ALIGN_RIGHT: int

DEFAULT: int
LABEL: int
BUTTON: int
TOGGLE: int
SLIDER: int
PROGRESSBAR: int
CHECKBOX: int
COMBOBOX: int
DROPDOWNBOX: int
TEXTBOX: int
VALUEBOX: int
SPINNER: int
LISTVIEW: int
COLORPICKER: int
SCROLLBAR: int
STATUSBAR: int

ffi: Any  # cffi FFI instance used internally

def begin_scissor_mode(
    x: int, y: int, width: int, height: int
) -> None: ...
def end_scissor_mode() -> None: ...
def get_file_name(file_path: bytes) -> bytes: ...
def fade(color: Color, alpha: float) -> Color: ...
