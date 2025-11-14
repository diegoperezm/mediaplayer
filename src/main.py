from utils import *


def main() -> None:
    init_raylib()
    init_audio_device()
    mp3_player: MusicPlayer = Mp3Player(State.WAITING)
    data: PlaylistData = PlaylistData()

    while not window_should_close():
        if is_file_dropped():
            add_file_to_playlist(data)

        update_music_stream_if_needed(data)
        begin_drawing()
        clear_background(BGCOLOR)
        render_ui(mp3_player, data)
        end_drawing()

    close_audio_device()
    close_window()


if __name__ == "__main__":
    main()
