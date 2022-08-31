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

from skimage.filters import try_all_threshold, threshold_local, threshold_otsu

from tqdm import tqdm
import tifffile
from scipy.ndimage import binary_fill_holes

import cv2
#%%
# path_im = Path(r"19871213-152.tif")
# path_im = Path(r"19871213-156.tif")

debug = False
path_dir = Path(r"D:\Photos\test_batch")
list_path_tiffs = list(path_dir.glob("*.tif"))
for path_im in tqdm(list_path_tiffs[:]):
    pass
    print(f"processing: {path_im.name}")
    im = tifffile.imread(path_im)
    max_rows, max_cols, _ = im.shape
    
    # normalize image, otherwise multiplications will clip at 2^16
    im_norm = normalize(im)
    if debug:
        plt.imshow(im_norm)
        plt.show()
    
    # create grayscale image intensity
    im_intensity = im_norm[...,0] * im_norm[...,1] * im_norm[...,2]
    if debug:
        plt.imshow(im_intensity)
        plt.show()
    
    mask_binary = im_intensity > threshold_otsu(im_intensity)
    if debug:
        plt.imshow(mask_binary)
        plt.show()
    
    # invert mask 
    mask_inverted = np.invert(mask_binary)
    if debug:
        plt.imshow(mask_inverted)
        plt.show()
    
    labels = label(mask_inverted)
    props = regionprops(labels, im_norm)
    
    
    list_rois = []
    list_areas=[]
    large_area = 1e6 # abritrary large number to grab large areas
    for region in props:
        list_areas.append(region.area)
        if region.area > large_area:
            list_rois.append(region)
    
    # Visualize individual images
    pad = 50
    
    #deskew
    
    for idx, r in enumerate(list_rois):
        pass
        # plt.imshow(r.image)
        # plt.show()
        minr, minc, maxr, maxc= r.bbox
        im_rgb = im_norm[max(minr-pad,0):min(maxr+pad,max_rows), max(minc-pad,0):min(maxc+pad,max_cols),:]
        im_orig = im[max(minr-pad,0):min(maxr+pad,max_rows), max(minc-pad,0):min(maxc+pad,max_cols),:]
    
        if debug:
            # find better way to get the angle?
            plt.title("image without rotation")
            plt.imshow(im_rgb)
            plt.show()
            
            plt.title("image rotated")
            plt.imshow(rotate(im_rgb, angle=r.orientation, cval=1))
            plt.show()
        
        # save image as tiff again
        im_orig_rotated = rotate(im_orig, 
                                 angle=r.orientation, 
                                 cval=1,
                                 preserve_range=True)
        tifffile.imwrite(path_im.parent / 'output' / f"{path_im.stem}_{idx}.tiff", im_orig)









#%%
# # Importing OpenCV 
# import cv2
# from skimage.morphology import square
# from skimage.filters import median
  
# # Getting the kernel to be used in Top-Hat
# filterSize =(500, 500)
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, 
#                                    filterSize)
  
# # Reading the image named 'input.jpg'
# # input_image = cv2.imread("testing.jpg")
# input_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# # create binary mask
# im_summed = im.sum(axis=2)
# sq = square(10)
# im_med = median(im_summed,sq)
# im_border =  im_med > np.percentile(im_med,45)
# plt.imshow(im_border)


# im_median = cv2.medianBlur(input_image, 3)
# plt.imshow(im_median)

# # Applying the Top-Hat operation
# tophat_img = cv2.morphologyEx(input_image, 
#                               cv2.MORPH_TOPHAT,
#                               kernel)

# plt.imshow(tophat_img)
# # cv2.imshow("original", input_image)
# # cv2.imshow("tophat", tophat_img)
# # cv2.waitKey(5000)






