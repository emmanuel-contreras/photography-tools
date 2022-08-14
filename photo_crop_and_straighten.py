from pathlib import Path
import tifffile

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
import numpy as np

from skimage.measure import regionprops
from skimage.feature import canny 

from cell_analysis_tools.image_processing import kmeans_threshold

import cv2
#%%
path_im = Path(r"D:\Pictures\grid\19941213-084_casa abue toya 1993.tif")

path_im = Path(r"D:\Pictures\19901213-142.tif")
im = tifffile.imread(path_im)


# create binary mask
im_summed = im.sum(axis=2)

# add white padding to 
pad_size 
im_sum_padding = np.pad(im_summed,())
# compute regionprops(major axis)
# determine angle from horizontal
# rotate from center to 

# top_hat filter

plt.imshow(canny(im_summed))
plt.show()

plt.imshow(im_summed)
plt.show()



#%%
# Importing OpenCV 
import cv2
from skimage.morphology import square
from skimage.filters import median
  
# Getting the kernel to be used in Top-Hat
filterSize =(500, 500)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
                                   filterSize)
  
# Reading the image named 'input.jpg'
# input_image = cv2.imread("testing.jpg")
input_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# create binary mask
im_summed = im.sum(axis=2)
sq = square(10)
im_med = median(im_summed,sq)
im_border =  im_med > np.percentile(im_med,45)
plt.imshow(im_border)


im_median = cv2.medianBlur(input_image, 3)
plt.imshow(im_median)

# Applying the Top-Hat operation
tophat_img = cv2.morphologyEx(input_image, 
                              cv2.MORPH_TOPHAT,
                              kernel)

plt.imshow(tophat_img)
# cv2.imshow("original", input_image)
# cv2.imshow("tophat", tophat_img)
# cv2.waitKey(5000)






