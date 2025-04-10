import cv2
import numpy as np
import os
from datetime import datetime
import os
import shutil
from datetime import datetime
from PIL import Image


def copy_folder_with_timestamp(input_folder):
    """Copy the input folder to a new folder with a timestamped name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_folder = f"Context_{timestamp}"
    shutil.copytree(input_folder, new_folder)
    return new_folder

