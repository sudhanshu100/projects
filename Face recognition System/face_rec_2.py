import cv2
import numpy as np
import pickle
import face_recognition
import os
from simple_facerec import SimpleFacerec

#Encode faces from a folder>>>>
sfr = SimpleFacerec()
sfr.load_encoding_images("D://my codes//python codes//Face Recognition System//faces")

#load camera>>>>
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

#Load the encoding file
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)

while True:
    success, img = cap.read()
    
    #detect faces>>>>
    face_locations, face_names = sfr.detect_known_faces(img)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        
        cv2.putText(img, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 200, 0), 4)
    
    cv2.imshow("press q to quit", img )
    
    if cv2.waitKey(1) == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    