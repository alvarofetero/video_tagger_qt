import os
import tempfile
import unittest
import subprocess
from unittest.mock import patch, MagicMock
from PyQt5.QtCore import QThread
from src.exporter import ExporterThread
from io import StringIO

class TestExporterThread(unittest.TestCase):
    def setUp(self):
        self.tags = [
            {"start": 0.0, "end": 10.0, "category": "Test1"},
            {"start": 10.0, "end": 20.0, "category": "Test2"}
        ]
        self.video_path = os.path.join(tempfile.gettempdir(), "test_video.mp4")
        self.output_dir = os.path.join(tempfile.gettempdir(), "test_output")
        self.filename_base = "clip"
        self.exporter = ExporterThread(self.tags, self.video_path, self.output_dir, self.filename_base)

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    @patch("subprocess.Popen")
    def test_run(self, mock_popen):
        # Setup mock process
        mock_process = MagicMock()
        mock_process.poll.return_value = 0
        mock_process.stderr = StringIO("frame=100\n")  # Simulate ffmpeg output
        mock_popen.return_value = mock_process

        # Setup signal trackers
        progress_values = []
        self.exporter.progress.connect(lambda v: progress_values.append(v))
        finished_called = False
        self.exporter.finished.connect(lambda: setattr(self, 'finished_called', True))

        # Run the export
        self.exporter.run()

        # Verify Popen was called for each tag with correct arguments
        self.assertEqual(mock_popen.call_count, len(self.tags))
        
        # Check calls had correct ffmpeg arguments
        for i, tag in enumerate(self.tags):
            output_filename = f"{tag['category']}_{i+1}.mp4"
            output_path = os.path.join(self.output_dir, output_filename)
            expected_args = [
                "ffmpeg", "-y",
                "-i", self.video_path,
                "-ss", str(tag["start"]),
                "-to", str(tag["end"]),
                "-c:v", "libx264",
                "-c:a", "aac",
                "-f", "mp4",
                "-stats",
                output_path
            ]
            mock_popen.assert_any_call(
                expected_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

        # Verify progress was tracked
        self.assertGreater(len(progress_values), 0)
        self.assertEqual(progress_values[-1], 100)  # Final progress should be 100%

    def tearDown(self):
        # Clean up the output directory if it exists
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                try:
                    os.remove(os.path.join(self.output_dir, file))
                except (OSError, PermissionError):
                    pass
            try:
                os.rmdir(self.output_dir)
            except (OSError, PermissionError):
                pass  # Ignore errors during cleanup

if __name__ == "__main__":
    unittest.main()