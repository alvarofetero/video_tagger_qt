# FFmpeg-based export logic
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import os

class ExporterThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, tags, video_path, output_dir, filename_base):
        super().__init__()
        self.tags = tags
        self.video_path = video_path
        self.output_dir = output_dir
        self.filename_base = filename_base

    def run(self):
        total = len(self.tags)
        for i, tag in enumerate(self.tags):
            if tag["end"]:
                start_time = tag["start"]
                end_time = tag["end"]
                output_filename = f"{self.filename_base}_{i+1}.mp4"
                output_path = os.path.join(self.output_dir, output_filename)

                command = [
                    "ffmpeg", "-y", "-i", self.video_path,
                    "-ss", str(start_time),
                    "-to", str(end_time),
                    "-c:v", "libx264", "-c:a", "aac",
                    "-strict", "experimental", output_path
                ]
                subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                self.progress.emit(i + 1)

        self.finished.emit()
