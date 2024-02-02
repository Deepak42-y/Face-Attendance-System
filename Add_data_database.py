import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import cv2
import face_recognition
import pickle
import os

cred = credentials.Certificate("service_account_key.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-26581-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-26581.appspot.com"
})
ref = db.reference('Students')
data= {
    "21115046":
        {
            "name": "Deepak Yadav",
            "Major": "Data Science",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21115062":
        {
            "name": "Itesh Mujalde",
            "Major": "Electrical",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 8
        },
    "21115076":
        {
            "name": "Kshitij Mesharam",
            "Major": "Consultant",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21115083":
        {
            "name": "Manmath",
            "Major": "Electrical",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21115156":
        {
            "name": "Sahil",
            "Major": "Developer",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21116009":
        {
            "name": "Ajay Sonwani",
            "Major": "Coder",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21116096":
        {
            "name": "Tapan Karangiya",
            "Major": "Coder + Developer",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21117110":
        {
            "name": "Pratik Snap",
            "Major": "Developer",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
    "21116087":
        {
            "name": "Shikhardeep",
            "Major": "data analyst & coder",
            "Starting Year": "2021",
            "last_attendance_time": "2024-01-31  14:54:11",
            "Total_attendance" : 7
        },
}
for key, value in data.items():
    ref.child(key).set(value)

folder_path = 'Images'
imagepathList = os.listdir(folder_path)
imgList = []
student_id = []
for path in imagepathList:
    imgList.append(cv2.imread(os.path.join(folder_path,path)))
    # student_id.append(os.path.splitext(path)[0])
    student_id.append(path[0:8])
    fileName = f'{folder_path}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)




print("Data Imported")
