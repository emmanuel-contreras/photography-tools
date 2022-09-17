from skimage.transform import resize
from pathlib import Path
import tifffile
import numpy as np

import matplotlib.pylab as plt
import matplotlib as mpl
mpl.rcParams["figure.dpi"] = 300
#%% MAKE THUMBNAILS 


def create_thumbnail(path_image : Path, 
                     path_output : Path):
        """
        Parameters
        ----------
        path_image : Path
            path to the image to create a thumbnail for.
        path_output : Path
            Path to save the thumbnail to.
        
        Returns
        -------
        None.
        
        """
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

if __name__ == "__main__":

    path_images = Path("./test_images/output")
    path_output_thumbnails = Path(r"./test_images/thumbnails")

    list_path_images = list(path_images.glob("*.tif?"))
    
    for path_image in list_path_images:
        pass
        
        if not path_output_thumbnails.exists():
            path_output_thumbnails.mkdir(exist_ok=True)
        
        create_thumbnail(path_image,
                         path_output_thumbnails)
    
    
    
    