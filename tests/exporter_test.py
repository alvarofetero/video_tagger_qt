import os
import unittest
import subprocess  # Add this import for subprocess mocking
from unittest.mock import patch, MagicMock
from PyQt5.QtCore import QThread
from src.exporter import ExporterThread

class TestExporterThread(unittest.TestCase):
    def setUp(self):
        self.tags = [
            {"start": "00:00:00", "end": "00:00:10"},
            {"start": "00:00:10", "end": "00:00:20"}
        ]
        self.video_path = "test_video.mp4"
        self.output_dir = "output"
        self.filename_base = "clip"
        self.exporter = ExporterThread(self.tags, self.video_path, self.output_dir, self.filename_base)

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    @patch("subprocess.run")
    def test_run(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock()

        progress_mock = MagicMock()
        finished_mock = MagicMock()

        self.exporter.progress.connect(progress_mock)
        self.exporter.finished.connect(finished_mock)

        self.exporter.run()

        # Check if subprocess.run was called for each tag
        self.assertEqual(mock_subprocess_run.call_count, len(self.tags))

        # Verify the commands passed to subprocess.run
        for i, tag in enumerate(self.tags):
            output_filename = f"{self.filename_base}_{i+1}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            expected_command = [
                "ffmpeg", "-y", "-i", self.video_path,
                "-ss", str(tag["start"]),
                "-to", str(tag["end"]),
                "-c:v", "libx264", "-c:a", "aac",
                "-strict", "experimental", output_path
            ]
            mock_subprocess_run.assert_any_call(expected_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Check if progress signal was emitted correctly
        self.assertEqual(progress_mock.call_count, len(self.tags))
        progress_mock.assert_any_call(1)
        progress_mock.assert_any_call(2)

        # Check if finished signal was emitted
        finished_mock.assert_called_once()

    def tearDown(self):
        # Clean up the output directory
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)

if __name__ == "__main__":
    unittest.main()