import json

# This is a simple tag manager for video tagging applications.
# It allows adding, removing, and saving tags with start and end times.
class TagManager:
    def __init__(self):
        self.tags = []
        self.offset = 0.0

    # Set the offset for the tags. This is useful for synchronizing tags with video playback.
    # The offset is subtracted from the start time of each tag when it is added.
    def set_offset(self, seconds):
        self.offset = seconds

    # Add a start tag at the specified time in seconds.
    # The start time is adjusted by the offset, ensuring it doesn't go below 0.0 seconds.
    def add_start(self, time_sec, category="General"):
        self.tags.append({
            "start": max(0.0, time_sec - self.offset),
            "end": None,
            "category": category
        })
        print(f"[TAG] Inicio ajustado en {time_sec:.2f}s")

    def add_end(self, time_sec):
        if self.tags and self.tags[-1]["end"] is None:
            self.tags[-1]["end"] = time_sec

    def remove_tag(self, index):
        if 0 <= index < len(self.tags):
            self.tags.pop(index)

    def get_tags(self):
        return self.tags

    def save_tags(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.tags, f, indent=2)
            return True
        return False

    def load_tags(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            self.tags = json.load(f)
