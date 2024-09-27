import cv2

# Open the default camera
cam = cv2.VideoCapture(0)
ret = cam.set(cv2.CAP_PROP_FPS, 60.0)
fps = cam.get(cv2.CAP_PROP_FPS)
print(f"{fps=}, {ret=}")

# Get the default frame width and height
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cam.read()
    # if frame.ndim > 2:
    # Use the cvtColor() function to grayscale the image
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Display the captured frame
    cv2.imshow("Camera", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord("q"):
        break

# Release the capture and writer objects
cam.release()
cv2.destroyAllWindows()
