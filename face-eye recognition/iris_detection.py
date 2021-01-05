import numpy as np
import cv2

if __name__ == "__main__":
    cap = cv2.VideoCapture("EyeDetection.mp4")

    video_width = int(cap.get(3))
    video_height = int(cap.get(4))

    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    out = cv2.VideoWriter(("output.mp4"),fourcc, 5.00, (video_width,video_height))

    # print(cap.isOpened())

    print("Beginning Video Analysis")

    while cap.isOpened():
        ret, frame = cap.read()
        original = frame
        try:
            # # detect face box, probability and landmarks
            # boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
            # # draw on frame
            # self._draw(frame, boxes, probs, landmarks)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.blur(gray, (3, 3)) 
            detected_circles = cv2.HoughCircles(gray_blurred,  
                            cv2.HOUGH_GRADIENT, 1, 35, param1 = 50, 
                        param2 = 30, minRadius = 45, maxRadius = 150)
    
            #find the iris and recenter image based on iris
            detected_circles = np.uint16(np.around(detected_circles)) 
        
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2] 
                print(a, b, r)
                # Draw the circumference of the circle. 
                #size = 2*r
                cv2.circle(frame, (a, b), r, (0, 255, 0), 2)
                # Draw a small circle (of radius 1) to show the center. 
                cv2.circle(frame, (a, b), 1, (0, 0, 255), 3) 

        except:
            frame = original

        # Show the frame
        out.write(frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        if (ret == False):
            break

    print("Video Successfully Processed!")
    cap.release()
    out.release()
    cv2.destroyAllWindows()
        