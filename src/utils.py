from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

#import resource
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
    file_path_counter: int = 0
    current_track_index: int = -1
    current_track_pos: float = pr.ffi.new("float *", 0.0)
    total_track_time: float = pr.ffi.new("float *", 0.0)
    current_vol_level: float = pr.ffi.new("float *", 0.3)


@dataclass
class MediaPlayer:
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

_map_default: List[List[int]] = [
    [0] * SIZE_COLS for _ in range(SIZE_ROWS)
]

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
    media_player: MediaPlayer, event: Event, data: PlayListData
) -> None:
    current_state = media_player.current_state
    next_state = transition_table[current_state].get(
        event, State.INVALID
    )

    if next_state is State.INVALID:
        print(
            f"Invalid transition: {event.name} from {current_state.name}"
        )

    media_player.current_state = next_state
    print(f"{current_state.name} -> {next_state.name}")

    match next_state:
        case State.WAITING:
            pass
        case State.PLAYING:
            if is_playlist_empty(data) is False:
                load_track(data)
                play_track(data)

        case State.RESUMED:
            if is_playlist_empty(data) is False:
                resume_track(data)

        case State.PAUSED:
            if data.music is not None and pr.is_music_stream_playing(
                data.music
            ):
                pr.pause_music_stream(data.music)

        case State.STOPPED:
            if data.music is not None and pr.is_music_stream_playing(
                data.music
            ):
                pr.stop_music_stream(data.music)
                data.current_track_pos[0] = pr.get_music_time_played(data.music)
                pr.unload_music_stream(data.music) # TODO: required? 

        case State.PREV:
            if is_playlist_empty(data) is False:
                data.current_track_index = get_prev_track(data)
                if pr.is_music_stream_playing(data.music): 
                    pr.unload_music_stream(data.music)

            update_state(media_player, Event.play, data)

        case State.NEXT:
            if is_playlist_empty(data) is False:
                data.current_track_index = get_next_track(data)
                if pr.is_music_stream_playing(data.music):
                    pr.unload_music_stream(data.music)
            update_state(media_player, Event.play, data)


def get_prev_track(data: PlayListData) -> int:
    return (
        data.current_track_index - 1 + data.file_path_counter
    ) % data.file_path_counter


def get_next_track(data: PlayListData) -> int:
    return (data.current_track_index + 1) % data.file_path_counter


def is_playlist_empty(data: PlayListData) -> bool:
    return data.file_path_counter <= 0


def init_raylib() -> None:
    screen_w = 800
    screen_h = 600
    pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
    pr.init_window(screen_w, screen_h, b"Media Player")
    pr.set_target_fps(30)
    rl.GuiLoadStyle(b"assets/style_cyber.rgs")


def get_layout(media_player: MediaPlayer) -> List[List[int]]:
    match media_player.current_state:
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


def render_ui(media_player: MediaPlayer, data: PlayListData) -> None:
    layout = get_layout(media_player)

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
                    if clicked:
                        update_state(media_player, Event.prev, data)

                case Element.EL_BTN_PLAY.value:
                    clicked = render_el_btn_play(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked:
                        update_state(media_player, Event.play, data)

                case Element.EL_BTN_PAUSE.value:
                    clicked = render_el_btn_pause(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked:
                        update_state(media_player, Event.pause, data)

                case Element.EL_BTN_STOP.value:
                    clicked = render_el_btn_stop(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked:
                        update_state(media_player, Event.stop, data)

                case Element.EL_BTN_NEXT.value:
                    clicked = render_el_btn_next(
                        cell_x, cell_y, cell_width, cell_height
                    )
                    if clicked:
                        update_state(media_player, Event.next, data)

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
    progress_bar_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width * 8, cell_height / 2
    )

    if data.music is not None and pr.is_music_stream_playing(
        data.music
    ):
        data.current_track_pos[0] = pr.get_music_time_played(data.music)
        data.total_track_time[0] = pr.get_music_time_length(data.music)

    pr.gui_progress_bar(
        progress_bar_bounds,
        b"",
        b"",
        data.current_track_pos,
        0.0,
        data.total_track_time[0],
    )


def render_el_btn_prev(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    control_btn_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width, cell_height
    )

    return pr.gui_button(control_btn_bounds, b"<<")


def render_el_btn_play(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    control_btn_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width, cell_height
    )

    return pr.gui_button(control_btn_bounds, b">")


def render_el_btn_pause(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    control_btn_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width, cell_height
    )

    return pr.gui_button(control_btn_bounds, b"||")


def render_el_btn_stop(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    control_btn_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width, cell_height
    )

    return pr.gui_button(control_btn_bounds, b"[]")


def render_el_btn_next(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
) -> bool:
    control_btn_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width, cell_height
    )

    return pr.gui_button(control_btn_bounds, b">>")


def render_el_volume_slider(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
    data: PlayListData,
) -> None:
    volume_bar_bounds = pr.Rectangle(
        cell_x,
        cell_y + (cell_height / 2),
        cell_width * 7,
        cell_height / 2,
    )

    if data.music is not None:
        pr.set_music_volume(data.music, data.current_vol_level[0])

    pr.gui_slider(
        volume_bar_bounds, b"VOL ", b"", data.current_vol_level, 0, 1
    )


def render_el_drop_files(
    cell_x: float,
    cell_y: float,
    cell_width: float,
    cell_height: float,
    data: PlayListData,
) -> None:
    drop_files_bounds = pr.Rectangle(
        cell_x, cell_y, cell_width * 12, cell_height * 11
    )

    if not hasattr(render_el_drop_files, "scroll"):
        render_el_drop_files.scroll = pr.Vector2(0, 0)
        render_el_drop_files.view = pr.Rectangle(0, 0, 0, 0)

    scroll = render_el_drop_files.scroll
    view = render_el_drop_files.view

    content_height = (
        ((data.file_path_counter * cell_height) + (cell_height * 2.0))
        if (data.file_path_counter * cell_height)
        > drop_files_bounds.height
        else drop_files_bounds.height
    )

    content = pr.Rectangle(
        drop_files_bounds.x,
        drop_files_bounds.y,
        drop_files_bounds.width,
        content_height,
    )

    pr.gui_scroll_panel(
        drop_files_bounds,
        b"Files",
        content,
        scroll,
        view,
    )

    pr.begin_scissor_mode(
        int(view.x), int(view.y), int(view.width), int(view.height)
    )
    draw_file_list(
        data, drop_files_bounds, scroll, cell_width, cell_height
    )
    pr.end_scissor_mode()


def draw_file_list(
    data: PlayListData,
    bounds: pr.Rectangle,
    scroll: pr.Vector2,
    cell_width: float,
    cell_height: float,
) -> None:
    for i in range(data.file_path_counter):
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

        color = (
            pr.YELLOW if i == data.current_track_index else pr.WHITE
        )
        pr.draw_text(file_name, x, y, int(cell_height / 1.5), color)


def add_file_to_playlist(data: PlayListData) -> None:
    if pr.is_file_dropped():
        dropped_files = pr.load_dropped_files()
        for i in range(dropped_files.count):
            path = pr.ffi.string(dropped_files.paths[i]).decode(
                "utf-8"
            )
            data.file_paths.append(path)
            data.file_path_counter += 1
        if data.current_track_index is -1:
            data.current_track_index = 0 
        pr.unload_dropped_files(dropped_files)


def load_track(data: PlayListData) -> None:
    path = data.file_paths[data.current_track_index]
    data.music = pr.load_music_stream(path.encode("utf-8"))
    if data.music is None:
        print(f"Failed to load: {path}")
        return


def play_track(data: PlayListData) -> None:
    path = data.file_paths[data.current_track_index]
    if data.music is not None:
        pr.play_music_stream(data.music)
        print(f"Playing: {path}")


def resume_track(data: PlayListData) -> None:
    path = data.file_paths[data.current_track_index]
    if data.music is not None:
        pr.resume_music_stream(data.music)
        print(f"Playing: {path}")


def update_music_stream_if_needed(data: PlayListData) -> None:
    if data.music is not None and pr.is_music_stream_playing(
        data.music
    ):
        pr.update_music_stream(data.music)



#def get_memory_usage_mb() -> float:
#    usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#    return usage_kb / 1024  # convert KB → MB on Linux
    # print(f"Memory usage: {get_memory_usage_mb():.2f} MB")

