from utils import * 

def main() -> None:
    init_raylib()
    init_audio_device()
    music_player: MusicPlayer = MusicPlayer(State.WAITING)
    data: PlayListData = PlayListData()

    while not window_should_close():
        if is_file_dropped():
            add_file_to_playlist(data)

        update_music_stream_if_needed(data)
        begin_drawing()
        clear_background(BGCOLOR)
        render_ui(music_player, data)
        end_drawing()

    close_audio_device()
    close_window()


if __name__ == "__main__":
    main()
