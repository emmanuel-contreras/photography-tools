from pathlib import Path
import tifffile

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
import numpy as np

from skimage.measure import regionprops
from skimage.feature import canny 
from skimage.morphology import square, erosion, dilation, label, binary_closing
from skimage.filters import median
from skimage.segmentation import clear_border
from skimage.transform import rotate

import tifffile

from scipy.ndimage import binary_fill_holes

from cell_analysis_tools.image_processing import kmeans_threshold
from cell_analysis_tools.image_processing import normalize

import cv2
#%%
path_im = Path(r"19871213-152.tif")
# path_im = Path(r"19871213-156.tif")
im = tifffile.imread(path_im)

# normalize image, otherwise multiplications will clip at 2^16
im_norm = normalize(im)
plt.imshow(im_norm)
plt.show()

# intensity
im_intensity = im_norm[...,0] * im_norm[...,1] * im_norm[...,2]

im_dia = dilation(im_intensity, square(5))
plt.imshow(im_dia)

mask = im_dia > np.percentile(im_dia, 80)
plt.imshow(mask)

mask_inverted = np.invert(mask)
plt.imshow(mask_inverted)

# clear border
mask_cb = clear_border(mask_inverted)
plt.imshow(mask_cb)

# binary closing 
mask_closed = binary_closing(mask_cb, square(30))
plt.imshow(mask_closed)
plt.show()

labels = label(mask_closed)

props = regionprops(labels, im_norm)


list_rois = []
large_area = 10000 # abritrary large number
for region in props:
    
    if region.area > large_area:
        list_rois.append(region)

# Visualize individual images
pad = 50

#deskew
for r in list_rois:
    row_min, col_min, row_max, col_max = r.bbox
    im_rgb = im_norm[row_min-pad:row_max+pad, col_min-pad:col_max+pad,:]
    plt.imshow(rotate(im_rgb, angle=r.orientation, cval=1))
    plt.show()


# save image as tiff again







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






