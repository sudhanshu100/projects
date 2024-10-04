import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone # type: ignore

# Set up webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
imgBackground = cv2.imread("D:\\my codes\\python codes\\Automated Attendance System\\resources\\background\\background.png")

#importing the mode images into a list
folderModePath = "D:\\my codes\\python codes\\Automated Attendance System\\resources\\modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))


#Load the Encoading File
print("Loading encoding File.....")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("encoding File Loaded.....")


# Main loop to capture frames
while True:
    success, img = cap.read()
    
    # Resize and convert frame for face recognition
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    
    # Detect faces and get encodings in the current frame
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
    # Place webcam feed and mode image onto the background
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 807:807 + 414] = imgModeList[3]
    
    # Match detected faces with known encodings
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDist", faceDist)
        
        matchIndex = np.argmin(faceDist)
        
        if matches[matchIndex]:
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
            
        
        
    # Show the resulting image
    cv2.imshow("face Attendance", imgBackground)
    
    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break
    
# Release the webcam and close windows
# cap.release()
# cv2.destroyAllWindows()