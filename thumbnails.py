from skimage.transform import resize
from pathlib import Path
import tifffile
import numpy as np

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams["figure.dpi"] = 300
#%% MAKE THUMBNAILS 
path_output_thumbnails = Path(r"thumbnails")


path_images = Path("output")

list_path_images = list(path_images.glob("*.tif?"))


for path_image in list_path_images:
    pass
    im = tifffile.imread(path_image)
    plt.imshow(im/im.max())
    plt.show()
    
    scale_factor = 10
    im_scaled = resize(im, 
                       (im.shape[0]//scale_factor,im.shape[1]//scale_factor ),
                       anti_aliasing=(True))
    
    plt.imshow(im_scaled/im_scaled.max())
    plt.show()
    
    tifffile.imwrite(path_output_thumbnails / f"{path_image.stem}_thumbnail.tiff", 
                     (im_scaled * 255).astype(np.uint8))
    

#%% GIVEN THUMBNAILS COPY IMAGES OVER TO OTHER FOLDER