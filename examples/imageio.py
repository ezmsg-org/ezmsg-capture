from PIL import Image
import imageio as iio

try:
    while True:
        img = iio.imread("<video0>")
        # Convert the frame (numpy array) to an image
        img = Image.fromarray(img)

        # Show the image
        img.show()

        # To avoid opening too many windows, you can use a delay
        img.close()
except KeyboardInterrupt:
    ...
