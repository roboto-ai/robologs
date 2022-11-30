"""Rosbag utilities

This module contains functions to extract data from rosbags.

"""
import rospy
import yaml
import os
import glob
from rosbag.bag import Bag
from typing import Optional
import cv2
import numpy as np
import logging
from cv_bridge import CvBridge
from tqdm import tqdm

import utils.file_utils
import utils.img_utils


def get_bag_info_from_file(rosbag_path: str) -> dict:
    """
    Args:
        rosbag_path (str): Input file path rosbag.

    Returns:
        dict: Dictionary with rosbag metadata.

    """

    if not os.path.exists(rosbag_path):
        raise Exception(f"{rosbag_path} does not exist.")

    if not rosbag_path.endswith('.bag'):
        raise Exception(f"{rosbag_path} is not a rosbag.")

    return yaml.load(Bag(os.path.abspath(rosbag_path), 'r')._get_yaml_info(), Loader=yaml.FullLoader)


def get_bag_info_from_file_or_folder(input_path: str) -> dict:
    """
    Args:
        input_path (str): Input file path of a rosbag, or folder with multiple rosbags.

    Returns:
        dict: Dictionary with rosbag metadata for each rosbag. The key of the dictionary is the rosbag file path.

    """

    rosbag_info_dict = dict()

    if input_path.endswith('.bag'):
        rosbag_info_dict[os.path.abspath(input_path)] = get_bag_info_from_file(input_path)
    else:
        for filename in sorted(glob.glob(os.path.join(input_path, './*.bag'))):
            rosbag_info_dict[os.path.abspath(filename)] = get_bag_info_from_file(filename)

    return rosbag_info_dict


def create_manifest_entry_dict(msg_timestamp: int, rosbag_timestamp: int, file_path: str, index: int) -> dict:
    """
    Args:
        msg_timestamp (int):
        rosbag_timestamp (int):
        file_path (str):
        index (int):

    Returns: dict

    """
    return {"msg_timestamp": msg_timestamp, "rosbag_timestamp": rosbag_timestamp, "path": file_path, "msg_index": index}


def get_image_topic_types():
    """
    Returns:

    """
    return ["sensor_msgs/CompressedImage", "sensor_msgs/Image"]


def get_topic_names_of_type(all_topics: list, filter_topic_types: list) -> list:
    """
    Args:
        all_topics (list):
        filter_topic_types (list):

    Returns:

    """
    return [x["topic"] for x in all_topics if x["type"] in filter_topic_types]


def rosbag_function_callback(rosbag_path: str, function, topics=None, **args) -> None:
    """
    Args:
        rosbag_path ():
        function ():
        topics ():
        **args ():

    Returns:

    """
    bag = Bag(rosbag_path, "r")

    if not topics:
        for topic, msg, t in bag.read_messages():
            function(topic, msg, t, args)
    else:
        for topic, msg, t in bag.read_messages(topics=topics):
            function(topic, msg, t, args)
    return


def get_image_name_from_timestamp(timestamp: int, file_format: str = "jpg") -> str:
    """
    Args:
        timestamp (int):
        file_format (str):

    Returns:

    """
    img_name = f"{str(timestamp)}.{file_format}"
    return img_name


def get_image_name_from_index(index: int, file_format: str = "jpg", zero_padding: int = 6) -> str:
    """
    Args:
        index ():
        file_format ():
        zero_padding ():

    Returns:

    """
    img_name = f"{str(index).zfill(zero_padding)}.{file_format}"
    return img_name


def replace_ros_topic_name(topic_name: str, replace_character: str = "_") -> str:
    """
    Args:
        topic_name ():
        replace_character ():

    Returns:

    """
    return topic_name.replace("/", replace_character)[1:]


def get_filter_fraction(start_time: Optional[float], end_time: Optional[float], start_rosbag: float, end_rosbag: float):
    """
    Args:
        start_time (float or None):
        end_time (float or None):
        start_rosbag (float):
        end_rosbag (float):

    Returns:

    """
    rosbag_duration = end_rosbag - start_rosbag

    if rosbag_duration <= 0:
        return

    if start_time and end_time:
        return float((end_time.to_sec()-start_time.to_sec()) / rosbag_duration)

    if start_time and not end_time:
        return float((end_rosbag - start_time.to_sec()) / rosbag_duration)

    if end_time and not start_time:
        return float((end_time.to_sec() - start_rosbag) / rosbag_duration)

    if not end_time and not start_time:
        return 1


def get_images_from_bag(rosbag_path: str,
                        output_folder: str,
                        file_format: str = "jpg",
                        topics: Optional[list] = None,
                        create_manifest: bool = False,
                        naming: str = "sequential",
                        resize: Optional[list] = None,
                        sample: Optional[int] = None,
                        start_time: Optional[rospy.Time] = None,
                        end_time: Optional[rospy.Time] = None):
    """
    Args:
        rosbag_path (str):
        output_folder (str):
        file_format (str):
        topics (list):
        create_manifest (bool):
        naming (str):
        resize (list):
        sample (int):
        start_time (rospy.Time):
        end_time (rospy.Time):

    Returns: None

    """

    rosbag_metadata = get_bag_info_from_file(rosbag_path=rosbag_path)

    filter_duration = get_filter_fraction(start_time=start_time,
                                          end_time=end_time,
                                          start_rosbag=rosbag_metadata["start"],
                                          end_rosbag=rosbag_metadata["end"])

    if not topics:
        all_topics_dict = rosbag_metadata["topics"]
        img_topic_types = get_image_topic_types()
        topics = get_topic_names_of_type(all_topics=all_topics_dict, filter_topic_types=img_topic_types)

    bag = Bag(rosbag_path, "r")
    bridge = CvBridge()
    topic_msg_counter_dict = dict()
    total_number_of_images = 0
    manifest_dict = dict()

    for topic in topics:
        topic_msg_counter_dict[topic] = 0
        total_number_of_images += bag.get_message_count(topic)
        manifest_dict[topic] = dict()

    if sample:
        total_number_of_images /= sample

    if start_time or end_time:
        total_number_of_images = int(total_number_of_images * filter_duration)

    if not topics:
        logging.warning(f"Robologs: no image topics to extract in {rosbag_path}...")

        return

    logging.debug(f"Robologs: extracting images...")
    print(f"Robologs: extracting {total_number_of_images} images...")

    with tqdm(total=total_number_of_images) as pbar:
        for it, (topic, msg, t) in enumerate(bag.read_messages(topics=topics, start_time=start_time, end_time=end_time)):
            if sample and not (topic_msg_counter_dict[topic] % sample) == 0:
                topic_msg_counter_dict[topic] += 1
                continue

            topic_name_underscore = replace_ros_topic_name(topic)

            output_images_folder_folder_path = os.path.join(output_folder, topic_name_underscore)

            if not os.path.exists(output_images_folder_folder_path):
                os.makedirs(output_images_folder_folder_path)

            if "compressedDepth" in msg.format:
                cv_image = convert_compressed_depth_to_cv2(msg)
            else:
                cv_image = bridge.compressed_imgmsg_to_cv2(msg)

            if naming == "rosbag_timestamp":
                image_name = get_image_name_from_timestamp(timestamp=t.to_nsec(),
                                                           file_format=file_format)

            elif naming == "message_timestamp":
                image_name = get_image_name_from_timestamp(timestamp=msg.header.stamp.to_nsec(),
                                                           file_format=file_format)

            else:
                image_name = get_image_name_from_index(index=topic_msg_counter_dict[topic],
                                                       file_format=file_format)

            image_name = f"{topic_name_underscore}_{image_name}"

            image_path = os.path.join(output_images_folder_folder_path, image_name)

            if resize:
                cv_image = utils.img_utils.resize_image(img=cv_image,
                                                        new_width=resize[0],
                                                        new_height=resize[1])

            cv2.imwrite(image_path, cv_image)

            if create_manifest:
                manifest_dict[topic][image_name] = create_manifest_entry_dict(msg_timestamp=msg.header.stamp.to_nsec(),
                                                                              rosbag_timestamp=t.to_nsec(),
                                                                              file_path=image_path,
                                                                              index=topic_msg_counter_dict[topic])

            if topic in topic_msg_counter_dict.keys():
                topic_msg_counter_dict[topic] += 1

            pbar.update(1)

    if create_manifest:
        for key in manifest_dict.keys():
            output_images_folder_folder_path = os.path.join(output_folder, replace_ros_topic_name(key))
            output_path_manifest_json = os.path.join(output_images_folder_folder_path, "img_manifest.json")
            utils.file_utils.save_json(manifest_dict[key], output_path_manifest_json)

    return


def convert_compressed_depth_to_cv2(compressed_depth):
    """
    Convert a compressedDepth topic image into a cv2 image.
    compressed_depth must be from a topic /bla/compressedDepth
    as it's encoded in PNG
    Code from: https://answers.ros.org/question/249775/display-compresseddepth-image-python-cv2/
    """
    depth_fmt, compr_type = compressed_depth.format.split(';')
    # remove white space
    depth_fmt = depth_fmt.strip()
    compr_type = compr_type.strip().replace(" png", "")
    if compr_type != "compressedDepth":
        raise Exception("Compression type is not 'compressedDepth'."
                        "You probably subscribed to the wrong topic.")

    depth_header_size = 12
    raw_data = compressed_depth.data[depth_header_size:]

    depth_img_raw = cv2.imdecode(np.frombuffer(raw_data, np.uint8), 0)

    if depth_img_raw is None:
        # probably wrong header size
        raise Exception("Could not decode compressed depth image."
                        "You may need to change 'depth_header_size'!")
    result = cv2.normalize(depth_img_raw, depth_img_raw, 0, 255, norm_type=cv2.NORM_MINMAX)

    im_color = cv2.applyColorMap(depth_img_raw, cv2.COLORMAP_JET)

    return im_color
