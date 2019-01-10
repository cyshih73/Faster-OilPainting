import cv2
import numpy as np
from scipy import ndimage

def prewitt(img):
    img_gaussian = cv2.GaussianBlur(img,(3,3),0)
    kernelx = np.array( [[1, 1, 1],[0, 0, 0],[-1, -1, -1]] )
    kernely = np.array( [[-1, 0, 1],[-1, 0, 1],[-1, 0, 1]] )
    img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
    img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
    return img_prewittx // 15.36, img_prewitty // 15.36

def roberts(img):
    roberts_cross_v = np.array( [[ 0, 0, 0 ],
                                 [ 0, 1, 0 ],
                                 [ 0, 0,-1 ]] )
    roberts_cross_h = np.array( [[ 0, 0, 0 ],
                                 [ 0, 0, 1 ],
                                 [ 0,-1, 0 ]] )
    vertical = ndimage.convolve( img, roberts_cross_v )
    horizontal = ndimage.convolve( img, roberts_cross_h )
    return vertical // 50.0, horizontal // 50.0

# Different Edge Operator 
def get_gradient(img_o, ksize, gtype):
    if gtype == 'scharr':
        X = cv2.Scharr(img_o, cv2.CV_32F, 1, 0) / 50.0
        Y = cv2.Scharr(img_o, cv2.CV_32F, 0, 1) / 50.0
    elif gtype == 'prewitt':
        X, Y = prewitt(img_o)
    elif gtype == 'sobel':
        X = cv2.Sobel(img_o,cv2.CV_32F,1,0,ksize=5)  / 50.0
        Y = cv2.Sobel(img_o,cv2.CV_32F,0,1,ksize=5)  / 50.0
    elif gtype == 'roberts':
        X, Y = roberts(img_o)
    else:
        print('Not suppported type!')
        exit()

    # Blur the Gradient to smooth the edge
    X = cv2.GaussianBlur(X, ksize, 0)
    Y = cv2.GaussianBlur(Y, ksize, 0)
    return X, Y