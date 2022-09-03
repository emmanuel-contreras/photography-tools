from pathlib import Path
from tqdm import tqdm

path_scans = Path(r"D:\Photos\original_scans")

path_output = path_scans / "output"

from split_multi_scanned_photos import split_multi_scanned_photos


list_path_tiffs = list(path_scans.glob("*.tif"))

for path_im in tqdm(list_path_tiffs[:]):
    split_multi_scanned_photos(path_im, path_output=path_output)

