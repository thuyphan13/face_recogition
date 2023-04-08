import cv2
import sqlite3
import os

cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Hàm cập nhật tên và ID vào CSDL
def insertOrUpdate(id, name, age, gender,cr):
    conn=sqlite3.connect("FaceBaseNew.db")
    cursor=conn.execute('SELECT * FROM People WHERE ID='+str(id))
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
        break

    if isRecordExist==1:
        cmd="UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(id)
        cmd="UPDATE people SET Age=' "+str(age)+" ' WHERE ID="+str(id)
        cmd="UPDATE people SET Gender=' "+str(gender)+" ' WHERE ID="+str(id)
        cmd="UPDATE people SET CR=' "+str(cr)+" ' WHERE ID="+str(id)


    else:
        cmd="INSERT INTO people(ID,Name,Age,Gender,CR) Values("+str(id)+",' "+str(name)+" ',' "+str(age)+" ',' "+str(gender)+" ',' "+str(cr)+" ')"

    conn.execute(cmd)
    conn.commit()
    conn.close()
    
id=input('Nhập mã nhân viên:')
name=input('Nhập tên nhân viên:')
age=input('Nhập tuổi:')
gender=input('Nhập giới tính:')
cr=input('Nhập phòng:')


print("Bắt đầu chụp ảnh nhân viên, nhấn q để thoát!")

insertOrUpdate(id,name,age,gender,cr)

sampleNum=0

while(True):

    ret, img = cam.read()

    # Lật ảnh cho đỡ bị ngược
    img = cv2.flip(img,1)

    # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
    centerH = img.shape[0] // 2;
    centerW = img.shape[1] // 2;
    sizeboxW = 300;
    sizeboxH = 400;
    cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)

    # Đưa ảnh về ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật quanh mặt nhận được
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
       
        # Tạo đường dẫn đến thư mục của người đó
        path = os.path.join("dataSet", name)

        # Kiểm tra xem thư mục đã tồn tại hay chưa
        if not os.path.exists(path):
            # Nếu chưa tồn tại thì tạo mới
            os.makedirs(path)

        # Ghi dữ liệu khuôn mặt vào thư mục dataSet
        cv2.imwrite(os.path.join(path, f"{id}.{name}.{sampleNum}.jpg"), gray[y:y + h, x:x + w])
        # cv2.imwrite("dataSet/" + path + id +'.'+ name +'.'+ str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        # cv2.imwrite("dataSet/" + id +'.'+ str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

        sampleNum = sampleNum + 1
    cv2.imshow('frame', img)
    # Check xem có bấm q hoặc trên 80 ảnh sample thì thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif sampleNum > 80:
        break

cam.release()
cv2.destroyAllWindows()