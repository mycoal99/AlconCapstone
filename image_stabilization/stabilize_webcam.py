# import libraries
from vidgear.gears import VideoGear
from vidgear.gears import WriteGear
import cv2

stream = VideoGear(source=0, stabilize = True).start() # To open any valid video stream(for e.g device at 0 index)

# infinite loop
while True:

    frame = stream.read()
    # read stabilized frames

    # check if frame is None
    if frame is None:
        #if True break the infinite loop
        break

    # do something with stabilized frame here

    cv2.imshow("Stabilized Frame", frame)
    # Show output window

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        #if 'q' key-pressed break out
        break

cv2.destroyAllWindows()
# close output window

stream.stop()
# safely close video stream