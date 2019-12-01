# Import PyQt5 classes
import sys
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Lab12.MorphingGUI import *
from Lab12.Morphing import *
from PIL import ImageTk, Image, ImageQt
import imageio
import numpy as np
import time
class Morphapp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        #init state
        self.loadleft = False
        self.loadright = False
        super(Morphapp,self).__init__()
        self.setupUi(self)
        self.disable()
        #add points on logic
        self.num_left = 0
        self.num_right = 0
        self.checknum = 0
        self.numsaved = 0
        self.store = False
        self.newleft = list()
        self.newright = list()
        self.leftflag = False
        self.new = False
        self.templeft = False
        self.tempright = False

        #btn functions
        self.Loadstartbtn.clicked.connect(self.load1)
        self.Loadendbtn.clicked.connect(self.load2)
        self.tempstar = QtWidgets.QGraphicsScene()
        self.tempend = QtWidgets.QGraphicsScene()
        self.boxsize = QtWidgets.QGraphicsView()
        #alpha value
        self.Linebar.setMaximum(100)
        self.Linebar.setMinimum(0)
        self.Linebar.setSingleStep(5)
        self.Linebar.valueChanged.connect(self.setalpha)

        self.qp = QPainter()
        self.Startimage.mousePressEvent = self.start_click
        self.Endimage.mousePressEvent = self.end_click
        #display triangles
        self.Triangleshow.toggled.connect(self.sanjiaoxing)

        #blend
        self.alphaval = 0
        self.blendscene = QtWidgets.QGraphicsScene()
        self.Blendbtn.clicked.connect(self.getblend)
        self.blendlist = list()

    #backspace
    def sanjiaoxing(self):
        if self.Triangleshow.isChecked() == True:
            (self.lt,self.rt) = loadTriangles((self.startpath+".txt"),(self.endpath+".txt"))
            for x in self.lt:
                vt_1 = QPointF(x.vertices[0][0]/4,x.vertices[0][1]/4)
                vt_2 = QPointF(x.vertices[1][0] / 4, x.vertices[1][1] / 4)
                vt_3 = QPointF(x.vertices[2][0] / 4, x.vertices[2][1] / 4)
                self.tempstar.addPolygon(QPolygonF([vt_1,vt_2,vt_3]),QPen(Qt.black,1,cap=Qt.RoundCap))
            for y in self.rt:
                vt_1 = QPointF(y.vertices[0][0] / 4, y.vertices[0][1] / 4)
                vt_2 = QPointF(y.vertices[1][0] / 4, y.vertices[1][1] / 4)
                vt_3 = QPointF(y.vertices[2][0] / 4, y.vertices[2][1] / 4)
                self.tempend.addPolygon(QPolygonF([vt_1,vt_2, vt_3]), QPen(Qt.black, 1, cap=Qt.RoundCap))
        else:

            for a in self.tempstar.items():
                print(type(a))
                if isinstance(a,QGraphicsPolygonItem):
                    self.tempstar.removeItem(a)
            for b in self.tempend.items():
                if isinstance(b,QGraphicsPolygonItem):
                    self.tempend.removeItem(b)


    def keyPressEvent(self,event):
        if (event.key()) == Qt.Key_Backspace:
            if self.tempstar != QtWidgets.QGraphicsScene() and self.tempend != QtWidgets.QGraphicsScene():
                if self.tempright and self.templeft:
                    self.tempend.removeItem(self.rightitem)
                    self.tempright = False
                    del self.newright[-1]
                    print(len(self.newright))

                elif self.templeft and not self.tempright:
                    self.tempstar.removeItem(self.leftitem)
                    self.templeft = False
                    self.leftflag = False
                    self.new = False
                    del self.newleft[-1]




    def mousePressEvent(self,event):
        self.numsaved = min(len(self.newleft),len(self.newright))
        if len(self.newleft) != len(self.newright) :
            return
        elif self.tempstar != QtWidgets.QGraphicsScene() and self.tempend != QtWidgets.QGraphicsScene():
            self.huablue()
            self.save()

    def start_click(self,event):

        if self.tempstar != QtWidgets.QGraphicsScene() and self.tempend != QtWidgets.QGraphicsScene():
            if (len(self.newleft) == len(self.newright)) and len(self.newleft) != 0 and self.new != False:
                self.huablue()
                self.new = False
            elif not self.leftflag:
                self.leftgreen = event.localPos()
                left = self.leftgreen
                self.tempstar.addEllipse(left.x(), left.y(), 3, 3, QPen(Qt.green))
                self.leftitem = self.tempstar.items()[0]
                self.newleft.append((left.x(),left.y()))
                self.leftflag=True
                self.templeft = True

    def huablue(self):
        if len(self.newleft) != 0:
            self.tempstar.addEllipse(self.newleft[-1][0],self.newleft[-1][1],3,3,QPen(Qt.blue))
            self.tempend.addEllipse(self.newright[-1][0], self.newright[-1][1], 3, 3, QPen(Qt.blue))
            self.leftflag = False
            self.save()
            self.new = False

    def end_click(self,event):

        if self.tempstar != QtWidgets.QGraphicsScene() and self.tempend != QtWidgets.QGraphicsScene():
            if len(self.newright) == len(self.newleft) and self.new != False:
                self.huablue()
                self.new = False
            if self.leftflag:
                self.rightgreen = event.localPos()
                x = self.rightgreen

                self.tempend.addEllipse(x.x(), x.y(), 3, 3, QPen(Qt.green))
                self.rightitem = self.tempend.items()[0]
                self.newright.append((x.x(),x.y()))
                self.leftflag = False
                self.new = True
                self.tempright = True



    def load1(self):
        #self.Startimage.clear()
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open image file ...', filter="image files (*.jpg *.gif *.png)")
        if not filePath:
            return
        self.morphstart = imageio.imread(filePath)
        self.tempstar.clear()
        self.startpath = filePath
        re_scaled = self.loadscene(filePath)
        self.Startimage.resize(re_scaled.size())
        self.tempstar.addPixmap(re_scaled)
        self.Startimage.setScene(self.tempstar)
        self.Startimage.fitInView(self.tempstar.sceneRect(), Qt.KeepAspectRatio)
        self.loadleft = True
        if self.loadright and self.loadleft:
            self.points()
            for x in self.leftpos:
                self.tempstar.addEllipse(x[0],x[1],3,3,QPen(Qt.red))

    def save(self):
        if self.tempstar != QtWidgets.QGraphicsScene() and self.tempend != QtWidgets.QGraphicsScene() and len(self.newleft) > 0 and len(self.newright) >0:
            left_file = open((self.startpath + ".txt"),"a")
            right_file = open((self.endpath + ".txt"),"a")
            left = self.newleft[-1]
            right = self.newright[-1]
            x_left = left[0] *4
            y_left = left[1]*4
            x_right = right[0]*4
            y_right = right[1] *4

            left_file.write('\n   %.1f   %.1f\n'%(x_left,y_left))
            right_file.write('\n   %.1f   %.1f\n'%(x_right,y_right))

            left_file.close()
            right_file.close()

    def points(self):
        right_path = self.endpath+".txt"
        left_path = self.startpath+".txt"
        self.leftpos = list()
        self.rightpos = list()
        if os.path.exists(self.startpath + ".txt") and os.path.exists(right_path):
            lpoint = np.loadtxt(left_path,np.float64)
            rpoint = np.loadtxt(right_path,np.float64)
            for a,b in zip(lpoint,rpoint):
                self.leftpos.append((a[0]/4, a[1]/4))
                self.rightpos.append((b[0]/4,b[1]/4))


    def load2(self):
        #self.Endimage.clear()
        filePath, _ = QFileDialog.getOpenFileName(self, caption='Open image file ...', filter="image files (*.jpg *.gif *.png)")
        if not filePath:
            return

        self.morphend = imageio.imread(filePath)
        self.tempend.clear()
        self.endpath = filePath
        re_scaled = self.loadscene(filePath)
        self.Endimage.resize(re_scaled.size())
        self.tempend.addPixmap(re_scaled)
        self.Endimage.setScene(self.tempend)
        self.Endimage.fitInView(self.tempend.sceneRect(),Qt.KeepAspectRatio)
        self.loadright = True
        if self.loadright and self.loadleft:
            self.points()
            for x in self.rightpos:
                self.tempend.addEllipse(x[0], x[1], 3, 3, QPen(Qt.red))
            for y in self.leftpos:
                self.tempstar.addEllipse(y[0],y[1], 3, 3,QPen(Qt.red))
            self.enable()
        else:
            self.disable()

    def loadscene(self,filePath):
        # establish the temp image to be loaded
        self.boxsize.resize(360, 270)
        img1 = Image.open(filePath)
        img2 = ImageQt.ImageQt(img1)
        pixels = QtGui.QPixmap.fromImage(img2)
        size = self.boxsize.size()
        
        re_scaled = pixels.scaled(self.boxsize.size(),  QtCore.Qt.KeepAspectRatio)
        return re_scaled

    def enable(self):
        self.Triangleshow.setEnabled(True)
        self.Blendbtn.setEnabled(True)
        self.Linebar.setEnabled(True)
        self.Alphacof.setEnabled(True)
    def disable(self):
        self.Triangleshow.setEnabled(False)
        self.Blendbtn.setEnabled(False)
        self.Linebar.setEnabled(False)
        self.Alphacof.setEnabled(False)
    def setalpha(self, alpha_cof):
        alpha_cof = self.Linebar.value() / 100.0
        self.alphaval = alpha_cof
        self.Alphacof.setText(str(round(alpha_cof,2)))
        index = int(alpha_cof/0.05)
        blend = self.blendlist[index]
        self.blendscene.clear()
        self.blendscene.addPixmap(blend)
        self.Morphimage.resize(blend.size())
        self.Morphimage.setScene(self.blendscene)

        self.Morphimage.fitInView(self.blendscene.sceneRect(), Qt.KeepAspectRatio)


    def getblend(self):
        time1 = time.time()
        (self.lt, self.rt) = loadTriangles2((self.startpath + ".txt"), (self.endpath + ".txt"),4)
        a = 0
        img1 = Image.open(self.startpath)
        img2 = Image.open(self.endpath)
        print(self.tempstar.width())
        img1.thumbnail((360,270))
        img1 = np.array(img1)
        img2.thumbnail((360,270))
        img2 = np.array(img2)
        morph = Morpher(img1, self.lt, img2, self.rt)
        img3 = morph.getImageAtAlpha(a)
        img4 = QImage(img3, img3.shape[1], img3.shape[0], QImage.Format_Grayscale8)
        img5 = QPixmap.fromImage(img4).scaled(self.Morphimage.size(), Qt.KeepAspectRatio)
        self.blendlist.append(img5)
        self.blendscene.clear()
        self.blendscene.addPixmap(img5)
        self.Morphimage.resize(img5.size())
        self.Morphimage.setScene(self.blendscene)
        self.Morphimage.fitInView(self.blendscene.sceneRect(), Qt.KeepAspectRatio)
        for x in range(0,21):
            a += 0.05
            img3 = morph.getImageAtAlpha(a)
            img4 = QImage(img3, img3.shape[1], img3.shape[0], QImage.Format_Grayscale8)
            img5 = QPixmap.fromImage(img4).scaled(self.Morphimage.size(), Qt.KeepAspectRatio)
            self.blendlist.append(img5)
        time2 = time.time()
        print(time2-time1)

def loadTriangles2(leftPointFilePath, rightPointFilePath,ratio):

    leftlist = np.loadtxt(leftPointFilePath,dtype=np.float64) / ratio
    rightlist = np.loadtxt(rightPointFilePath, dtype=np.float64) / ratio

    tri = Delaunay(np.array(leftlist)).simplices
    lt=[]
    rt=[]
    for i in tri:
        lt.append(Triangle(leftlist[i]))
        rt.append(Triangle(rightlist[i]))
    return(lt,rt)
if __name__ == "__main__":
    currentApp = QApplication(sys.argv)
    currentForm = Morphapp()

    currentForm.show()
    currentApp.exec_()
    time2 = time.time()