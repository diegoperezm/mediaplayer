from utils import (
    BGCOLOR,
    AudioPlayer,
    PlayListData,
    State,
    add_file_to_playlist,
    init_raylib,
    pr,
    render_ui,
    update_music_stream_if_needed,
)


def main() -> None:
    init_raylib()
    pr.init_audio_device()
    audio_player: AudioPlayer = AudioPlayer(State.WAITING)
    data: PlayListData = PlayListData()

    while not pr.window_should_close():
        if pr.is_file_dropped():
            add_file_to_playlist(data)

        update_music_stream_if_needed(data)
        pr.begin_drawing()
        pr.clear_background(BGCOLOR)
        render_ui(audio_player, data)
        pr.end_drawing()

    pr.close_audio_device()
    pr.close_window()


if __name__ == "__main__":
    main()
