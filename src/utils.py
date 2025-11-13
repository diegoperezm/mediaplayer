from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

# import resource
import pyray as pr
import raylib as rl

GRID_COLS = 12
GRID_ROWS = 12
SIZE_ROWS = 12
SIZE_COLS = 12
BGCOLOR = pr.Color(0, 34, 43, 255)


class State(Enum):
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    RESUMED = "RESUMED"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    PREV = "PREV"
    NEXT = "NEXT"
    INVALID = "INVALID"


class Event(Enum):
    play = "evt_play"
    pause = "evt_pause"
    stop = "evt_stop"
    prev = "evt_prev"
    next = "evt_next"


class Element(Enum):
    EL_BLANK = 0
    EL_DROP_FILES = 1
    EL_BTN_PREV = 2
    EL_BTN_PLAY = 3
    EL_BTN_PAUSE = 4
    EL_BTN_STOP = 5
    EL_BTN_NEXT = 6
    EL_PROGRESS_BAR = 7
    EL_VOLUME_SLIDER = 8


@dataclass
class PlayListData:
    music: Optional[pr.Music] = None
    file_paths: list = field(default_factory=list)
    current_track_index: int = -1
    current_track_pos: float = pr.ffi.new("float *", 0.0)
    total_track_time: float = pr.ffi.new("float *", 0.0)
    current_vol_level: float = pr.ffi.new("float *", 0.3)
    scroll: pr.Vector2 = pr.Vector2(0, 0)
    view: pr.Rectangle = pr.Rectangle(0, 0, 0, 0)


@dataclass
class MusicPlayer:
    current_state: State = State.WAITING


transition_table: Dict[State, Dict[Event, State]] = {
    State.WAITING: {
        Event.play: State.PLAYING,
        Event.pause: State.INVALID,
        Event.stop: State.INVALID,
        Event.prev: State.INVALID,
        Event.next: State.INVALID,
    },
    State.PLAYING: {
        Event.play: State.INVALID,
        Event.pause: State.PAUSED,
        Event.stop: State.STOPPED,
        Event.prev: State.PREV,
        Event.next: State.NEXT,
    },
    State.RESUMED: {
        Event.play: State.INVALID,
        Event.pause: State.PAUSED,
        Event.stop: State.STOPPED,
        Event.prev: State.PREV,
        Event.next: State.NEXT,
    },
    State.PAUSED: {
        Event.play: State.RESUMED,
        Event.pause: State.INVALID,
        Event.stop: State.STOPPED,
        Event.prev: State.PREV,
        Event.next: State.NEXT,
    },
    State.STOPPED: {
        Event.play: State.PLAYING,
        Event.pause: State.INVALID,
        Event.stop: State.INVALID,
        Event.prev: State.PREV,
        Event.next: State.NEXT,
    },
    State.PREV: {
        Event.play: State.PLAYING,
        Event.pause: State.INVALID,
        Event.stop: State.INVALID,
        Event.prev: State.INVALID,
        Event.next: State.INVALID,
    },
    State.NEXT: {
        Event.play: State.PLAYING,
        Event.pause: State.INVALID,
        Event.stop: State.INVALID,
        Event.prev: State.INVALID,
        Event.next: State.INVALID,
    },
}

_map_default: List[List[int]] = [[0] * SIZE_COLS for _ in range(SIZE_ROWS)]

_map_state_waiting: List[List[int]] = [
    [Element.EL_DROP_FILES.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [
        Element.EL_BTN_PREV.value,
        Element.EL_BTN_PLAY.value,
        Element.EL_BTN_STOP.value,
        Element.EL_BTN_NEXT.value,
        Element.EL_PROGRESS_BAR.value,
        Element.EL_VOLUME_SLIDER.value,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
]

_map_state_play: List[List[int]] = [
    [Element.EL_DROP_FILES.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [
        Element.EL_BTN_PREV.value,
        Element.EL_BTN_PAUSE.value,  # <- Different from waiting
        Element.EL_BTN_STOP.value,
        Element.EL_BTN_NEXT.value,
        Element.EL_PROGRESS_BAR.value,
        Element.EL_VOLUME_SLIDER.value,
        0,
        0,
        0,
        0,
        0,
        0,
    ],
]


def update_state(
    music_player: MusicPlayer, event: Event, data: PlayListData
) -> None:
    current_state = music_player.current_state

    next_state = transition_table[current_state].get(event, State.INVALID)

    if next_state is not State.INVALID:
        music_player.current_state = next_state
        pr.trace_log(
            pr.LOG_INFO,
            f"current state: {current_state.name} -> next state: {music_player.current_state.name}",
        )
    else:
        pr.trace_log(
            pr.LOG_WARNING,
            f"Invalid transition: {event.name} from {current_state.name}",
        )

    match next_state:
        case State.WAITING:
            pass
        case State.PLAYING:
            load_track(data)
            play_track(data)

        case State.RESUMED:
            resume_track(data)

        case State.PAUSED:
            pr.pause_music_stream(data.music)

        case State.STOPPED:
            pr.stop_music_stream(data.music)
            data.current_track_pos[0] = pr.get_music_time_played(data.music)
            pr.unload_music_stream(data.music)  # TODO: required?

        case State.PREV:
            data.current_track_index = get_prev_track(data)
            if pr.is_music_stream_playing(data.music):
                pr.unload_music_stream(data.music)
            update_state(music_player, Event.play, data)

        case State.NEXT:
            data.current_track_index = get_next_track(data)
            if pr.is_music_stream_playing(data.music):
                pr.unload_music_stream(data.music)
            update_state(music_player, Event.play, data)


def get_prev_track(data: PlayListData) -> int:
    return (data.current_track_index - 1 + len(data.file_paths)) % len(
        data.file_paths
    )


def get_next_track(data: PlayListData) -> int:
    return (data.current_track_index + 1) % len(data.file_paths)


def is_playlist_empty(data: PlayListData) -> bool:
    return len(data.file_paths) == 0


def init_raylib() -> None:
    screen_w = 800
    screen_h = 600
    pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
    pr.init_window(screen_w, screen_h, b"Media Player")
    pr.set_target_fps(30)
    rl.GuiLoadStyle(b"assets/style_cyber.rgs")


def get_layout(music_player: MusicPlayer) -> List[List[int]]:
    match music_player.current_state:
        case State.PLAYING | State.RESUMED:
            return _map_state_play
        case (
            State.WAITING
            | State.PAUSED
            | State.STOPPED
            | State.PREV
            | State.NEXT
        ):
            return _map_state_waiting
        case _:
            return _map_default


def render_ui(music_player: MusicPlayer, data: PlayListData) -> None:
    layout = get_layout(music_player)

    width = pr.get_screen_width()
    height = pr.get_screen_height()
    cell_width = width / GRID_COLS
    cell_height = height / GRID_ROWS
    clicked: bool

    for row, row_data in enumerate(layout):
        for col, element in enumerate(row_data):
            cell_x = col * cell_width
            cell_y = row * cell_height

            match element:
                case Element.EL_BLANK.value:
                    pass

                case Element.EL_PROGRESS_BAR.value:
                    render_el_progress_bar(
                        cell_x, cell_y, cell_width, cell_height, data
                    )

                case Element.EL_BTN_PREV.value:
                    clicked = render_el_btn_prev(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked and is_playlist_empty(data) is False:
                        update_state(music_player, Event.prev, data)

                case Element.EL_BTN_PLAY.value:
                    clicked = render_el_btn_play(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked and is_playlist_empty(data) is False:
                        update_state(music_player, Event.play, data)

                case Element.EL_BTN_PAUSE.value:
                    clicked = render_el_btn_pause(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if (
                        clicked
                        and data.music is not None
                        and pr.is_music_stream_playing(data.music)
                    ):
                        update_state(music_player, Event.pause, data)

                case Element.EL_BTN_STOP.value:
                    clicked = render_el_btn_stop(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if (
                        clicked
                        and data.music is not None
                        and pr.is_music_stream_playing(data.music)
                    ):
                        update_state(music_player, Event.stop, data)

                case Element.EL_BTN_NEXT.value:
                    clicked = render_el_btn_next(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked and is_playlist_empty(data) is False:
                        update_state(music_player, Event.next, data)

                case Element.EL_VOLUME_SLIDER.value:
                    render_el_volume_slider(
                        cell_x, cell_y, cell_width, cell_height, data
                    )

                case Element.EL_DROP_FILES.value:
                    render_el_drop_files(
                        cell_x,
                        cell_y,
                        cell_width,
                        cell_height,
                        data,
                    )


def render_el_progress_bar(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
    data: PlayListData,
) -> None:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width * 8, cell_height / 2)

    if data.music is not None and pr.is_music_stream_playing(data.music):
        data.current_track_pos[0] = pr.get_music_time_played(data.music)
        data.total_track_time[0] = pr.get_music_time_length(data.music)

    total_track_time_max = max(data.total_track_time[0], 0.001)

    pr.gui_progress_bar(
        bounds,
        b"",
        b"",
        data.current_track_pos,
        0.0,
        total_track_time_max,
    )


def render_el_btn_prev(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)

    return pr.gui_button(bounds, b"<<")


def render_el_btn_play(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)

    return pr.gui_button(bounds, b">")


def render_el_btn_pause(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)

    return pr.gui_button(bounds, b"||")


def render_el_btn_stop(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)

    return pr.gui_button(bounds, b"[]")


def render_el_btn_next(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)

    return pr.gui_button(bounds, b">>")


def render_el_volume_slider(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
    data: PlayListData,
) -> None:
    bounds = pr.Rectangle(
        cell_x,
        cell_y + (cell_height / 2),
        cell_width * 7,
        cell_height / 2,
    )

    pr.gui_slider(bounds, b"VOL ", b"", data.current_vol_level, 0, 1)

    if data.music is not None:
        pr.set_music_volume(data.music, data.current_vol_level[0])


def get_content_height(
    data: PlayListData,
    cell_height: float,
    bounds: pr.Rectangle,
) -> float:
    if (len(data.file_paths) * cell_height) > bounds.height:
        return (len(data.file_paths) * cell_height) + (cell_height * 2)
    else:
        return bounds.height


def render_el_drop_files(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
    data: PlayListData,
) -> None:
    bounds = pr.Rectangle(cell_x, cell_y, cell_width * 12, cell_height * 11)

    content_height = get_content_height(data, cell_height, bounds)

    content = pr.Rectangle(
        bounds.x,
        bounds.y,
        bounds.width,
        content_height,
    )

    pr.gui_scroll_panel(
        bounds,
        b"Files",
        content,
        data.scroll,
        data.view,
    )

    pr.begin_scissor_mode(
        int(data.view.x),
        int(data.view.y),
        int(data.view.width),
        int(data.view.height),
    )
    draw_file_list(data, bounds, data.scroll, cell_width, cell_height)
    pr.end_scissor_mode()


def draw_file_list(
    data: PlayListData,
    bounds: pr.Rectangle,
    scroll: pr.Vector2,
    cell_width: float,
    cell_height: float,
) -> None:
    for i in range(len(data.file_paths)):
        path = data.file_paths[i]

        if isinstance(path, str):
            path_bytes = path.encode("utf-8")
        else:
            path_bytes = path

        file_name = pr.get_file_name(path_bytes)

        x = int((bounds.x + scroll.x) + (cell_width / 2.0))
        y = int(bounds.y + scroll.y + cell_height * (i + 2))
        pr.draw_rectangle(
            x,
            y,
            int(bounds.width),
            int(cell_height),
            pr.fade(pr.YELLOW, 0.0),
        )

        color = pr.YELLOW if i == data.current_track_index else pr.WHITE
        pr.draw_text(file_name, x, y, int(cell_height / 1.5), color)


def add_file_to_playlist(data: PlayListData) -> None:
    if pr.is_file_dropped():
        dropped_files = pr.load_dropped_files()
        for i in range(dropped_files.count):
            path = pr.ffi.string(dropped_files.paths[i]).decode("utf-8")
            data.file_paths.append(path)
        if data.current_track_index == -1:
            data.current_track_index = 0
        pr.unload_dropped_files(dropped_files)


def load_track(data: PlayListData) -> None:
    path = data.file_paths[data.current_track_index]
    data.music = pr.load_music_stream(path.encode("utf-8"))
    # check if playlist is empty?
    if data.music is None:
        pr.trace_log(pr.LOG_WARNING, f"Failed to load: {path}")


def play_track(data: PlayListData) -> None:
    # check if playlist is empty?
    if data.music is not None:
        pr.play_music_stream(data.music)


def resume_track(data: PlayListData) -> None:
    path = data.file_paths[data.current_track_index]
    # check if is playling?
    if data.music is not None:
        pr.resume_music_stream(data.music)
        print(f"Playing: {path}")


def update_music_stream_if_needed(data: PlayListData) -> None:
    if data.music is not None and pr.is_music_stream_playing(data.music):
        pr.update_music_stream(data.music)


# def get_memory_usage_mb() -> float:
#    usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#    return usage_kb / 1024  # convert KB → MB on Linux
# print(f"Memory usage: {get_memory_usage_mb():.2f} MB")
