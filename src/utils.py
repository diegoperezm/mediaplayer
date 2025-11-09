import pyray  as pr
import raylib as rl
from enum import Enum
from dataclasses import dataclass,field
from typing import Dict, List, Optional

BGCOLOR = pr.Color(0, 34, 43, 255)
MAX_FILEPATH_RECORDED = 256
MAX_FILEPATH_SIZE = 512
panelScroll = pr.Vector2(0, 0)
panelView = pr.Rectangle(0, 0, 0, 0)
curr_pos = pr.ffi.new('float *', 1.0)
curr_vol_level = pr.ffi.new('float *', 1.0)

GRID_COLS = 12
GRID_ROWS = 12
SIZE_ROWS = 12
SIZE_COLS = 12

class State(Enum):
  WAITING = "WAITING"
  PLAY    = "PLAY"
  PAUSE   = "PAUSE"
  STOP    = "STOP"
  PREV    = "PREV"
  NEXT    = "NEXT"
  INVALID = "INVALID"

class Event(Enum):
  play  = "evt_play"
  pause = "evt_pause"
  stop  = "evt_stop"
  prev  = "evt_prev"
  next  = "evt_next"

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
class MediaData:
    file_paths: list = field(default_factory=list)
    file_path_counter: int = 0          
    music: Optional[pr.Music] = None
    current_track_index: int = -1
    is_playing: bool = False
    current_time: float = 0.0
    total_time: float = 0.0
    volume: float = 1.0

@dataclass
class MediaPlayer:
    current_state: State = State.WAITING

_map_default: List[List[int]] = [[0] * SIZE_COLS for _ in range(SIZE_ROWS)]

_map_state_waiting: List[List[int]] = [
    [Element.EL_DROP_FILES.value, 0, 0, 0, 0, 0,0,0,0,0,0,0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0],
    [Element.EL_BTN_PREV.value,
     Element.EL_BTN_PLAY.value,
     Element.EL_BTN_STOP.value,
     Element.EL_BTN_NEXT.value,
     Element.EL_PROGRESS_BAR.value,
     Element.EL_VOLUME_SLIDER.value,0,0,0,0,0,0],
]

_map_state_play: List[List[int]] = [
    [Element.EL_DROP_FILES.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [Element.EL_BTN_PREV.value,
     Element.EL_BTN_PAUSE.value,  # <- Different from waiting
     Element.EL_BTN_STOP.value,
     Element.EL_BTN_NEXT.value,
     Element.EL_PROGRESS_BAR.value,
     Element.EL_VOLUME_SLIDER.value,0,0,0,0,0,0],
]

transition_table: Dict[State, Dict[Event, State]] = {
    State.WAITING: {
        Event.play:  State.PLAY,
        Event.pause: State.INVALID,
        Event.stop:  State.INVALID,
        Event.prev:  State.INVALID,
        Event.next:  State.INVALID,
    },
    State.PLAY: {
        Event.play:  State.INVALID,
        Event.pause: State.PAUSE,
        Event.stop:  State.STOP,
        Event.prev:  State.PREV,
        Event.next:  State.NEXT,
    },
    State.PAUSE: {
        Event.play:  State.PLAY,
        Event.pause: State.INVALID,
        Event.stop:  State.STOP,
        Event.prev:  State.PREV,
        Event.next:  State.NEXT,
    },
    State.STOP: {
        Event.play:  State.PLAY,
        Event.pause: State.INVALID,
        Event.stop:  State.INVALID,
        Event.prev:  State.PREV,
        Event.next:  State.NEXT,
    },
    State.PREV: {
        Event.play:  State.PLAY,
        Event.pause: State.INVALID,
        Event.stop:  State.INVALID,
        Event.prev:  State.INVALID,
        Event.next:  State.INVALID,
    },
    State.NEXT: {
        Event.play:  State.PLAY,
        Event.pause: State.INVALID,
        Event.stop:  State.INVALID,
        Event.prev:  State.INVALID,
        Event.next:  State.INVALID,
    },
}

# not sure -> bool
def update_state(media_player: MediaPlayer, event: Event) -> bool:
  current_state = media_player.current_state
  next_state = transition_table[current_state].get(event, State.INVALID)

  if next_state is State.INVALID:
    print(f"Invalid transition: {event.name} from {current_state.name}")
    return False
    
  media_player.current_state = next_state
  print(f"{current_state.name} -> {next_state.name}")
  return True

def init_raylib() -> None :
  screen_w = 800
  screen_h = 600
  pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
  pr.init_window(screen_w, screen_h, b"Media Player")
  pr.set_target_fps(1)
  pr.init_audio_device()
  rl.GuiLoadStyle(b"assets/style_cyber.rgs")

def return_layout(media_player: MediaPlayer) -> List[List[int]]:  
  match media_player.current_state: 
    case State.PLAY:
      return _map_state_play
    case State.WAITING | State.PAUSE | State.STOP | State.PREV | State.NEXT:
      return _map_state_waiting
    case _:
      return _map_default
  
def render_ui(media_player: MediaPlayer, data: MediaData) -> None:
  layout  = return_layout(media_player)

  width = pr.get_screen_width()
  height = pr.get_screen_height()
  cell_width = width / GRID_COLS
  cell_height = height / GRID_ROWS

  for row, row_data in enumerate(layout):
    for col, element in enumerate(row_data):
      cell_x = col * cell_width
      cell_y = row * cell_height

      drop_files_bounds   = pr.Rectangle(cell_x, cell_y, cell_width * 12, cell_height * 11)
      control_btn_bounds  = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)
      progress_bar_bounds = pr.Rectangle(cell_x, cell_y, cell_width * 8, cell_height / 2)
      volume_bar_bounds   = pr.Rectangle(cell_x, cell_y + (cell_height / 2), cell_width * 7, cell_height / 2)


      match element: 
        case Element.EL_BLANK.value: 
          pass

        case Element.EL_PROGRESS_BAR.value: 
          render_el_progress_bar(progress_bar_bounds,curr_pos)

        case Element.EL_BTN_PREV.value:
          render_el_btn_prev(control_btn_bounds)

        case Element.EL_BTN_PLAY.value:
          render_el_btn_play(control_btn_bounds)

        case Element.EL_BTN_PAUSE.value:
         render_el_btn_pause(control_btn_bounds)

        case Element.EL_BTN_STOP.value:
          render_el_btn_stop(control_btn_bounds)

        case Element.EL_BTN_NEXT.value:
          render_el_btn_next(control_btn_bounds)

        case Element.EL_VOLUME_SLIDER.value:
          render_el_volume_slider(volume_bar_bounds,curr_vol_level)

        case Element.EL_DROP_FILES.value:
          render_el_drop_files(drop_files_bounds, data, panelScroll, panelView, cell_width, cell_height)

def render_el_progress_bar(progress_bar_bounds: pr.Rectangle, curr_pos: int) -> None:
  pr.gui_progress_bar(progress_bar_bounds,b"",b"",curr_pos,0,10)

def render_el_btn_prev(control_btn_bounds: pr.Rectangle) -> None:
  pr.gui_button(control_btn_bounds, b"<<")

def render_el_btn_play(control_btn_bounds: pr.Rectangle) -> None:
  pr.gui_button(control_btn_bounds, b">")

def render_el_btn_pause(control_btn_bounds: pr.Rectangle) -> None:
  pr.gui_button(control_btn_bounds, b"||")

def render_el_btn_stop(control_btn_bounds: pr.Rectangle) -> None:
  pr.gui_button(control_btn_bounds, b"[]")

def render_el_btn_next(control_btn_bounds: pr.Rectangle) -> None:
  pr.gui_button(control_btn_bounds, b">>")

def render_el_volume_slider(volume_bar_bounds: pr.Rectangle,curr_vol_level: int) -> None:
  pr.gui_slider(volume_bar_bounds, b"VOL ", b"", curr_vol_level, 0,10)

def render_el_drop_files(drop_files_bounds: pr.Rectangle, data: MediaData, panelScroll: pr.Vector2, panelView: pr.Rectangle, cell_width: float, cell_height: float) -> None:
  pr.gui_scroll_panel(drop_files_bounds, b"Files", drop_files_bounds, panelScroll, panelView)
  pr.begin_scissor_mode(int(panelView.x), int(panelView.y), int(panelView.width), int(panelView.height))
  draw_file_list(data, drop_files_bounds, cell_width, cell_height)
  pr.end_scissor_mode()


def draw_file_list(data: MediaData, bounds: pr.Rectangle, cell_width: float, cell_height: float) -> None:
  for i in range(data.file_path_counter):
      path = data.file_paths[i]

      if isinstance(path, str):
          path_bytes = path.encode('utf-8')
      else:
          path_bytes = path  
  
      file_name = pr.get_file_name(path_bytes)
  
      x = int((bounds.x + panelScroll.x) + (cell_width/2.0))
      y = int(bounds.y + panelScroll.y + cell_height * (i+2))
      pr.draw_rectangle(
        x, 
        y, 
        int(bounds.width),
        int(cell_height),
        pr.fade(pr.YELLOW, 0.0))
 
      color = pr.YELLOW if i == data.current_track_index else pr.WHITE
      pr.draw_text(file_name, x, y, int(cell_height/1.5), color)

def load_and_play_track(data: MediaData, media_player: MediaPlayer, index: int) -> None:
    if data.music is not None:
        pr.stop_music_stream(data.music)
        pr.unload_music_stream(data.music)
        data.music = None
        data.is_playing = False
    if index < 0 or data.file_paths is None or index >= len(data.file_paths):
        return
    path = data.file_paths[index]
    data.music = pr.load_music_stream(path.encode('utf-8'))
    if data.music is None:
        print(f"Failed to load: {path}")
        return
    pr.play_music_stream(data.music)
    data.current_track_index = index
    data.is_playing = True
    print(f"Playing: {path}")

def update_music_stream_if_needed(data: MediaData) -> None:
    if data.music is not None and data.is_playing:
        pr.update_music_stream(data.music)
        # If you want to detect end-of-stream you can use IsMusicStreamPlaying or other logic
        if not pr.is_music_stream_playing(data.music):
            # Music finished
            data.is_playing = False
"""
def handle_button_play(media_player, data: MediaData):
    if gui.gui_button(data.control_btn_bounds, b">"):
        if data.file_path_counter == 0:
            return  # nothing to play

        # If there is already a music stream loaded
        if data.music is not None:
            # If currently paused / not playing, resume; else do nothing or restart
            if not pr.is_music_stream_playing(data.music):
                pr.play_music_stream(data.music)     # resume / start
                data.is_playing = True
                print("Resuming playback")
            else:
                # already playing — optionally restart or ignore
                print("Already playing")
        else:
            # No music loaded: load and play the first (or current) track
            # pick a sensible index: either 0 or data.current_index + 1 logic
            next_index = 0 if data.current_index < 0 else data.current_index
            load_and_play_track(data, next_index)

        update_state(media_player, event_play)

   def next_track(self) -> None:
        if self.filePaths:
            self.currentTrackIndex = (self.currentTrackIndex + 1) % len(self.filePaths)

    def prev_track(self) -> None:
        if self.filePaths:
            self.currentTrackIndex = (self.currentTrackIndex - 1) % len(self.filePaths)
"""


