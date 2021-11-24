
from picamera import PiCamera


if __name__ == '__main__':
    with PiCamera() as camera:
        camera.start_preview()
        sleep(1)
        camera.capture('test_cam.jpg')
        camera.stop_preview()
