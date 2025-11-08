from utils import *

def main():
  init_raylib()

  media_player: MediaPlayer = MediaPlayer(initial_state=State.WAITING)

  while not pr.window_should_close():
    if pr.is_file_dropped():
      dropped_files = pr.load_dropped_files()
      for i in range(dropped_files.count):
        path = pr.ffi.string(dropped_files.paths[i]).decode('utf-8')
        media_player.filePaths.append(path)    
        media_player.filePathCounter += 1
      pr.unload_dropped_files(dropped_files)

    pr.begin_drawing()
    pr.clear_background(pr.WHITE)
    render_ui(media_player)
    pr.end_drawing()

  pr.close_window()

if __name__ == "__main__":
  main()


