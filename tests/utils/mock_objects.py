"""Mock objects used in UI testing"""

class MockVideoPlayer:
    """Mock video player for testing tag controls"""
    def __init__(self, current_time=10.0):
        self._current_time = current_time

    def get_time(self):
        return self._current_time

    def set_time(self, time):
        self._current_time = time

    def play(self):
        pass

    def pause(self):
        pass