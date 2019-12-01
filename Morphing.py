#######################################################
#    Author:      Jiaxing Yang
#    email:       yang1274@purdue.edu
#    ID:          ee364d24
#    Date:        11/24/2019
#######################################################
import numpy as np
from scipy.interpolate import RectBivariateSpline
import imageio
from scipy.spatial import Delaunay
from matplotlib.path import Path
import time
# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################

class Triangle:
    def __init__(self, vertices):
        if type(vertices) != np.ndarray:
            raise ValueError('The entered object has to be a numpy array with dimension 3x2 and with the type float64')
        if vertices.dtype != np.float64:
            raise ValueError('The entered object has to be a numpy array with dimension 3x2 and with the type float64')
        if vertices.shape != (3,2):
            raise ValueError("Input dimension wrong")

        self.vertices = vertices

    def getPoints(self):
        x_arr = np.array([self.vertices[0][0], self.vertices[1][0], self.vertices[2][0]])
        y_arr = np.array([self.vertices[0][1], self.vertices[1][1], self.vertices[2][1]])
        xmin, xmax = int(np.min(x_arr)), int(np.max(x_arr))
        ymin, ymax = int(np.min(y_arr)), int(np.max(y_arr))

        # p = path.Path(np.insert(self.vertices, 3, self.vertices[0], axis=0), closed=True)
        p = Path(self.vertices)
        x, y = np.meshgrid(np.arange(xmin, xmax + 1), np.arange(ymin, ymax + 1))
        points = np.vstack((x.flatten(), y.flatten())).T

        grid = p.contains_points(points, radius=0.5)
        return np.float64(points[grid])

class Morpher:
    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):
        if leftImage.dtype != np.uint8:
            raise TypeError('The left image has to be a np array with uint8')
        for x in leftTriangles:
            if not isinstance(x, Triangle):
                raise TypeError('The list has to contain all the Triangle class')
        if rightImage.dtype != np.uint8:
            raise TypeError('The left image has to be a np array with uint8')
        for y in rightTriangles:
            if not isinstance(y, Triangle):
                raise TypeError('The list has to contain all the Triangle class')
        self.leftImage = leftImage
        self.leftTriangles = leftTriangles
        self.rightImage = rightImage
        self.rightTriangles = rightTriangles

    def getImageAtAlpha(self,alpha):
        if alpha < 0 or alpha >1:
            raise ValueError('The entered alpha value has to be in the range of 0 and 1')
        if alpha == 0:
            return self.leftImage
        if alpha == 1:
            return self.rightImage

        #initialize the states
        lt = self.leftTriangles
        rt = self.rightTriangles
        li = self.leftImage
        ri = self.rightImage
        #https://scipython.com/book/chapter-8-scipy/examples/two-dimensional-interpolation-with-scipyinterpolaterectbivariatespline/
        morph_image = np.zeros_like(li, dtype=np.uint8)
        inplt_li = RectBivariateSpline(x=np.arange(0,li.shape[0]),y=np.arange(0,li.shape[1]), z = li,kx=1, ky = 1)
        inplt_ri = RectBivariateSpline(x=np.arange(0, ri.shape[0]), y=np.arange(0, ri.shape[1]), z= ri, kx=1, ky = 1)

        for x in range(0,len(lt)):
            #first find the vertices of the morphed triangles
            morph_ver = (1 - alpha) * lt[x].vertices + alpha * rt[x].vertices
            morph_tri = Triangle(morph_ver)

            #find the original points P P = [x, y, 1]
            P = morph_tri.getPoints()
            P_asint = P.astype(int).T
            P_w1 = (np.asmatrix((np.insert(P,2,1,axis = 1)))).T

            #find the transformation matrix H
            H_left = getTransform(lt[x].vertices, morph_tri.vertices)
            H_right = getTransform(rt[x].vertices,morph_tri.vertices)

            #the individual component from each part of image
            morph_left = np.matmul(H_left, P_w1)
            morph_right = np.matmul(H_right, P_w1)



            morph_image[P_asint[1],P_asint[0]] = (1-alpha)*inplt_li.ev(morph_left[1],morph_left[0]) + alpha *inplt_ri.ev(morph_right[1],morph_right[0])

        return morph_image.astype(np.uint8)

def getTransform(initial, final):
    #this is the fastest way to generate the matrix corresponding
    A_matrix = [[initial[0][0], initial[0][1], 1, 0, 0, 0],[0, 0, 0, initial[0][0], initial[0][1], 1],[initial[1][0], initial[1][1], 1, 0, 0, 0],[0, 0, 0, initial[1][0], initial[1][1], 1],[initial[2][0], initial[2][1], 1, 0, 0, 0],[0, 0, 0, initial[2][0], initial[2][1], 1]]
    mat_mid = [[final[0][0]], [final[0][1]], [final[1][0]], [final[1][1]], [final[2][0]], [final[2][1]]]
    transform = np.linalg.solve(np.array(A_matrix), np.array(mat_mid))
    hfunc = np.reshape(transform,(2,3))
    hfunc = np.concatenate((hfunc,[[0,0,1]]),axis=0)
    #find the inverse transform function
    h_inv = np.linalg.inv(hfunc)

    return h_inv



def loadTriangles(leftPointFilePath, rightPointFilePath):

    leftlist = np.loadtxt(leftPointFilePath,dtype=np.float64)
    rightlist = np.loadtxt(rightPointFilePath, dtype=np.float64)

    tri = Delaunay(np.array(leftlist)).simplices
    lt=[]
    rt=[]
    for i in tri:
        lt.append(Triangle(leftlist[i]))
        rt.append(Triangle(rightlist[i]))
    return(lt, rt)



class ColorMorpher(Morpher):
    def __init__(self,li,lt,ri,rt):
        Morpher.__init__(self,li,lt,ri,rt)


    def getImageAtAlpha(self,alpha):
        if alpha < 0 or alpha >1:
            raise ValueError('The entered alpha value has to be in the range of 0 and 1')
        if alpha == 0:
            return self.leftImage
        if alpha == 1:
            return self.rightImage

        #initialize the states
        lt = self.leftTriangles
        rt = self.rightTriangles
        li = self.leftImage
        ri = self.rightImage
        #https://scipython.com/book/chapter-8-scipy/examples/two-dimensional-interpolation-with-scipyinterpolaterectbivariatespline/
        morph_image = np.zeros_like(li, dtype=np.uint8)

        #have to do r g b separetely, since now, the image data is a tuple contains rgb
        #r
        inplt_li_r = RectBivariateSpline(x=np.arange(0,li.shape[0]),y=np.arange(0,li.shape[1]), z = li[:,:,0],kx=1, ky = 1)
        inplt_ri_r = RectBivariateSpline(x=np.arange(0, ri.shape[0]), y=np.arange(0, ri.shape[1]), z= ri[:,:,0], kx=1, ky = 1)

        #g
        inplt_li_g = RectBivariateSpline(x=np.arange(0, li.shape[0]), y=np.arange(0, li.shape[1]), z=li[:, :, 1], kx=1,
                                         ky=1)
        inplt_ri_g = RectBivariateSpline(x=np.arange(0, ri.shape[0]), y=np.arange(0, ri.shape[1]), z=ri[:, :, 1], kx=1,
                                         ky=1)


        #b
        inplt_li_b = RectBivariateSpline(x=np.arange(0, li.shape[0]), y=np.arange(0, li.shape[1]), z=li[:, :, 2], kx=1,
                                         ky=1)
        inplt_ri_b = RectBivariateSpline(x=np.arange(0, ri.shape[0]), y=np.arange(0, ri.shape[1]), z=ri[:, :, 2], kx=1,
                                         ky=1)




        for x in range(0,len(lt)):
            #first find the vertices of the morphed triangles
            morph_ver = (1 - alpha) * lt[x].vertices + alpha * rt[x].vertices
            morph_tri = Triangle(morph_ver)

            #find the original points P P = [x, y, 1]
            P = morph_tri.getPoints()
            P_asint = P.astype(int).T
            P_w1 = (np.asmatrix((np.insert(P,2,1,axis = 1)))).T

            #find the transformation matrix H
            H_left = getTransform(lt[x].vertices, morph_tri.vertices)
            H_right = getTransform(rt[x].vertices,morph_tri.vertices)

            #the individual component from each part of image
            morph_left = np.matmul(H_left, P_w1)
            morph_right = np.matmul(H_right, P_w1)



            morph_image[P_asint[1],P_asint[0],0] = (1-alpha)*inplt_li_r.ev(morph_left[1],morph_left[0]) + alpha *inplt_ri_r.ev(morph_right[1],morph_right[0])
            morph_image[P_asint[1], P_asint[0], 1] = (1 - alpha) * inplt_li_g.ev(morph_left[1],morph_left[0]) + alpha * inplt_ri_g.ev(morph_right[1], morph_right[0])
            morph_image[P_asint[1], P_asint[0], 2] = (1 - alpha) * inplt_li_b.ev(morph_left[1],morph_left[0]) + alpha * inplt_ri_b.ev(morph_right[1], morph_right[0])
        return morph_image.astype(np.uint8)



    def saveVideo(self,targetFilePath, frameCount, frameRate, includeReversed = True):
        file = imageio.get_writer("/home/ecegridfs/a/ee364d24/tmp/"+targetFilePath,fps=frameRate)
        if not includeReversed:
            file.append_data(self.getImageAtAlpha(0))
            for x in range(frameCount,1,-1):
                alpha = 1 / x
                file.append_data(self.getImageAtAlpha(alpha))

            file.close()
            return
        else:
            frames = list()
            file.append_data(self.getImageAtAlpha(0))
            for x in range(frameCount,1,-1):
                alpha = 1 / x
                file.append_data(self.getImageAtAlpha(alpha))
                frames.append(self.getImageAtAlpha(alpha))

            for y in reversed(frames):
                file.append_data(y)

            file.close()





if __name__ == '__main__':
    alpha = 0.5
    (leftTri, rightTri) = loadTriangles('me2.jpg.txt', 'haotian.jpg.txt')
    leftImg = imageio.imread('haotian.jpg')
    rightImg = imageio.imread('me2.jpg')
    morph = ColorMorpher(leftImg, leftTri, rightImg, rightTri)
    morph.saveVideo('video_color.mp4', 10, 5)

