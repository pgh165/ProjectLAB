from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2 as cv
import speech_recognition as sr
from gtts import gTTS 
import os 
import time 
import playsound 

# speak 함수 정의
def speak(text):
    tts = gTTS(lang='ko', text=text ) #ko')
    filename='voice.mp3' 
    tts.save(filename) 
    playsound.playsound(filename) 

#teachable machine으로 훈련된 인공신경망 모델 로드
model = load_model('C:/Users/Home/Desktop/Coding/prolab_embedded-main/embedded/keras_model.h5')

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

size = (224, 224)
#연결된 카메라 
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    image1 = cv.resize(frame, size, interpolation=cv.INTER_AREA)
    image_array = np.asarray(image1)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
       
    prediction = model.predict(data)
    print(prediction)
    
    #np.argmax()를 사용하여 정확도가 높은 레이블 추출
    if(np.argmax(prediction[0]) == 0): speak("지호입니다.") #0번 레이블이 검출되면 tts로 "지호입니다." 출력
    else: speak("배경입니다.") #1번 레이블이 검출되면 "배경입니다." 출력
    
    cv.imshow('frame', image1)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()