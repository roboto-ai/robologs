import glob
import io
import os
import subprocess

import cv2
import numpy as np
from PIL import Image


def convert_compressed_depth_to_cv2(compressed_depth):
    """
    Convert a compressedDepth topic image into a cv2 image.
    compressed_depth must be from a topic /bla/compressedDepth
    as it's encoded in PNG
    Code from: https://answers.ros.org/question/249775/display-compresseddepth-image-python-cv2/
    """
    depth_fmt, compr_type = compressed_depth.format.split(";")
    # remove white space
    depth_fmt = depth_fmt.strip()
    compr_type = compr_type.strip().replace(" png", "")
    if compr_type != "compressedDepth":
        raise Exception("Compression type is not 'compressedDepth'." "You probably subscribed to the wrong topic.")

    depth_header_size = 12
    raw_data = compressed_depth.data[depth_header_size:]

    depth_img_raw = cv2.imdecode(np.frombuffer(raw_data, np.uint8), 0)

    if depth_img_raw is None:
        # probably wrong header size
        raise Exception("Could not decode compressed depth image." "You may need to change 'depth_header_size'!")
    result = cv2.normalize(depth_img_raw, depth_img_raw, 0, 255, norm_type=cv2.NORM_MINMAX)

    im_color = cv2.applyColorMap(depth_img_raw, cv2.COLORMAP_JET)

    return im_color


def convert_image_to_cv2(msg):
    """
    Args:
        msg ():

    Returns:

    """
    np_arr = np.fromstring(msg.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
    return image_np


def create_video_from_images(input_path, output_path, output_name="video.mp4", frame_rate=12, resize=None):
    """
    Args:
        input_path ():
        output_path ():
        output_name ():
        frame_rate ():
        resize ():

    Returns:

    """
    img_array = []
    output_video_path = os.path.join(output_path, output_name)
    output_video_path_temp = os.path.join(output_path, "temp.mp4")

    for filename in sorted(glob.glob(os.path.join(input_path, "./*.jpg"))):
        img = cv2.imread(filename)
        if resize:
            img = cv2.resize(img, (0, 0), fx=resize, fy=resize, interpolation=cv2.INTER_LANCZOS4)

        if len(img.shape) == 3:
            height, width, _ = img.shape
        else:
            height, width = img.shape

        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter(output_video_path_temp, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    subprocess.call(["ffmpeg", "-i", output_video_path_temp, "-vcodec", "libx264", "-y", output_video_path])
    os.remove(output_video_path_temp)
    return
