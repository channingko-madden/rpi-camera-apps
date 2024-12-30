"""
Time lapse photo capturing using pi camera

Classes:
    TimeLapseCapture
        - Sync/Async time lapse photo capture with callback
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from picamera2 import Picamera2

from rca.logger import get_logger

logger = get_logger(__name__)


@dataclass
class TimeLapseCapture:
    """
    A class to capture time lapse photos asynchronously or synchronously, and call a
    callback when all photos are captured

    Attributes
    ----------
    image_folder : Path
        File path to where to temporarily store images
    image_count : int
        The number of images to capture
    capture_delay : float
        The delay between capturing photos (sec)

    """

    image_folder: Path  # Path to folder where image files can temporarily be stored
    image_count: int = 1  # Number of images to capture for time lapse
    capture_delay: int = 0  # Delay between capturing photos (s)

    def sync_capture(self, callback: Callable[[list[Path]], None]) -> None:
        """
        Block while time lapse capture occurs and call callback once complete

        Args:
            callback : Callback function called when time lapse capture ends, passed a list of image file names.
        """
        with Picamera2() as camera:
            camera_config = camera.create_still_configuration()
            camera.configure(camera_config)
            camera.start()
            try:
                camera.start_and_capture_files(
                    str(self.image_folder / "time_lapse_capture_img{:d}.jpg"),
                    initial_delay=5,
                    delay=self.capture_delay,
                    num_files=self.image_count,
                    # show_preview=False,
                )
                if callable(callback):
                    file_list: list[Path] = [
                        self.image_folder / f"time_lapse_capture_img{x}.jpg" for x in range(0, self.image_count)
                    ]
                    callback(file_list)
            except Exception:
                logger.exception("Encountered an error capturing images")
