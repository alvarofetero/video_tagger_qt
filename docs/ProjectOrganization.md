# Project Organization

Here it is explained the structure of the project and the principal functionality of each component.


## UI Components

Folder src/ui

### base_component.py

Base class for all UI components in the application
It is declare the setup_ui() method as a required method for all the subclasses

### main_window.py
Main application window for Video Tagger

This window contains all the components of the application.

 * Create central widget
 * Initialize tag manager
 * Initialize video player first
 * Initialize components
        self.player_controls = PlayerControls(self)
        self.tag_controls = TagControls(self)
        
 * Pass video_player to FileControls
 * Setup menu
 * Setup connections


### file_controls_widget.py

### tag_widget.py

### video_player_controls_widget.py

## Utilities

Folder src/utils

## Configuration


