from utils import *

def main():
  media_player: MediaPlayer = MediaPlayer();
  init_raylib()
  while not window_should_close():
    begin_drawing()
    clear_background(WHITE)
    render_ui(media_player)
    end_drawing()
  close_window()

if __name__ == "__main__":
  main()


