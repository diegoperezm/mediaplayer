import pyray  as pr
import raylib as rl
from enum   import Enum
from typing import Dict, List

#import pdb

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

class MediaPlayer:
    def __init__(self, initial_state: State = State.WAITING) -> None:
        self.currentState = initial_state

        self.filePaths: list[str] = []         
        self.filePathCounter: int = 0          
        self.currentTrackIndex: int = 0        

        self.isPlaying: bool = False
        self.currentTime: float = 0.0
        self.totalTime: float = 0.0
        self.volume: float = 1.0

        self.music = None  # rl.Music object or None

    def add_file(self, path: str) -> None:
        self.filePaths.append(path)
        self.filePathCounter = len(self.filePaths)

    def next_track(self) -> None:
        if self.filePaths:
            self.currentTrackIndex = (self.currentTrackIndex + 1) % len(self.filePaths)

    def prev_track(self) -> None:
        if self.filePaths:
            self.currentTrackIndex = (self.currentTrackIndex - 1) % len(self.filePaths)



# not sure -> bool
def update_state(media_player: MediaPlayer, event: Event) -> bool:
  current_state = media_player.current_state
  next_state = transition_table[current_state].get(event, State.INVALID)

  if next_state is State.INVALID:
    print(f"Invalid transition: {event.name} from {current_state.name}");
    return False
    
  media_player.current_state = next_state
  print(f"{current_state.name} -> {next_state.name}");
  return True

def init_raylib():
  screen_w = 800
  screen_h = 600
  pr.set_config_flags(pr.FLAG_WINDOW_RESIZABLE)
  pr.init_window(screen_w, screen_h, "Media Player")
  pr.set_target_fps(30);
  rl.GuiLoadStyle(b"assets/style_cyber.rgs")

def return_layout(media_player: MediaPlayer) -> List[List[int]]:  
  match media_player.currentState: 
    case State.PLAY:
      return _map_state_play
    case State.WAITING | State.PAUSE | State.STOP | State.PREV | State.NEXT:
      return _map_state_waiting
    case _:
      return _map_default
  
def render_ui(media_player: MediaPlayer) -> None:
  layout  = return_layout(media_player);

  width = pr.get_screen_width();
  height = pr.get_screen_height();
  cell_width = width / GRID_COLS;
  cell_height = height / GRID_ROWS;

  for row, row_data in enumerate(layout):
    for col, element in enumerate(row_data):
      cell_x = col * cell_width;
      cell_y = row * cell_height;

      drop_files_bounds   = pr.Rectangle(cell_x, cell_y, cell_width * 12, cell_height * 11)
      control_btn_bounds  = pr.Rectangle(cell_x, cell_y, cell_width, cell_height)
      progress_bar_bounds = pr.Rectangle(cell_x, cell_y, cell_width * 8, cell_height / 2)
      volume_bar_bounds   = pr.Rectangle(cell_x, cell_y + (cell_height / 2), cell_width * (7), cell_height / 2)


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
          render_el_drop_files(drop_files_bounds, media_player, panelScroll, panelView, cell_width, cell_height)

def render_el_progress_bar(progress_bar_bounds,curr_pos):
  pr.gui_progress_bar(progress_bar_bounds,"","",curr_pos,0,10)

def render_el_btn_prev(control_btn_bounds):
  pr.gui_button(control_btn_bounds, "<<")

def render_el_btn_play(control_btn_bounds):
  pr.gui_button(control_btn_bounds, ">")

def render_el_btn_pause(control_btn_bounds):
  pr.gui_button(control_btn_bounds, "||")

def render_el_btn_stop(control_btn_bounds):
  pr.gui_button(control_btn_bounds, "[]")

def render_el_btn_next(control_btn_bounds):
  pr.gui_button(control_btn_bounds, ">>")

def render_el_volume_slider(volume_bar_bounds,curr_vol_level):
  pr.gui_slider(volume_bar_bounds, "VOL ", "", curr_vol_level, 0,10)  

def render_el_drop_files(drop_files_bounds, media_player, panelScroll, panelView,cell_width,cell_height):
  pr.gui_scroll_panel(drop_files_bounds, b"Files", drop_files_bounds, panelScroll, panelView)
  pr.begin_scissor_mode(int(panelView.x), int(panelView.y), int(panelView.width), int(panelView.height))
  draw_file_list(media_player, drop_files_bounds, cell_width, cell_height)
  pr.end_scissor_mode()


def draw_file_list(data, bounds, cell_width, cell_height):
  for i in range(data.filePathCounter):
      path = data.filePaths[i]
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
 
      color = pr.YELLOW if i == data.currentTrackIndex else pr.WHITE
      pr.draw_text(file_name, x, y, int(cell_height/1.5), color)
         

