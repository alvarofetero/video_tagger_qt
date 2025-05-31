import pytest
from PyQt5.QtCore import Qt
from src.player import VideoPlayer

def test_video_player_init(qtbot):
    """Test that video player initializes correctly"""
    player = VideoPlayer()
    qtbot.addWidget(player)
    
    # Check initial state
    assert player.video_frame is not None
    assert player.mediaplayer is not None
    assert player.timer is not None

def test_video_player_speed_change(qtbot):
    """Test video player speed changes"""
    player = VideoPlayer()
    qtbot.addWidget(player)
    
    # Track speed change signals
    speed_changes = []
    player.speed_changed.connect(lambda rate: speed_changes.append(rate))
    
    # Test speed increase
    player.change_speed(0.25)
    assert len(speed_changes) == 1
    assert speed_changes[0] == 1.25  # Default 1.0 + 0.25
    
    # Test speed decrease
    player.change_speed(-0.25)
    assert len(speed_changes) == 2
    assert speed_changes[1] == 1.0  # Back to default

def test_video_player_time_signal(qtbot):
    """Test that time change signals are emitted correctly"""
    player = VideoPlayer()
    qtbot.addWidget(player)
    
    # Track time signals
    time_signals = []
    player.time_changed.connect(lambda t: time_signals.append(t))
    
    # Mock the mediaplayer methods
    player.mediaplayer.is_playing = lambda: True
    player.mediaplayer.get_time = lambda: 5000  # 5 seconds in milliseconds
    
    # Trigger the timer manually
    player.update_time()
    
    # Verify signal was emitted with correct time
    assert len(time_signals) == 1
    assert time_signals[0] == 5.0  # Should convert ms to seconds