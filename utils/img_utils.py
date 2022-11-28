import cv2
import os
import glob


def create_thumbnails(input_folder: str, output_folder: str, resize: float = 1.0, max_size: int = 1000, file_extension=".png"):
    """
    This function creates thumbnails from images in a folder
    Args:
        input_folder: input folder with imgs
        output_folder: output folder where thumbnails are saved
        resize: percentage to which the image will re resized
        max_size: only resize images which are bigger than max_size

    Returns:

    """
    for filename in sorted(glob.glob(os.path.join(input_folder, f"./*{file_extension}"))):
        img = cv2.imread(filename)
        height, width, _ = img.shape
        if width > max_size:
            img = cv2.resize(img, (0, 0), fx=resize, fy=resize, interpolation=cv2.INTER_AREA)
        _, image_name = os.path.split(filename)
        output_path = os.path.join(output_folder, image_name)
        print(output_path)
        cv2.imwrite(output_path, img)
    return
