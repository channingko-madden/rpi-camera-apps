# rpi-camera-apps
Raspberry Pi apps that use the camera module.

## Dependencies 

This project uses Picamera2, and therefore only supports Raspberry PI OS Bullseye or later.
See [here](https://github.com/raspberrypi/picamera2) for instructions for installing Picamera2.

I am using Poetry for dev dependencies only right now. I have not gotten 
Poetry to work nicely and use the system installed Picamera2 package and
its dependencies. Trying to install Picamera2 and dependencies purely
through Poetry ends up freezing the Pi.
