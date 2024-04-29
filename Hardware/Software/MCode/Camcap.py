from picamera import PiCamera
from time import sleep
from datetime import datetime


class Rpi_Cam(object):

    def __init__(self):
        self.camera = PiCamera()

    def imgCap(self):
        now = datetime.now()
        dt = now.strftime("%d%m%Y%H:%M:%S")
        name = dt+".jpg"
        self.camera.resolution = (1920, 1080)
        self.camera.flash_mode = 'on'
        self.camera.awb_mode = 'auto'
        self.camera.brightness = 40
        self.camera.sharpness = 60
        self.camera.image_effect = 'colorbalance'
        self.camera.zoom = (0.05, 0.05, 0.8, 0.9)
        self.camera.capture(name)
        # from picamera import PiCamera, Color
        # camera.brightness = 70
        # camera.image_effect = 'colorswap'
        # camera.exposure_mode = 'beach'
        # camera.awb_mode = 'sunlight'
        # camera.annotate_background = Color('blue')
        # camera.annotate_foreground = Color('yellow')
        # camera.annotate_text = " Hello world "
        return name

    def strt_vid(self):
        now = datetime.now()
        dt = now.strftime("%d%m%Y%H:%M:%S")
        name = dt+".h264"
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 15
        self.camera.flash_mode = 'auto'
        self.camera.awb_mode = 'auto'
        self.camera.brightness = 40
        self.camera.sharpness = 60
        self.camera.image_effect = 'colorbalance'
        self.camera.zoom = (0.05, 0.05, 0.8, 0.9)
        self.camera.start_recording(name)
        sleep(5)
        self.camera.stop_recording()
        return name

    def CamClose(self):
        self.camera.close()

    # def vidCap(self):
    #     self._thread = threading.Thread(target=self.strt_vid)
    #     self._thread.stopped = False
    #     self._thread.start()

    # def vidStp(self, timeout=2.0):
    #     self._thread.stopped = True
    #     self._thread.join(timeout)
