import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier()
# face_cascade.load('../haarcascade_frontalface_default.xml')

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


print("cascade", cv2.__version__)

cap = cv2.VideoCapture(0)

try:
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        resized_cropped = np.asarray([])
        height, width, channels = img.shape
        scale=10

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.rectangle(img,(x,y),(x+int(w/2),y+int(h/2)), (0,0,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            #prepare the crop
            
            # centerX,centerY = int((x+w)/2),int((y+h)/2)
            # centerX,centerY = int(x + w / 2),int(y + h / 2)
            # radiusX,radiusY = int(scale*height/100),int(scale*width/100)

            # minX,maxX = centerX-radiusX,centerX+radiusX
            # minY,maxY = centerY-radiusY,centerY+radiusY

            # print("MIN MAX", minX, maxX, minY, maxY)
        
            # cropped = img[minX:maxX, minY:maxY]
            # print(x, w, y, h, "LENGTH")



            # # =========== for face
            # cropped = img[y:y+h, x:x+w]
            # print("CROPED:", cropped.shape)
            # try:
            #     resized_cropped = cv2.resize(cropped, (width, height))
            #     print("RESIZED:", resized_cropped.shape)
            # except:
            #     pass


            # print(eyes)

            for (ex,ey,ew,eh) in eyes:
                if ex <= x and ey <= y and ew <= w and eh <= h:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

                    print(ex, ew, ey, eh, "LENGTH")


                    cropped = img[y +ey: y + ey + eh, x + ex: x + ex + ew]
                    print("CROPED:", cropped.shape)
                    
                    try:
                        resized_cropped = cv2.resize(cropped, (width, height))
                        print("RESIZED:", resized_cropped.shape)
                    except:
                        pass

        

        #get the webcam size
        
        print("SHAPE:", resized_cropped.shape)

        

        

        # cv2.imshow('my webcam', resized_cropped)
        
        if not all(resized_cropped.shape):
            resized_cropped = img
        # else:
        #     if resized_cropped.any():
        #         resized_cropped = img
            
        print("AFTER:", resized_cropped.shape)
        #if resized_cropped:
        cv2.imshow('img',resized_cropped)
        # else:
        #     cv2.imshow('img',img)


        # if cv2.waitKey(1) == 27: 
        #     break  # esc to quit

        # #add + or - 5 % to zoom

        # if cv2.waitKey(30) == ord('a'): 
        #     scale += 5  # +5

        # if cv2.waitKey(30) == ord('s'): 
        #     scale -= 5  # +5


        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
except OSError:
    print(OSError)