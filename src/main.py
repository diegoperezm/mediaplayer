from utils import (
    MediaData,
    MediaPlayer,
    State,
    add_file_to_playlist,
    init_raylib,
    pr,
    render_ui,
    update_music_stream_if_needed,
    update_state,
)


def main() -> None:
    init_raylib()
    pr.init_audio_device()
    media_player: MediaPlayer = MediaPlayer(State.WAITING)
    data: MediaData = MediaData()

    while not pr.window_should_close():
        if pr.is_file_dropped():
            add_file_to_playlist(data)

        update_music_stream_if_needed(data)
        pr.begin_drawing()
        pr.clear_background(pr.WHITE)
        render_ui(media_player, data)
        pr.end_drawing()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
