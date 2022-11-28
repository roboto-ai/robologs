"""Rosbag utilities

This module contains functions to extract data from rosbags.

"""

import yaml
import os
import glob
from rosbag.bag import Bag
from typing import Tuple, Optional
from cv_bridge import CvBridge


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


def get_image_topic_types():
    return ["sensor_msgs/CompressedImage", "sensor_msgs/Image"]


def get_topic_names_of_type(all_topics: list, filter_topic_types: list) -> list:
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


# def get_images_from_bag(topic,
#                         msg,
#                         t,
#                         output_folder: str,
#                         file_format: str = "jpg",
#                         topics: Optional[list] = None,
#                         create_manifest: bool = False,
#                         naming: str = "sequential",
#                         resize: Optional[Tuple[int, int]] = None,
#                         sample: Optional[int] = None):

def get_images_from_bag(rosbag_path: str,
                        output_folder: str,
                        file_format: str = "jpg",
                        topics: Optional[list] = None,
                        create_manifest: bool = False,
                        naming: str = "sequential",
                        resize: Optional[Tuple[int, int]] = None,
                        sample: Optional[int] = None):
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

    Returns: None

    """

    bag = Bag(rosbag_path, "r")

    # for topic, msg, t in bag.read_messages(topics=topics):
    #     function(topic, msg, t, args)
    #
    #
    # topic_name_underscore = topic.replace("/", "_")
    # print(output_folder)
    #
    # output_images_folder_folder_path = os.path.join(output_folder, topic_name_underscore)
    #
    # # if not os.path.exists(output_images_folder_folder_path):
    # #     os.makedirs(output_images_folder_folder_path)
    #
    # print(msg.format)

    return

#     bag = Bag(rosbag_path, "r")
#     bridge = CvBridge()
#     timestamp_dict = dict()
#     # for entry in topics:
#     #     clean_topic_name = RosbagLoader.get_clean_topic_name(entry)
#     #
#     #     timestamp_dict[clean_topic_name] = list()
#     #
#     # # extract images
#     #
#     # for topic, msg, t in bag.read_messages(topics=topics):
#     #     print(t)
#     #     clean_topic_name = RosbagLoader.get_clean_topic_name(topic)
#     #     output_path_image_topic = os.path.join(output_folder, clean_topic_name)
#     #
#     #     if not os.path.exists(output_path_image_topic):
#     #         os.makedirs(output_path_image_topic)
#     #     # cv_image = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="16UC3")
#     #     if "compressedDepth" in msg.format:
#     #         cv_image = RosbagLoader.convert_compressedDepth_to_cv2(msg)
#     #     else:
#     #         cv_image = bridge.compressed_imgmsg_to_cv2(msg)
#     #
#     #     timestamp = msg.header.stamp.to_nsec()
#     #     image_name = clean_topic_name + "_" + RosbagLoader.get_image_name_from_timestamp(timestamp)
#     #     img_path = os.path.join(output_path_image_topic, image_name)
#     #     timestamp_dict[clean_topic_name].append((timestamp, image_name, img_path))
#     #     cv2.imwrite(img_path, cv_image)
#     #
#     # bag.close()
#
#     return timestamp_dict

