from utils import init_raylib, MediaPlayer, MediaData, State, render_ui, pr 

def main() -> None:
  init_raylib()
  media_player: MediaPlayer = MediaPlayer(State.WAITING)
  data: MediaData = MediaData()

  while not pr.window_should_close():
    if pr.is_file_dropped():
      dropped_files = pr.load_dropped_files()
      for i in range(dropped_files.count):
        path = pr.ffi.string(dropped_files.paths[i]).decode('utf-8')
        data.file_paths.append(path)    
        data.file_path_counter += 1
      pr.unload_dropped_files(dropped_files)

    pr.begin_drawing()
    pr.clear_background(pr.WHITE)
    render_ui(media_player, data)
    pr.end_drawing()

  pr.close_audio_device()
  pr.close_window()

if __name__ == "__main__":
  main()


