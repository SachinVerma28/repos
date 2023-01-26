import os
import pickle
import cvzone
from firebase_admin import db
from firebase_admin import storage
import face_recognition
import time
import numpy as np
import firebase_admin
from firebase_admin import credentials
import cv2

#cred = credentials.Certificate("serviceAccountKey.json")
#firebase_admin.initialize_app(cred, {
#    'databaseURL':"https://onpythagor-default-rtdb.firebaseio.com"
#})

Ronak = "False"
counts = "0"


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://onpythagor-default-rtdb.firebaseio.com",
    'storageBucket':"onpythagor.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
matches = []
imgBackground = cv2.imread('Resources/background.png')

folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print(len(imgModeList))
#print(imgModeList)

#Load The Encoding File
print("Loading Encode File...")
file = open('EncodeFilesMINE.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
file.close()
encodeListKnown, studentsIds = encodeListKnownWithIds
#print(studentsIds)
print("Encode File Loaded...")
ModeType = 0
counter = 0
id = -1
imgStudents = []
PID = "TESTpid"
counts = "0"





while True:

   # time.sleep(1)
   # cv2.waitKey(1)

    BOL = db.reference(f'Students/BooleanVal')
    BOL.child('conditionWORK').set("Condition Server Running Perfectly...")


    refer = db.reference(f'Students/BooleanVal').get()
    Ronak = str(refer['condition'])
    if Ronak == "True":

        if counts == "0":
            PID = str(refer['PID'])
            counts = "1"
            print(Ronak, counts, PID)



            success, img = cap.read()

            # Getting Required Arguments From Server.
            blob = bucket.get_blob(f'Images/{PID}.jpg')
            arrays = np.frombuffer(blob.download_as_string(), np.uint8)
            arguments = cv2.imdecode(arrays, cv2.COLOR_BGR2RGB)
            # Done Here

            img = arguments
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            faceCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#            imgBackground[162:162 + 480, 55:55 + 640] = img
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[ModeType]

            for encoFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encoFace)
                faceDistance = face_recognition.face_distance(encodeListKnown, encoFace)

                # print("matches", matches)
                # print("faceDistances", faceDistance)
                matchIndex = np.argmin(faceDistance)
                ROM = "False"

                if matches[matchIndex] == False:
                    print("Unknown User")
                    ROM = "True"
                    Bos = db.reference(f'Students/BooleanVal/{PID}')
                    Bos.child('status').set("Face Not Detected.")

                    BOL = db.reference(f'Students/BooleanVal')
                    BOL.child('condition').set("False")
                    BOL.child("PID").set(counts)



                if matches[matchIndex]:
                    print(studentsIds[matchIndex])

                    Bos = db.reference(f'Students/BooleanVal/{PID}')
                    Bos.child('status').set("Face Detected Successfully.")


                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentsIds[matchIndex]
                    if counter == 0:
                        counter = 1
                        ModeType = 1
            if counter != 0:
                if counter == 1:
                    studentsInfo = db.reference(f'Students/{id}').get()
                    # Get The Images From Storage
                    blob = bucket.get_blob(f'Images/{id}.jpg')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudents = cv2.imdecode(array, cv2.COLOR_BGR2RGB)
                    # Update Attendence On Database
                    ref = db.reference(f'Students/{id}')
#                    studentsInfo['total_attendance'] = 5
            #        ref.child('total_attendance').set(studentsInfo['total_attendance'])

                    Bo = db.reference(f'Students/BooleanVal')
                    Bo.child('condition').set("False")
                    Bos = db.reference(f'Students/BooleanVal')
                    Bos.child('status').set("Done SuccessFully")

                    counts = "0"

                    print(studentsInfo)
                    if studentsInfo:
                       Bos = db.reference(f'Students/BooleanVal/{PID}')
                       Bos.child('outputInfo').set(studentsInfo)
                    else:
                        Bos = db.reference(f'Students/BooleanVal/{PID}')
                        Bos.child('outputInfo').set("Please Upload Student Data In Your DataBase First")

"""
nbghj fvnhprint("Running Code")

                cv2.putText(imgBackground, str(studentsInfo['total_attendance']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(studentsInfo['major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentsInfo['standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentsInfo['year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentsInfo['starting_year']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)

                cv2.putText(imgBackground, str(studentsInfo['name']), (808, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                # imgBackground[175:175+216, 909:909+216] = imgStudents

                counter += 1

            cv2.imshow("Face Attendence", imgBackground)
            # cv2.imshow("Web Cam", img)
            cv2.waitKey(1)

"""


