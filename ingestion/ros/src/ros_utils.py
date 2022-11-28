"""Rosbag utilities

This module contains functions to extract metadata from rosbags.

"""

import yaml
import os
import glob
from rosbag.bag import Bag


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

