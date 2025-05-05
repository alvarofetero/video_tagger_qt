    ## VideoTaggerApp Overview

    VideoTaggerApp is a PyQt5-based application for tagging and exporting clips from a video file. It provides a graphical user interface (GUI) for loading videos, marking start and end points of tags, managing tags, and exporting the tagged clips.

    ### Attributes

    - **video_path** (`str`): Path to the currently loaded video file.
    - **output_directory** (`str`): Directory where exported clips will be saved.
    - **tags** (`list`): List of tags, each represented as a dictionary with `start` and `end` keys.

    ### Methods

    #### `setup_ui()`
    Sets up the user interface, including controls, video player, and timeline.

    #### `seek_to_tag(time_seconds)`
    Seeks the video player to a specific time corresponding to a tag.

    #### `load_video()`
    Opens a file dialog to load a video file and initializes the video player.

    #### `toggle_playback()`
    Toggles between playing and pausing the video.

    #### `mark_start()`
    Marks the start time of a new tag at the current video playback position.

    #### `mark_end()`
    Marks the end time of the most recent tag at the current video playback position.

    #### `update_tag_list()`
    Updates the tag list widget to reflect the current tags.

    #### `delete_selected_tag()`
    Deletes the currently selected tag from the tag list.

    #### `save_tags()`
    Saves the current tags to a JSON file.

    #### `load_tags()`
    Loads tags from a JSON file and updates the tag list.

    #### `change_speed(delta)`
    Adjusts the playback speed of the video by a given delta.

    #### `export_clips()`
    Exports video clips based on the defined tags to the specified output directory.

    #### `on_export_finished()`
    Handles the completion of the export process, re-enabling the export button.
    ```
    Attributes:
        video_path (str): Path to the currently loaded video file.
        output_directory (str): Directory where exported clips will be saved.
        tags (list): List of tags, each represented as a dictionary with 'start' and 'end' keys.
    Methods:
        setup_ui():
            Sets up the user interface, including controls, video player, and timeline.
        seek_to_tag(time_seconds):
            Seeks the video player to a specific time corresponding to a tag.
        load_video():
            Opens a file dialog to load a video file and initializes the video player.
        toggle_playback():
            Toggles between playing and pausing the video.
        mark_start():
            Marks the start time of a new tag at the current video playback position.
        mark_end():
            Marks the end time of the most recent tag at the current video playback position.
        update_tag_list():
            Updates the tag list widget to reflect the current tags.
        delete_selected_tag():
            Deletes the currently selected tag from the tag list.
        save_tags():
            Saves the current tags to a JSON file.
        load_tags():
            Loads tags from a JSON file and updates the tag list.
        change_speed(delta):
            Adjusts the playback speed of the video by a given delta.
        export_clips():
            Exports video clips based on the defined tags to the specified output directory.
        on_export_finished():
            Handles the completion of the export process, re-enabling the export button.
    """