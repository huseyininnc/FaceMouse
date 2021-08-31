from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys, os, cv2
import numpy as np
import pyautogui as auto

auto.FAILSAFE = False
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class Uygulama(QWidget):
    def __init__(self):
        super().__init__()
        self.pencere1()
        self.setWindowTitle('FACE MOUSE')
        
    def pencere1(self):
        self.form = QFormLayout()

        self.pb = QPushButton("Kalibrasyonu ayarla")
        self.pb1 = QPushButton("Başlat")

        self.lb = QLabel("Yüz hassasiyeti")
        self.lb1 = QLabel("Mouse hassasiyeti")
        self.lb2 = QLabel("")

        self.le = QLineEdit()
        self.le1 = QLineEdit()

        self.form.addRow(self.lb, self.le)
        self.form.addRow(self.lb1, self.le1)
        self.form.addRow(self.pb, self.pb1)
        self.form.addRow(self.lb2)

        self.pb.clicked.connect(self.kalibrasyon)
        self.pb1.clicked.connect(self.baslat)

        self.setLayout(self.form)
        self.show()
    
    def kalibrasyon(self):
        try:
            video = cv2.VideoCapture(0)
            ret, frame = video.read()

            cv2.resizeWindow('FACE MOUSE', 500,500)
            cv2.line(frame,(500,250),(0,250),(0,255,0),1)
            cv2.line(frame,(250,0),(250,500),(0,255,0),1)
            cv2.circle(frame, (250, 250), 5, (255, 255, 255), -1)
            cv2.rectangle(frame,(280,250),(370,330),(0,0,255),5)

            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3)

            for (x,y,w,h) in faces:
                self.yuz_konumX = x
                self.yuz_konumY = y
                self.lb2.setText(f"Kalibrasyon şuna göre ayarlandı; X: {str(self.yuz_konumX)}  Y: {str(self.yuz_konumY)}")
                print(f"({x}, {y})")
                print(len(faces))

            video.release()
            cv2.destroyAllWindows()

        except:
            self.lb2.setText("Beklenmedik bir hata oluştu!")

    def baslat(self):
        video = cv2.VideoCapture(0)

        while True:
            ret, frame = video.read()

            cv2.resizeWindow('FACE MOUSE', 500,500)
            cv2.line(frame,(500,250),(0,250),(0,255,0),1)
            cv2.line(frame,(250,0),(250,500),(0,255,0),1)
            cv2.circle(frame, (250, 250), 5, (255, 255, 255), -1)

            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),5)

                if x > self.yuz_konumX + int(self.le.text()):
                    auto.moveRel(-int(self.le1.text()),0)

                if x < self.yuz_konumX - int(self.le.text()):
                    auto.moveRel(+int(self.le1.text()),0)

                if y > self.yuz_konumY + int(self.le.text()):
                    auto.moveRel(0,+int(self.le1.text()))

                if y < self.yuz_konumY - int(self.le.text()):
                    auto.moveRel(0,-int(self.le1.text()))

            cv2.imshow('FACE MOUSE',frame)
            k = cv2.waitKey(30) & 0xff

            if k == 27:
                break

        video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    uygulama = Uygulama()
    sys.exit(app.exec())
