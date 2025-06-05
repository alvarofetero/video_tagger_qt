# FFmpeg-based export logic
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import os
import re
from src.utils.logger import AppLogger

class ExporterThread(QThread):
    progress = pyqtSignal(int)  # Overall progress (0-100)
    clip_progress = pyqtSignal(int, int)  # Current clip progress (clip_index, progress 0-100)
    finished = pyqtSignal()

    def __init__(self, tags, video_path, output_dir, filename_base):
        super().__init__()
        self.tags = tags
        self.video_path = video_path
        self.output_dir = output_dir
        self.filename_base = filename_base
        self.logger = AppLogger.get_logger()

    def run(self):
        total_clips = len(self.tags)
        for i, tag in enumerate(self.tags):
            if tag["end"]:
                start_time = tag["start"]
                end_time = tag["end"]
                output_filename = f"{i+1:03d}_{tag['category']}_{i+1}.mp4"
                output_path = os.path.join(self.output_dir, output_filename)

                # Log the current clip being processed
                self.logger.info(f"Processing clip {i+1}/{total_clips}: {output_filename}")

                # Get video duration using ffmpeg
                duration = end_time - start_time
                fps = 25  # Assuming 25fps
                total_frames = int(duration * fps)

                # Construct FFmpeg command
                command = [
                    "ffmpeg", "-y",
                    "-i", self.video_path,
                    "-ss", str(start_time),
                    "-to", str(end_time),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-f", "mp4",
                    "-stats",
                    output_path
                ]

                # Start FFmpeg process
                process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    bufsize=1
                )

                # Send initial progress update for this clip
                self.clip_progress.emit(i, 0)
                overall_progress = int((i * 100) / total_clips)
                self.progress.emit(overall_progress)

                frame_count = 0
                while True:
                    # Read from stderr for FFmpeg progress
                    line = process.stderr.readline()
                    if not line and process.poll() is not None:
                        break
                    
                    # Try to parse frame information
                    if "frame=" in line:
                        try:
                            frame_match = re.search(r"frame=\s*(\d+)", line)
                            if frame_match:
                                frame_count = int(frame_match.group(1))
                                # Calculate progress percentages
                                clip_progress = min(100, int((frame_count / total_frames) * 100))
                                self.clip_progress.emit(i, clip_progress)
                                
                                # Calculate overall progress
                                overall_progress = int(((i * 100) + clip_progress) / total_clips)
                                self.progress.emit(overall_progress)
                                self.logger.debug(f"Progress - Clip: {clip_progress}%, Overall: {overall_progress}%")
                        except (ValueError, ZeroDivisionError) as e:
                            self.logger.error(f"Error parsing frame number: {e}")

                # Wait for process to complete
                process.wait()

                # Ensure 100% progress is emitted for this clip
                self.clip_progress.emit(i, 100)
                overall_progress = int(((i + 1) * 100) / total_clips)
                self.progress.emit(overall_progress)
                self.logger.info(f"Completed clip {i+1}: {output_filename}")

        # Final progress update
        self.progress.emit(100)
        self.finished.emit()
        self.logger.info("Export completed successfully")
