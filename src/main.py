from pathlib import Path
from tqdm import tqdm
from split_multi_scanned_photos import split_multi_scanned_photos


path_scans = Path(r"D:\Photos\\original_scans\original_scans_batch_1")

path_output = path_scans / "output"

list_path_tiffs = list(path_scans.glob("*.tif"))

for path_im in tqdm(list_path_tiffs[:]):
    split_multi_scanned_photos(path_im, 
                               path_output=path_output, 
                               debug=False)

