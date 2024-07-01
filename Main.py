# import os
# import pickle
# import numpy as np
# import cv2
# import face_recognition
# import cvzone
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import storage
# import numpy as np
# from datetime import datetime
# import pyttsx3
# # if we use asyncronus function it will show video in real time it will update and download the data base in braket
# def mark_voice(info):
#           engine = pyttsx3.init()
#           engine.setProperty('voice', 'en-us')  # Change the voice to a specific language/accent
#           engine.setProperty('rate', 150)  # Adjust the speaking rate (words per minute)
#           engine.setProperty('volume', 1.0)  # Adjust the volume (0.0 to 1.0)
#           # message = "Your attendance is marked."
#           message = info
#           engine.say(message)
#           engine.runAndWait()

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://faceattendencerealtime-44886-default-rtdb.firebaseio.com/",
#     'storageBucket': "faceattendencerealtime-44886.appspot.com"
# })

# bucket = storage.bucket()

# cap = cv2.VideoCapture(0)   # master 1 instead of 0
# cap.set(3, 640)
# cap.set(4, 480)

# imgBackground = cv2.imread('Resources/background.png')
# # print(imgBackground)

# # Importing the mode images into a list
# folderModePath = 'Resources/Modes'
# modePathList = os.listdir(folderModePath)
# imgModeList = []
# for path in modePathList:
#     imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# # print(len(imgModeList))

# # Load the encoding file
# print("Loading Encode File ...")
# file = open('EncodeFile.p', 'rb')
# encodeListKnownWithIds = pickle.load(file)
# file.close()
# encodeListKnown, studentIds = encodeListKnownWithIds
# # print(studentIds)
# # print("Encode File Loaded")

# modeType = 0
# counter = 0
# id = -1
# imgStudent = []

# while True:
#     success, img = cap.read()
#     # print(success)
#     # print(img)

#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#     imgBackground[162:162 + 480, 55:55 + 640] = img
#     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#     if faceCurFrame:
#         for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#             matches = face_recognition.compare_faces(encodeListKnown, encodeFace,tolerance=.45)
#             faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#             # print("matches", matches)
#             # print("faceDis", faceDis)

#             matchIndex = np.argmin(faceDis)
#             # print("Match Index", matchIndex)

#             if matches[matchIndex]:
#                 # print("Known Face Detected")
#                 # print(studentIds[matchIndex])
#                 y1, x2, y2, x1 = faceLoc
#                 y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4    # we are multiply by 4 bcz we reduce the the size by 4(.25)
#                 bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
#                 imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)   #rectangle thickness rt=0
#                 id = studentIds[matchIndex]
#                 if counter == 0:
#                     cvzone.putTextRect(imgBackground, "Loading", (275, 400))
#                     cv2.imshow("Face Attendance", imgBackground)
#                     cv2.waitKey(1)
#                     counter = 1
#                     modeType = 1

#         if counter != 0:

#             if counter == 1:
#                 # Get the Data
#                 studentInfo = db.reference(f'Students/{id}').get()
#                 print(studentInfo) # here student info print everything my name uid course and all
#                 # Get the Image from the storage
#                 blob = bucket.get_blob(f'Images/{id}.png')
#                 array = np.frombuffer(blob.download_as_string(), np.uint8)
#                 imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
#                 # Update data of attendance
#                 datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
#                                                    "%Y-%m-%d %H:%M:%S")
#                 secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
#                 print(secondsElapsed)
#                 if secondsElapsed > 180: # attendence will we mark for same person after 30 second ... its maybe leacture time and time must be in second
#                     mark_voice(studentInfo['name']+"your attendence marked")
#                     ref = db.reference(f'Students/{id}')
#                     studentInfo['total_attendance'] += 1
#                     ref.child('total_attendance').set(studentInfo['total_attendance'])
#                     ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#                 else:
#                     modeType = 3
#                     mark_voice(studentInfo['name']+"you attendece is already marked")
#                     counter = 0
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#             if modeType != 3:

#                 if 10 < counter < 20:
#                     modeType = 2

#                 imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

#                 if counter <= 10:
#                     cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(id), (1006, 493),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
#                     cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
#                     cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
#                     cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
#                                 cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

#                     (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
#                     offset = (414 - w) // 2
#                     cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
#                                 cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

#                     imgBackground[190:190 + 199, 909:909 + 216] = imgStudent
#                     # imgBackground[162:162 + 216, 55:55 + 199] = imgStudent  # comment se bhail ba

#                 counter += 1
# #here we reset the every thing
#                 if counter >= 20:
#                     counter = 0
#                     modeType = 0
#                     studentInfo = []
#                     imgStudent = []
#                     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
#     else:
#         modeType = 0
#         counter = 0
#     # cv2.imshow("Webcam", img)
#     cv2.imshow("Face Attendance", imgBackground)
#     if cv2.waitKey(1) & 0xFF == ord('s'):ss
#         break

import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
import pyttsx3
import pyautogui
# if we use asyncronus function it will show video in real time it will update and download the data base in braket
def mark_voice(info):
          engine = pyttsx3.init()
          engine.setProperty('voice', 'en-us')  # Change the voice to a specific language/accent
          engine.setProperty('rate', 150)  # Adjust the speaking rate (words per minute)
          engine.setProperty('volume', 1.0)  # Adjust the volume (0.0 to 1.0)
          # message = "Your attendance is marked."
          message = info
          engine.say(message)
          engine.runAndWait()

def take_ss():
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot.png')



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendencerealtime-44886-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendencerealtime-44886.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)   # master 1 instead of 0
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')
# print(imgBackground)

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
# print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []
path_QR=r'C:\Users\kumar\PycharmProjects\Face Recognition with Real-Time Database\Resources\Modes\QR code.jpg'
imgQR= cv2.imread(path_QR)

while True:
    success, img = cap.read()
    # print(success)
    # print(img)

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace,tolerance=.45)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4    # we are multiply by 4 bcz we reduce the the size by 4(.25)
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)   #rectangle thickness rt=0
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1) #wait time for 1 milisecond ; 5000 wait for 5 sec
                    counter = 1
                    modeType = 1
            else:
                # pass
                # y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  
                # bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                # color=(0,0,225) #RbG
                # imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                # mark_voice("Face not matched , Please Scan QR code")
                imgBackground[190:190 + 216, 909:909 + 216] = imgQR # try line 247 coordinates
                cv2.waitKey(200)
        if counter != 0:

            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo) # here student info print everything my name uid course and all
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 180: # attendence will we mark for same person after 30 second ... its maybe leacture time and time must be in second
                    mark_voice(studentInfo['name']+"your attendence marked")
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    mark_voice(studentInfo['name']+"you attendece is already marked")
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[190:190 + 199, 909:909 + 216] = imgStudent
                    # imgBackground[162:162 + 216, 55:55 + 199] = imgStudent  # comment se bhail ba

                counter += 1
#here we reset the every thing
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break