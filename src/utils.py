from pyray  import * 
from enum   import Enum
from typing import Dict, List

#import pdb

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
    [Element.EL_DROP_FILES.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BTN_PREV.value,
     Element.EL_BTN_PLAY.value,
     Element.EL_BTN_STOP.value,
     Element.EL_BTN_NEXT.value,
     Element.EL_PROGRESS_BAR.value,
     Element.EL_VOLUME_SLIDER.value],
]

_map_state_play: List[List[int]] = [
    [Element.EL_DROP_FILES.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BLANK.value, 0, 0, 0, 0, 0],
    [Element.EL_BTN_PREV.value,
     Element.EL_BTN_PAUSE.value,  # <- Different from waiting
     Element.EL_BTN_STOP.value,
     Element.EL_BTN_NEXT.value,
     Element.EL_PROGRESS_BAR.value,
     Element.EL_VOLUME_SLIDER.value],
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
    self.current_state = initial_state;

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
  set_config_flags(FLAG_WINDOW_RESIZABLE)
  init_window(screen_w, screen_h, "Media Player")
  set_target_fps(30);

def return_layout(media_player: MediaPlayer) -> List[List[int]]:  
  match media_player.current_state: 
    case State.PLAY:
      return _map_state_play
    case State.WAITING | State.PAUSE | State.STOP | State.PREV | State.NEXT:
      return _map_state_waiting
    case _:
      return _map_default
  
def render_ui(media_player: MediaPlayer) -> None:

  layout  = return_layout(media_player);

  width = get_screen_width();
  height = get_screen_height();
  cell_width = width / GRID_COLS;
  cell_height = height / GRID_ROWS;

#  breakpoint()
  for row, row_data in enumerate(layout):
    for col, element in enumerate(row_data):
      cell_x = col * cell_width;
      cell_y = row * cell_height;

      drop_files_bounds   = Rectangle( cell_x, cell_y, cell_width * 12, cell_height * 11)
      control_btn_bounds  = Rectangle(cell_x, cell_y, cell_width, cell_height)

      progress_bar_bounds = Rectangle(cell_x, cell_y, cell_width * 8, cell_height / 2)
      volume_bar_bounds   = Rectangle( cell_x, cell_y + (cell_height / 2), cell_width * (7), cell_height / 2)

      scroll  = Vector2(0, 0, 0, 0)
      content = Rectangle(0, 0, 0, 0)

      view = Rectangle(0,0,0,0);

      match element: 
        case Element.EL_BLANK.value: 
          pass

        case Element.EL_BTN_PLAY.value:
          gui_button(Rectangle(10,10,100,32),"TEST")
         



 

