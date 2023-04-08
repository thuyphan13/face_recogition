import cv2,os
import numpy as np
import image
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
name = "TrainModel"


def getImagesAndLabels(path):
    # Lấy tất cả các file trong thư mục
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    # create empth face list
    faceSamples=[]
    # create empty ID list
    Ids=[]
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        if imagePath.endswith(".jpg"):
            # Lấy ID từ tên file ảnh (tên file có định dạng "{id}.{name}.{sampleNum}.jpg")
            Id = int(os.path.basename(imagePath).split(".")[0])
            # loading the image and converting it to gray scale
            pilImage=Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp=np.array(pilImage,'uint8')
            # getting the face from the training image sample
            faces=detector.detectMultiScale(imageNp)
            # If a face is there then append that in the list as well as Id of it
            for (x,y,w,h) in faces:
                faceSamples.append(imageNp[y:y+h,x:x+w])
                Ids.append(Id)
    return faceSamples,Ids

# Lấy các khuôn mặt và ID từ thư mục dataSet
dataSetPath = os.path.join("dataSet", name)
faceSamples, Ids = getImagesAndLabels(dataSetPath)

# Train model để trích xuất đặc trưng các khuôn mặt và gán với từng nhân viên
recognizer.train(faceSamples, np.array(Ids))

# Lưu model
recognizer.save('recognizer/trainner.yml')

print("Trained!")
