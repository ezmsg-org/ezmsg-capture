import ezmsg.core as ez
import rerun as rr
import rerun.blueprint as rrb
from ezmsg.capture import VideoCapture, VideoCaptureSettings
from ezmsg.util.messages.axisarray import AxisArray


class RerunWebcam(ez.Unit):
    INPUT_SIGNAL = ez.InputStream(AxisArray)

    async def initialize(self) -> None:
        rr.init("ezmsg-capture dev", spawn=True)
        rr.send_blueprint(
            rrb.Blueprint(
                rrb.TensorView(
                    origin="webcam/stream",
                    slice_selection=rrb.TensorSliceSelection(
                        width=1,
                        height=2,
                        indices=[
                            rr.TensorDimensionIndexSelection(dimension=0, index=0),
                        ],
                        slider=[0],
                    ),
                )
            )
        )

    @ez.subscriber(INPUT_SIGNAL)
    async def on_frame(self, message):
        time_arr = message.ax("time").values
        rr.send_columns(
            "webcam/stream",
            times=[rr.TimeSecondsColumn("s", time_arr)],
            components=[rr.components.TensorDataBatch(message.data)],
        )


if __name__ == "__main__":
    crop = [slice(92, 988), slice(320, 1600)]
    cam = VideoCapture(VideoCaptureSettings(width=1920, height=1080, crop=crop))
    view = RerunWebcam()
    ez.run(CAM=cam, VIEWER=view, connections=((cam.OUTPUT_SIGNAL, view.INPUT_SIGNAL),))
