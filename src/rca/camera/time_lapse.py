"""
Time lapse photo capturing using pi camera

Classes:
    TimeLapseCapture
        - Sync/Async time lapse photo capture with callback
"""

##
# file: time_lapse_capture.py
# date: 2021-11-23
# author: Channing Ko-Madden
#
# description: This module contains classes and functions for capturing time lapse photos
# using the pi camera

import time
from picamera import PiCamera


##
# @class TimeLapseCapture
# @brief This class can be used to capture time lapse photos at a certain rate, and a
# callback called when capturing the time lapse photos has ended.
class TimeLapseCapture:
    """
    A class to capture time lapse photos asynchronously or synchronously, and call a
    callback when all photos are captured

    Attributes
    ----------
    image_folder : str
        File path to where to temporarily store images
    image_count : int
        The number of images to capture
    capture_delay : float
        The delay between capturing photos (sec)

    Methods
    -------

    """

    _image_folder = None # Path to folder where image files can temporarily be stored
    _image_count = 0 # Number of images to capture for time lapse
    _capture_delay = 0 # Delay between capturing photos (s)

    @property
    def image_folder(self):
        """
        Getter for image_folder attrbute
        """
        return self._image_folder

    @image_folder.setter
    def image_folder(self, folder):
        """
        Set the file path for image_folder attribute

        Parameters
        ----------
            folder : str
                File path to where to temporarily store images
        """
        self._image_folder = folder

    @property
    def image_count(self):
        """
        Getter for image_image attrbute
        """
        return self._image_count

    @image_count.setter
    def image_count(self, count):
        """
        Set the value for image_count attribute

        Parameters
        ----------
            count : int
                The number of images to capture
        """
        self._image_count = count

    @property
    def capture_delay(self):
        """
        Getter for capture_delay attribute
        """
        return self._capture_delay

    @capture_delay.setter
    def capture_delay(self, delay):
        """
        Set the value for capture_delay attribute
       
        Parameters
        ----------
            delay : float
                The delay between capturing photos (sec)
        """
        self._capture_delay = delay

    def sync_capture(self, callback):
        """
        Block while time lapse capture occurs and call callback once complete

        Parameters
        ----------
            callback : function
                Callback function called when time lapse capture ends, passed a list of str containing the
                image files.
        """
        with PiCamera() as camera:
            camera.start_preview()
            file_list = []
            try:
                for i, filename in enumerate(camera.capture_continuous(self._image_folder + 'img{counter}.jpg')):
                    file_list.append(filename)
                    if i == self._image_count:
                        break
                    time.sleep(self._capture_delay)
                
            finally:
                camera.stop_preview()
                if callable(callback):
                    callback(file_list)
