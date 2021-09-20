
#######################
#### https://blog.csdn.net/songzitea/article/details/40832565
#### https://www.docin.com/p-1446417455.html
##################
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication,QLabel,QLineEdit)
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtGui import (QImage)
import cv2
import numpy as np
from PyQt5.QtCore import QTimer
import acopy
import bcopy

def getRect():
  Mn = np.array([[0,2],[3,1]])
  for i in range(3):
    U = np.ones(Mn.shape)
    Mn1 = np.vstack((np.hstack((4*Mn,4*Mn+2*U)), np.hstack((4*Mn+3*U,4*Mn+U))))
    Mn = Mn1
  return Mn


def Bayer(rect):
  Mn = getRect()
  n = int(rect.shape[0] / Mn.shape[0] + 1)
  m = int(rect.shape[1] / Mn.shape[1] + 1)
  for i in range(rect.shape[0]):
    for j in range(rect.shape[1]):
      if(rect[i][j] < Mn[i % Mn.shape[0]][j % Mn.shape[1]]):
        rect[i][j] = 0
      else:
        rect[i][j] = 255
  return rect


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.isPress = False
        self.fileName = ''
        self.lable = None
        self.lable2 = None
        self.timer = None
        self.state = 0
        self.setAcceptDrops(True)
        self.initUI()
    #按钮事件

    def origin(self):
      self.lable2.setVisible(False)
      self.readPic(self.fileName)
    #抖动法半色调
    def dou(self):
      img = cv2.imread(self.fileName,0)
      shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      rect = Bayer(img)
      ITemp = cv2.imread(self.fileName,0)
      for i in range(ITemp.shape[0]):
        for j in range(ITemp.shape[1]):
          ITemp[i][j] = rect[i][j]
      
      self.lable.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      shrink = cv2.cvtColor(ITemp, cv2.COLOR_BGR2RGB)
      self.lable2.setVisible(True)
      self.lable2.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      self.timer.start(1)


    #半色调
    def href(self):
      img = cv2.imread(self.fileName,0)

      # cv2.imshow('origin',img)
      img_arr = np.array(img)
      img_arr = np.vstack((img_arr, np.zeros((1,img_arr.shape[1]))))
      img_arr = np.hstack((img_arr, np.zeros((img_arr.shape[0],1))))
      img_arr = np.hstack( (np.zeros((img_arr.shape[0],1)),img_arr))
      I = np.zeros((img_arr.shape[0],img_arr.shape[1]))
      img_arr = img_arr / 255
      a=7/16
      b=3/16
      c=5/16
      d=1/16
      for i in range(img_arr.shape[0]-1):
        for j in range(1,img_arr.shape[1]-1):
          if img_arr[i][j] < 1/2:
            I[i][j] = 0
          else:
            I[i][j] = 1
          error = img_arr[i][j] - I[i][j]
          img_arr[i][j+1] = img_arr[i][j+1] + error*a
          img_arr[i+1][j-1] = img_arr[i+1][j-1] + error*b
          img_arr[i+1][j] = img_arr[i+1][j] + error*c
          img_arr[i+1][j+1] = img_arr[i+1][j+1] + error*d
      
      ITemp = cv2.imread(self.fileName,0)
      # ITemp = I[:-1,1:-1]
      for i in range(ITemp.shape[0]):
        for j in range(ITemp.shape[1]):
          ITemp[i][j] = I[i][j+1]*255

      shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.lable.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      shrink = cv2.cvtColor(ITemp, cv2.COLOR_BGR2RGB)
      self.lable2.setVisible(True)
      self.lable2.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      self.timer.start(1)
      pass

    #边缘检测抠图
    def edge(self):
      img = cv2.imread(self.fileName,1)
      shrink = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
      self.lable.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      shrink = cv2.cvtColor(acopy.FindEdge(self.fileName), cv2.COLOR_BGR2RGB)
      self.lable2.setVisible(True)
      self.lable2.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      self.timer.start(1)
    def myMousePressEvent(self, event):
      self.isPress = True
      x = event.x()
      y = event.y()
      print(x,y)

    def myMouseMoveEvent(self, event):
      if(self.isPress and self.state == 1):
        x = event.x()
        y = event.y()
        recImg = bcopy.FindColor(self.fileName, (x,y))
        shrink = cv2.cvtColor(recImg, cv2.COLOR_BGR2RGB)
        self.lable.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
        self.timer.start(1)
        # print(x,y)
        
    def myMouseReleaseEvent(self, event):
      self.isPress = False
      x = event.x()
      y = event.y()
      recImg = bcopy.FindColor(self.fileName, (x,y),False)
      shrink = cv2.cvtColor(recImg, cv2.COLOR_BGR2RGB)
      self.lable.setPixmap(QPixmap.fromImage(QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)))
      self.timer.start(1)
    # 颜色抠图
    def colorCor(self):
      self.readPic(self.fileName)
      bcopy.initiate(self.fileName)
      self.state = 1
      print('color')


    # 读取图片
    def readPic(self,picName):
      self.fileName = picName
      shrink = cv2.cvtColor(cv2.imread(picName), cv2.COLOR_BGR2RGB)
      img = QImage(shrink.data,shrink.shape[1],shrink.shape[0],shrink.shape[1] * 3,QImage.Format_RGB888)
      self.lable2.setVisible(False)
      self.lable.setPixmap(QPixmap.fromImage(img))
      self.timer.start(1)
      
        
    def initUI(self):
      self.timer = QTimer()
      self.timer.timeout.connect(self.time)
      #初始化按钮
      originButton = QPushButton("原图")
      douButton = QPushButton("抖动法半值化")
      halfButton = QPushButton("误差扩散半值化")
      edgeButton = QPushButton("边缘检测抠图")
      colorButton = QPushButton("颜色抠图")
      #按钮事件
      douButton.clicked.connect(self.dou)
      originButton.clicked.connect(self.origin)
      halfButton.clicked.connect(self.href)
      edgeButton.clicked.connect(self.edge)
      colorButton.clicked.connect(self.colorCor)

      # 初始化图片标签
      lb1 = QLabel(self)
      self.lable = lb1
      lb2 = QLabel(self)
      lb2.setVisible(False)
      self.lable2 = lb2
      # self.readPic('123.jpg')
      self.setMouseTracking(True)

      #图片事件
      lb1.mousePressEvent = self.myMousePressEvent
      lb1.mouseMoveEvent = self.myMouseMoveEvent
      lb1.mouseReleaseEvent = self.myMouseReleaseEvent
      #按钮布局
      vbox = QVBoxLayout()
      vbox.addWidget(originButton)
      vbox.addWidget(douButton)
      vbox.addWidget(halfButton)
      vbox.addWidget(edgeButton)
      vbox.addWidget(colorButton)
      vbox.addStretch(1)
      #图片布局
      vbox1 = QVBoxLayout()
      vbox1.addWidget(lb1)
      vbox1.addWidget(lb2)
      vbox1.addStretch(0)
      #整体布局
      hbox = QHBoxLayout()
      hbox.addLayout(vbox1)
      hbox.addStretch(0)
      hbox.addLayout(vbox)
      #启用布局
      self.setLayout(hbox)    
      #设置窗口信息
      self.setGeometry(300, 300, 300, 150)
      self.setWindowTitle('仿ps抠图')
      self.show()
    def time(self):
      self.resize(self.minimumSize())
      self.timer.stop()

    def dragEnterEvent(self,e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()
    def dropEvent(self,e):
        print(e.mimeData().text())
        self.readPic(e.mimeData().text()[8:])
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    getRect()
    ex = Example()
    sys.exit(app.exec_())