import cv2
import face_recognition
import pickle
import os

folder_path = 'Images'
imagepathList = os.listdir(folder_path)
imgList = []
student_id = []
for path in imagepathList:
    imgList.append(cv2.imread(os.path.join(folder_path,path)))
    # student_id.append(os.path.splitext(path)[0])
    student_id.append(path[0:8])
# print(student_id)
# for i in imgList:
#     cv2.imshow('i',i)
#     cv2.waitKey(0)



def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList
print("encoding started....")
encodeListKnown = findEncodings(imgList)
encodeListKnownids = [encodeListKnown,student_id]
# print(encodeListKnown)
print("encoding complete")

print("file dumping start....")
file = open("EncoderFile.p","wb")
pickle.dump(encodeListKnownids,file)
file.close()
print("file dumped")

