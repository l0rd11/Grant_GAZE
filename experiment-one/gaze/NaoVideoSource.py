import cv2
import numpy
import qi
import time

from VideoSource import VideoSource

import vision_definitions

from emotions.emotions import Emotion


class NaoVideoSourceRemote(VideoSource):

    def __init__(self, session):
        self.vd_proxy = session.service("ALVideoDevice")
        self.resolution = vision_definitions.kVGA
        self.colorSpace = vision_definitions.kYuvColorSpace
        self.fps = 20
        self.nameId = None
        self.emotion = Emotion()


    def subscribeCamera(self):
        #subscribe or subscribeCamera?? - subscribe is deprecated
        self.nameId = self.vd_proxy.subscribeCamera("python_GVM6", 0, self.resolution, self.colorSpace, self.fps)
        # self.nameId = self.vd_proxy.subscribe("python_GVM7", self.resolution, self.colorSpace, self.fps)

    def getImage(self):
        image = self.vd_proxy.getImageRemote(self.nameId)
        image_width = image[0]
        image_height = image[1]

        frame = numpy.frombuffer(image[6], numpy.uint8).reshape(image_height, image_width, 1)
        grayImg = numpy.copy(frame)
        grayImg = cv2.cvtColor(grayImg, cv2.COLOR_GRAY2BGR)
        # start = time.time()
        self.emotion.extract_emotions(grayImg)
        # print start - time.time()
        return frame


    def releaseImage(self):
        self.vd_proxy.releaseImage(self.nameId)

    def unsubscribe(self):
        self.vd_proxy.unsubscribe(self.nameId)


class NaoVideoSourceLocal(VideoSource):
    def __init__(self, session):
        self.vd_proxy = session.service("ALVideoDevice")
        self.resolution = vision_definitions.kQVGA
        self.colorSpace = vision_definitions.kYUVColorSpace
        self.fps = 20
        self.nameId = None

    def subscribeCamera(self):
        # TODO - subscribeCamera
        self.nameId = self.vd_proxy.subscribe("python_GVM4", self.resolution, self.colorSpace, self.fps)

    def getImage(self):
        #returns AL::ALImage*
        image = self.vd_proxy.getImageLocal(self.nameId)

        #TODO - extract data from image
        return image

    def releaseImage(self):
        self.vd_proxy.releaseImage(self.nameId)

    def unsubscribe(self):
        self.vd_proxy.unsubscribe(self.nameId)
