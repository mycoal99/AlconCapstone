import numpy as np
import cv2

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
var = input("Enter right(r) or left(l) eye: ")
while(var != 'r' and var != 'l'):
    var = lower(var)
    if(var == "right"):
        var = 'r'
    elif(var == "left"):
        var = 'l'
    else:
        var = input("Enter right(r) or left(l) eye: ")

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier()
# face_cascade.load('../haarcascade_frontalface_default.xml')

#https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_eye.xml
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


print("cascade", cv2.__version__)

cap = cv2.VideoCapture(0)
ret, img = cap.read()
height, width, channels = img.shape
videoWriter = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('X','V','I','D'), 10, (width,height))
# img = cv2.imread("")
try:
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        resized_cropped = np.asarray([])

        scale=10

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # cv2.rectangle(img,(x,y),(x+int(w/2),y+int(h/2)), (0,0,255),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            print("eyes:\n", eyes)

            if(len(eyes) > 1):
                index = 0
                if(eyes[0][0] < eyes[1][0]):
                    right = 0
                else:
                    right = 1

                for (ex,ey,ew,eh) in eyes:
                    print("ex:",ex, "ey:",ey,"ew:",ew,"eh",eh)
                    if ex <= x and ey <= y and ew <= w and eh <= h:

                        if(index == right and var == 'r'):
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,255),2)
                            print(ex, ew, ey, eh, "LENGTH")
                            cropped = img[y +ey: y + ey + eh, x + ex: x + ex + ew]
                            print("CROPED:", cropped.shape)
                        if (index != right and var == 'l'):
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,255,0),2)
                            print(ex, ew, ey, eh, "LENGTH")
                            cropped = img[y +ey: y + ey + eh, x + ex: x + ex + ew]
                            print("CROPED:", cropped.shape)
                        
                        try:
                            resized_cropped = cv2.resize(cropped, (width, height))
                            print("RESIZED:", resized_cropped.shape)
                        except:
                            pass

                    index += 1

        if not all(resized_cropped.shape):
            resized_cropped = img
        cv2.imshow('img',resized_cropped)
        # videoWriter.write(resized_cropped)

        

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    

    cap.release()
    videoWriter.release()
    cv2.destroyAllWindows()
except OSError:
    print(OSError)