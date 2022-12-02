"""Rosbag utilities

This module contains functions to extract data from rosbags.

"""
from bagpy import bagreader

from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr

import os
import glob
from typing import Optional
import cv2
import logging
from tqdm import tqdm
import ros_img_tools


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

    bag = bagreader(rosbag_path)
    file_stats = os.stat(rosbag_path)

    summary_dict = dict()
    summary_dict["start_time"] = bag.start_time
    summary_dict["end_time"] = bag.end_time
    summary_dict["duration"] = bag.end_time - bag.start_time
    summary_dict["file_size_mb"] = file_stats.st_size / (1024 * 1024)
    summary_dict["topics"] = bag.topic_table.to_dict('records')

    return summary_dict


def get_topic_dict(rosbag_metadata_dict: dict) -> dict:
    topic_dict = dict()

    for entry in rosbag_metadata_dict["topics"]:
        topic_dict[entry["Topics"]] = entry
        
    return topic_dict


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
    _, img_name = os.path.split(file_path)
    return {"msg_timestamp": msg_timestamp,
            "rosbag_timestamp": rosbag_timestamp,
            "path": file_path,
            "msg_index": index,
            "img_name": img_name}


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
    return [x["Topics"] for x in all_topics if x["Types"] in filter_topic_types]


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
        return float((end_time-start_time) / rosbag_duration)

    if start_time and not end_time:
        return float((end_rosbag - start_time) / rosbag_duration)

    if end_time and not start_time:
        return float((end_time - start_rosbag) / rosbag_duration)

    if not end_time and not start_time:
        return 1


def check_if_in_time_range(t: float, start_time: float, end_time: float) -> bool:
    """
    Args:
        t (float):
        start_time (float):
        end_time (float):

    Returns:

    """

    if start_time and end_time:
        if t >= start_time and t <= end_time:
            return True
        else:
            return False

    if not start_time and end_time:
        if t <= end_time:
            return True
        else:
            return False

    if start_time and not end_time:
        if t >= start_time:
            return True
        else:
            return False

    if not start_time and not end_time:
        return True


def get_images_from_bag(rosbag_path: str,
                        output_folder: str,
                        file_format: str = "jpg",
                        topics: Optional[list] = None,
                        create_manifest: bool = False,
                        naming: str = "sequential",
                        resize: Optional[list] = None,
                        sample: Optional[int] = None,
                        start_time: Optional[float] = None,
                        end_time: Optional[float] = None):
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
        start_time (float):
        end_time (float):

    Returns: None

    """

    rosbag_metadata_dict = get_bag_info_from_file(rosbag_path=rosbag_path)
    topic_dict = get_topic_dict(rosbag_metadata_dict=rosbag_metadata_dict)

    if not topics:
        all_topics_dict = rosbag_metadata_dict["topics"]
        img_topic_types = get_image_topic_types()
        topics = get_topic_names_of_type(all_topics=all_topics_dict, filter_topic_types=img_topic_types)

    topic_msg_counter_dict = dict()
    total_number_of_images = 0
    manifest_dict = dict()

    for topic in topics:
        if topic not in topic_dict.keys():
            logging.warning(f"Robologs: {topic} not in ROSBag..skipping.")
            continue

        topic_msg_counter_dict[topic] = 0
        total_number_of_images += topic_dict[topic]["Message Count"]
        manifest_dict[topic] = dict()

    nr_imgs_to_extract = total_number_of_images

    if start_time or end_time:
        filter_duration = get_filter_fraction(start_time=start_time,
                                              end_time=end_time,
                                              start_rosbag=rosbag_metadata_dict["start_time"],
                                              end_rosbag=rosbag_metadata_dict["end_time"])
        filter_duration = 0 if filter_duration < 0 else filter_duration

        nr_imgs_to_extract = int(total_number_of_images * filter_duration)

    if sample:
        nr_imgs_to_extract /= sample

    if not topics:
        logging.warning(f"Robologs: no image topics to extract in {rosbag_path}...")

        return
    # 
    logging.debug(f"Robologs: extracting images...")
    print(f"Robologs: iterating over {total_number_of_images} images to extract: {nr_imgs_to_extract} images")

    with Reader(rosbag_path) as reader:
        connections = [x for x in reader.connections if x.topic in topics]

        if not connections:
            logging.warning(f"Robologs: none of the selected topics are in the ROSBag.")
            return

        with tqdm(total=total_number_of_images) as pbar:
            for it, (connection, t, rawdata) in enumerate(reader.messages(connections=connections)):
                topic = connection.topic
                msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
                rosbag_time_s = t * 1e-9
                if not check_if_in_time_range(rosbag_time_s, start_time, end_time):
                    topic_msg_counter_dict[topic] += 1
                    continue

                if sample and not (topic_msg_counter_dict[topic] % sample) == 0:
                    topic_msg_counter_dict[topic] += 1
                    continue

                topic_name_underscore = replace_ros_topic_name(topic)

                msg_timestamp = int(str(msg.header.stamp.sec) + str(msg.header.stamp.nanosec))

                output_images_folder_folder_path = os.path.join(output_folder, topic_name_underscore)

                if not os.path.exists(output_images_folder_folder_path):
                    os.makedirs(output_images_folder_folder_path)

                if "compressedDepth" in msg.format:
                    cv_image = ros_img_tools.convert_compressed_depth_to_cv2(msg)
                else:
                    cv_image = ros_img_tools.convert_image_to_cv2(msg)

                if naming == "rosbag_timestamp":
                    image_name = get_image_name_from_timestamp(timestamp=t,
                                                               file_format=file_format)

                elif naming == "msg_timestamp":
                    image_name = get_image_name_from_timestamp(timestamp=msg_timestamp,
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
                    manifest_dict[topic][image_name] = create_manifest_entry_dict(msg_timestamp=msg_timestamp,
                                                                                  rosbag_timestamp=t,
                                                                                  file_path=image_path,
                                                                                  index=topic_msg_counter_dict[topic])

                if topic in topic_msg_counter_dict.keys():
                    topic_msg_counter_dict[topic] += 1

                pbar.update(1)

        if create_manifest:
            for key in manifest_dict.keys():
                output_images_folder_folder_path = os.path.join(output_folder, replace_ros_topic_name(key))

                if not os.path.exists(output_images_folder_folder_path):
                    os.makedirs(output_images_folder_folder_path)

                output_path_manifest_json = os.path.join(output_images_folder_folder_path, "img_manifest.json")
                utils.file_utils.save_json(manifest_dict[key], output_path_manifest_json)

    return

