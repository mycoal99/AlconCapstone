import numpy as np
import cv2
from verify import verify
import threading




def verifying(cap):

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
        verify(gray)

if __name__=="__main__":
    cap = cv2.VideoCapture(0)

    verify_fnc = threading.Thread(target=verifying, args=[cap])
    verify_fnc.start()
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            
            break


    
    # When everything done, release the capture
    verify_fnc.join()
    cap.release()
    cv2.destroyAllWindows()