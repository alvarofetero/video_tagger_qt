# Project Organization

Here it is explained the structure of the project and the principal functionality of each component.


## UI Components

Folder src/ui

### base_component.py

Base class for all UI components in the application
It is declare the setup_ui() method as a required method for all the subclasses

```python
class BaseComponent(QWidget):
    # Abstract base class for UI components
    # Requires implementation of setup_ui() in subclasses
```

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

```python
class MainWindow(QMainWindow):
    # Main window implementation:
    # - Creates central widget and layout
    # - Initializes and manages:
    #   - TagManager for video tagging
    #   - VideoPlayer for video playback and annotations
    #   - PlayerControls for video control
    #   - TagControls for tag management
    #   - FileControls for file operations
    # - Sets up menus and connections between components
```
### video_player.py
Video playback and annotation component.

```python
class VideoPlayer(QWidget):
    # Handles:
    # - Video playback using VLC
    # - Drawing annotations (arrows, circles, rectangles)
    # - Object tracking
    # - Annotation overlay
    # - Drawing toolbar
    # - Frame capture and processing
```

## drawing_toolbar.py
Toolbar for annotation tools and controls.

```python
class DrawingToolbar(QToolBar):
    # Provides:
    # - Tool selection (arrow, circle, cone, rectangle)
    # - Color picker
    # - Clear annotations button
    # - Save/Load annotation controls
```

### annotation_overlay.py
Overlay for drawing annotations on video.

```python
class AnnotationOverlay(QWidget):
    # Manages:
    # - Drawing tools implementation
    # - Annotation storage and rendering
    # - Tracking box visualization
    # - Save/Load annotations to JSON
```

### file_controls_widget.py
Controls for file operations.

```python
class FileControls(BaseComponent):
    # Provides:
    # - Open video file
    # - Save/Load project
    # - Recent files management
    # - File format handling
```


### tag_widget.py
Interface for managing video tags.

```python
class TagControls(BaseComponent):
    # Handles:
    # - Tag creation and deletion
    # - Tag assignment to timestamps
    # - Tag categories
    # - Tag search and filtering
```

### video_player_controls_widget.py
Video playback control interface.

```python
class PlayerControls(BaseComponent):
    # Provides:
    # - Play/Pause controls
    # - Seek controls
    # - Speed adjustment
    # - Timeline visualization
    # - Frame navigation
```

## Utilities

Folder src/utils

### tracking/object_tracker.py
Object tracking implementation.

```python
class ObjectTracker:
    # Provides:
    # - OpenCV-based object tracking
    # - Bounding box conversion
    # - Track initialization and updates
```


## Configuration

Folder `src/config`
- Application settings
- Default configurations
- User preferences


