import cv2
import numpy as np
from tkinter.filedialog import *
import cv2
import numpy as np
import cv2
from IPython.display import Image, display
import numpy as np


def get_filtered_image(image, action):
    if action == 'NO_FILTER':
        filtered = image
    elif action == 'CARTOON STYLE1':
        line_size=7
        blur_value=7

        edges=edge_mask(image, line_size,blur_value)


        total_color=15
        img=color_quantization(image, total_color)
        filtered=img
        
    elif action == 'CARTOON STYLE2':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)


        color = cv2.bilateralFilter(image, 9, 300, 300)


        filtered = cv2.bitwise_and(color, color, mask=edges)

    elif action == 'CARTOON STYLE3':
        
        img_rgb =image 
        numDownSamples = 2     # number of downscaling steps 
        numBilateralFilters = 50 # number of bilateral filtering steps 
  
        # -- STEP 1 -- 
  
        # downsample image using Gaussian pyramid 
        img_color = img_rgb 
        for _ in range(numDownSamples): 
            img_color = cv2.pyrDown(img_color) 
  
        
        for _ in range(numBilateralFilters): 
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7) 
  
        
        for _ in range(numDownSamples): 
            img_color = cv2.pyrUp(img_color) 
      
  
        # -- STEPS 2 and 3 -- 
        # convert to grayscale and apply median blur 
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY) 
        img_blur = cv2.medianBlur(img_gray, 3) 
        #cv2.imshow("grayscale+median blur",img_color) 
        #cv2.waitKey(0) 
  
        # -- STEP 4 -- 
        # detect and enhance edges 
        img_edge = cv2.adaptiveThreshold(img_blur, 255, 
                                        cv2.ADAPTIVE_THRESH_MEAN_C, 
                                        cv2.THRESH_BINARY, 9, 9) 
        #cv2.imshow("edge",img_edge) 
        #cv2.waitKey(0) 
  
        # -- STEP 5 -- 
        # convert back to color so that it can be bit-ANDed with color image 
        (x,y,z) = img_color.shape 
        img_edge = cv2.resize(img_edge,(y,x)) 
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB) 
        
        filtered=cv2.bitwise_and(img_color, img_edge)

    elif action == 'CARTOON STYLE4':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)


        color = cv2.bilateralFilter(image, 9, 300, 300)


        filtered = cv2.bitwise_and(color, color, mask=edges)    
        blurred=cv2.bilateralFilter(image, d=7, sigmaColor=200, sigmaSpace=200,)



        cartoon=cv2.bitwise_and(blurred, blurred, mask=edges)
        filtered=cartoon
           


    
    return filtered       


def read_file(filename):
  img=cv2.imread(filename)
 
  cv2.waitKey(0)
  return img

def color_quantization(img, k):

  data=np.float32(img).reshape((-1, 3))

  criteria=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,20,0.001)

  ret, label, center=cv2.kmeans(data, k , None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
  center=np.uint8(center)
  result= center[label.flatten()]
  result=result.reshape(img.shape)

  return result

def edge_mask(img, line_size, blur_value):
  gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray_blur=cv2.medianBlur(gray, blur_value)
  edges=cv2.adaptiveThreshold(gray_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, line_size, blur_value)
  return edges    

