import os
import cv2
import pickle
import cvzone
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import face_recognition
import pickle
import os
from datetime import datetime as dt
# import datetime as dt

cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-26581-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-26581.appspot.com"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
titlepath = 'Resources/Modes'
modepath = os.listdir((titlepath))
titleList = []
for path in modepath:
    titleList.append(cv2.imread(os.path.join(titlepath,path)))

imgbackground = cv2.imread('Resources/background.png')

# load the  encoding file
print("Loading encoded file....")
file = open("EncoderFile.p","rb")
encodeListKnownids = pickle.load(file)
file.close()
encodeListKnown, student_id = encodeListKnownids
# print(student_id)
print("Encoded file loaded")

counter = 0
modeType = 0
imgstudent = []
while True:
    success, img  = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facecurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facecurFrame)

    imgbackground[162:162+480, 55:55+640] = img
    imgbackground[44:44+633 , 808:808+414] = titleList[modeType]
    # imgbackground[162:162 + 480, 55:55 + 640] = titleList[1]


    if facecurFrame:
        for encoFace , faceloc in zip(encodeCurFrame,facecurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encoFace)
            facedis = face_recognition.face_distance(encodeListKnown,encoFace)
            # print("matches" , matches)
            # print("facedis" , facedis)

            matIndex = np.argmin(facedis)
            # print("matchIndex" , matIndex)
            if(matches[matIndex] == True):
                # print("Face Detected" , student_id[matIndex])
                y1,x2,y2,x1 = faceloc
                y1,x2,y2,x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55+x1,162+y1, x2-x1,y2-y1
                imgbackground = cvzone.cornerRect(imgbackground,bbox, rt = 0)

                id = student_id[matIndex]
                if counter == 0:
                    cvzone.putTextRect(imgbackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgbackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType=1

            if counter!=0:
                if counter==1:
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(studentInfo)
                    blob = bucket.get_blob(f'Images/{id}.jpg')
                    array = np.frombuffer(blob.download_as_string(),np.uint8)
                    imgstudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                    #
                    datetimeObject = dt.strptime(studentInfo['last_attendance_time'],
                                                "%Y-%m-%d %H:%M:%S")

                    seconds_elapsed = (dt.now() - datetimeObject).total_seconds()

                    if(seconds_elapsed>30):
                        ref = db.reference(f'Students/{id}')
                        studentInfo['Total_attendance'] += 1
                        ref.child('Total_attendance').set(studentInfo['Total_attendance'])
                        ref.child('last_attendance_time').set(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        modeType=3
                        counter=0
                        imgbackground[44:44 + 633, 808:808 + 414] = titleList[modeType]

                if modeType!=3:
                    if 10<counter<20:
                        modeType=2
                    imgbackground[44:44 + 633, 808:808 + 414] = titleList[modeType]

                    if(counter<=10):
                        cv2.putText(imgbackground,str(studentInfo['Total_attendance']), (861,125),
                                    cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

                        cv2.putText(imgbackground, str(studentInfo['Major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(studentInfo['Starting Year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                        # cv2.putText(imgbackground, str(studentInfo['Year']), (1025, 625),
                        #             cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 100), 1)
                        # to align name in centre

                        (w,h),_ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX,1,1)
                        offset = (414-w)//2
                        cv2.putText(imgbackground, str(studentInfo['name']), (808+offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        height , width = imgstudent.shape[:2]

                        imgstudent = cv2.resize(imgstudent,(216,216))
                        height, width = imgstudent.shape[:2]
                        # print(height)
                        # print(width)
                        imgbackground[175:175+height,909:909+width] = imgstudent

                counter+=1

                if counter>=20:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    imgstudent=[]
                    imgbackground[44:44 + 633, 808:808 + 414] = titleList[modeType]
    else:
            modeType=0
            counter=0

    cv2.imshow("Face Attendance", imgbackground)
    # cv2.imshow("webcam",img)
    cv2.waitKey(1)