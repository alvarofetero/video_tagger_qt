class TagManager:
    def __init__(self):
        self.tags = []
        self.offset = 0.0

    def set_offset(self, seconds):
        self.offset = seconds

    def add_start(self, time_sec):
        self.tags.append({"start": max(0.0, time_sec - self.offset), "end": None})

    def add_end(self, time_sec):
        if self.tags and self.tags[-1]["end"] is None:
            self.tags[-1]["end"] = time_sec

    def remove_tag(self, index):
        if 0 <= index < len(self.tags):
            self.tags.pop(index)

    def get_tags(self):
        return self.tags
