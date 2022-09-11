from pathlib import Path
import tifffile

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
import numpy as np

from skimage.measure import regionprops
from skimage.transform import rotate
from skimage.filters import threshold_otsu
from skimage.morphology import label

import pandas as pd

from skimage.filters import gaussian, difference_of_gaussians

from hampel import hampel
from tqdm import tqdm

#%%

def split_multi_scanned_photos(path_im: Path, 
                                      path_output : Path=None,
                                      region_threshold : int=1e6,
                                      pad : int=25,
                                      deskew : bool=True,
                                      debug : bool=False):
    """
    splits a flatbed scan into multiple images

    Parameters
    ----------
    path_im : Path
        path to image on hdd.
    path_output : Path, optional
        path to where you want images to be save to, otherwise an output 
        directory will be created at the root of the files. The default is None.
    region_threshold : int, optional
        regions of interest smaller than these size will be ignored . The default is 1e6.
    pad : int, optional
        Pads the bounding box to prevent accidental cropping of photos edge. The default is 50.
    deskew : bool, optional
        Deskew photo on the fly. The default is True.
    debug : bool, optional
        Show intermedaite images for debugging. The default is False.

    Returns
    -------
    None
        function doesn't return anything.

    """
    
    # load image and get shape
    print(f"processing: {path_im.name}")
    im = tifffile.imread(path_im)
    max_rows, max_cols, _ = im.shape
    
    # normalize image for display, and otherwise multiplications will clip at 2^16
    def _normalize(im):
        return (im - im.min()) / (im.max() - im.min())
    
    im_norm = _normalize(im)
    if debug:
        plt.imshow(im_norm)
        plt.show()
    
    # create grayscale intensity
    im_intensity = im_norm[...,0] * im_norm[...,1] * im_norm[...,2]
    if debug:
        plt.imshow(im_intensity)
        plt.show()
        
    # im_intensity = gaussian(im_intensity, (2,10))
    # plt.imshow(im_intensity2)
    # plt.show()
        
    # create binary based on otsu, bg vs fg
    im_intensity_exp = im_intensity**2
    # plt.imshow((im_intensity_exp) > threshold_otsu((im_intensity_exp)))
    
    mask_binary = im_intensity_exp > threshold_otsu(im_intensity_exp)
    # mask_binary = im_intensity > threshold_otsu(im_intensity)
    if debug:
        plt.imshow(mask_binary)
        plt.show()
    
    # invert mask to keep photo regions 
    mask_inverted = np.invert(mask_binary)
    if debug:
        plt.imshow(mask_inverted)
        plt.show()
    
    # get labels or regions
    labels = label(mask_inverted)
    props = regionprops(labels, im_norm)
    
    # keept only regions with potential photos
    list_rois = [] # keep rois larger than threshold
    for region in props:
        if region.area > region_threshold:
            list_rois.append(region)
    
    # Iterate through each roi with a photo
    for idx, r in enumerate(list_rois):
        pass
        minr, minc, maxr, maxc= r.bbox
        im_rgb = im_norm[max(minr-pad,0):min(maxr+pad,max_rows), max(minc-pad,0):min(maxc+pad,max_cols),:]
        im_orig = im[max(minr-pad,0):min(maxr+pad,max_rows), max(minc-pad,0):min(maxc+pad,max_cols),:]
    
        
        if deskew:
            
            # find bottom edge to fit a line to
            mask_image = r.image
            
            # determine col indices with values by projecting
            values_col = mask_image.sum(axis=1)
            values_col = np.argwhere(values_col)
            
            # pick 1/4 of points in the middle to avoid outlier at edges
            quarter = len(values_col) // 4
            middle = len(values_col)//2
           
            values_col = values_col[middle-quarter:middle+quarter]
            
            
            # determine max idx of values in each col
            val_rows =[]
            for idx_col in values_col:
                pass
                col_indexes = np.argwhere(mask_image[:,idx_col])
                val_rows.append(np.max(col_indexes))
                
            # hampel filter to reduce outliers in y
            val_rows = hampel(pd.Series(val_rows),
                              window_size=100,
                              n=1,
                              imputation=True)
            
            # fit 1d line
            fit_line = np.polyfit(values_col.squeeze(), val_rows, deg=1)
            
            if debug:
                plt.scatter(values_col, val_rows, s=1)
            
            # visualize linear fit
            x = np.linspace(0,mask_image.shape[1],mask_image.shape[1])
            y = fit_line[0]*x + fit_line[1]
            if debug:
                plt.plot(x,y)
            angle = np.rad2deg(np.arctan(fit_line[0]))

            # angle_in_degrees = r.orientation * (180/np.pi) + 90 
            im_orig = rotate(im_orig,
                            angle=angle, 
                            cval=np.min(r.image), # to make white or as close to white
                            preserve_range=True)
            if debug:
                plt.title("image without rotation")
                plt.imshow(im_rgb)
                plt.show()
                
                plt.title("image rotated")
                plt.imshow(rotate(im_rgb, 
                                  angle=angle, 
                                  cval=np.max(im_rgb)))
                plt.show()
    
            
        if not debug and not path_output:
            path_output = path_im.parent / 'output'
            path_output.mkdir(exist_ok=True)
            
        # finally save image
        if not debug:
            tifffile.imwrite( path_output / f"{path_im.stem}_{idx}.tiff", im_orig.astype(np.uint16))
#%%
if __name__ == "__main__":
    
    #%%
    # test images
    # list_path_tiffs = [
    #     Path(r"19871213-152.tif"),
    #     Path(r"19871213-156.tif")
    #     ]
    
    path_images = Path(r"./test_images")
    list_path_images = list(path_images.glob("*.tif"))
    
    
    for path_im in tqdm(list_path_images[:]):
        pass
        split_multi_scanned_photos(path_im, deskew=True, debug=True)


