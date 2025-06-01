"""Mock classes for VLC components used in testing"""

class MockMediaPlayer:
    def __init__(self):
        self._playing = False
        self._time = 0
        self._rate = 1.0
        self._length = 100000  # Mock 100 seconds

    def play(self): 
        self._playing = True

    def pause(self):
        self._playing = False

    def is_playing(self):
        return self._playing

    def get_time(self):
        return self._time

    def set_time(self, time):
        self._time = time

    def get_length(self):
        return self._length

    def get_rate(self):
        return self._rate

    def set_rate(self, rate):
        self._rate = rate

    def set_hwnd(self, _): pass
    def set_xwindow(self, _): pass
    def set_nsobject(self, _): pass
    def set_media(self, _): pass

class MockVLCInstance:
    def __init__(self, *args): pass
    def media_player_new(self): return MockMediaPlayer()
    def media_new(self, path): return path