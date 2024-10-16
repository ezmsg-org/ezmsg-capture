import cv2
import time
import ezmsg.core as ez
from ezmsg.util.messages.axisarray import AxisArray
from typing import Iterable, Optional

from .__version__ import __version__ as __version__


class VideoCaptureSettings(ez.Settings):
    camera_index: Optional[int] = None
    color_conversion: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    crop: Optional[Iterable[slice]] = None


class VideoCaptureState(ez.State):
    cam: cv2.VideoCapture
    fps: float
    width: int
    height: int


class VideoCapture(ez.Unit):
    SETTINGS = VideoCaptureSettings
    STATE = VideoCaptureState

    OUTPUT_SIGNAL = ez.OutputStream(AxisArray)

    async def initialize(self) -> None:
        if self.SETTINGS.camera_index is None:
            index = 0
        else:
            index = self.SETTINGS.camera_index

        self.STATE.cam = cv2.VideoCapture(index)
        if self.SETTINGS.width is not None:
            self.STATE.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.SETTINGS.width)
        if self.SETTINGS.height is not None:
            self.STATE.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.SETTINGS.height)

        self.STATE.width = int(self.STATE.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.STATE.height = int(self.STATE.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.STATE.fps = self.STATE.cam.get(cv2.CAP_PROP_FPS)

    @ez.publisher(OUTPUT_SIGNAL)
    async def on_image(self):
        while True:
            _, frame = self.STATE.cam.read()
            if self.SETTINGS.color_conversion is not None:
                frame = cv2.cvtColor(frame, self.SETTINGS.color_conversion)
            if self.SETTINGS.crop is not None:
                frame = frame[*self.SETTINGS.crop]
            if frame.ndim == 2:
                yield (
                    self.OUTPUT_SIGNAL,
                    AxisArray(
                        data=frame[None],
                        dims=["time", "rows", "cols"],
                        axes={
                            "time": AxisArray.Axis.TimeAxis(
                                fs=self.STATE.fps, offset=time.time()
                            ),
                            "rows": AxisArray.Axis(),
                            "cols": AxisArray.Axis(),
                        },
                    ),
                )
            elif frame.ndim == 3:
                yield (
                    self.OUTPUT_SIGNAL,
                    AxisArray(
                        data=frame[None],
                        dims=["time", "rows", "cols", "color"],
                        axes={
                            "time": AxisArray.Axis.TimeAxis(
                                fs=self.STATE.fps, offset=time.time()
                            ),
                            "rows": AxisArray.Axis(),
                            "cols": AxisArray.Axis(),
                            "color": AxisArray.Axis(),
                        },
                    ),
                )
            else:
                raise Exception(
                    "Expected image from webcam to be either two or three dimensions"
                )
