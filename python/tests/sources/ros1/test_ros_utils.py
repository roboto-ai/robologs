import os

import pytest

from robologs.sources.ros1 import ros_utils
from robologs.utils.file_utils import file_utils


def test_get_image_name_from_index():
    assert ros_utils.get_image_name_from_index(123, file_format="png", zero_padding=6) == "000123.png"


def get_image_bag_file_path(dir_name, file_name):
    base_path_test_resources = os.path.abspath(f"{dir_name}/../../test_resources/")
    file_path = os.path.join(base_path_test_resources, file_name)
    return file_path


def test_get_bag_info_from_file(request):
    input_path = get_image_bag_file_path(request.fspath.dirname, "test_images.bag")
    summary_dict = ros_utils.get_bag_info_from_file(input_path)
    topics = [x["Topics"] for x in summary_dict["topics"]]

    assert topics == ["/alphasense/cam0/image_raw", "/alphasense/cam1/image_raw"]


def test_is_message_within_time_range():

    start_time_rosbag_ns = 10

    end_time_rosbag_ns = 15

    in_time_range, past_end_time = ros_utils.is_message_within_time_range(time_ns=9,
                                                                          start_time_rosbag_ns=start_time_rosbag_ns,
                                                                          end_time_rosbag_ns=end_time_rosbag_ns)

    assert not in_time_range
    assert not past_end_time

    in_time_range, past_end_time = ros_utils.is_message_within_time_range(time_ns=10,
                                                                          start_time_rosbag_ns=start_time_rosbag_ns,
                                                                          end_time_rosbag_ns=end_time_rosbag_ns)
    assert in_time_range
    assert not past_end_time

    in_time_range, past_end_time = ros_utils.is_message_within_time_range(time_ns=12,
                                                                          start_time_rosbag_ns=start_time_rosbag_ns,
                                                                          end_time_rosbag_ns=end_time_rosbag_ns)
    assert in_time_range
    assert not past_end_time

    in_time_range, past_end_time = ros_utils.is_message_within_time_range(time_ns=15,
                                                                          start_time_rosbag_ns=start_time_rosbag_ns,
                                                                          end_time_rosbag_ns=end_time_rosbag_ns)
    assert in_time_range
    assert not past_end_time

    in_time_range, past_end_time = ros_utils.is_message_within_time_range(time_ns=16,
                                                                          start_time_rosbag_ns=start_time_rosbag_ns,
                                                                          end_time_rosbag_ns=end_time_rosbag_ns)
    assert not in_time_range
    assert past_end_time


def test_convert_offset_s_to_rosbag_ns():

    first_timestamp_rosbag_ns = 1649764528071146477

    assert ros_utils.convert_offset_s_to_rosbag_ns(offset_s=0,
                                                   first_rosbag_time_ns=first_timestamp_rosbag_ns) == \
           1649764528071146477

    assert ros_utils.convert_offset_s_to_rosbag_ns(offset_s=10,
                                                   first_rosbag_time_ns=first_timestamp_rosbag_ns) == \
           1649764528071146477 + int(10*1e9)


def test_get_cropped_bag_file(request, tmp_path):
    input_path = get_image_bag_file_path(request.fspath.dirname, "test_images.bag")
    output_path = os.path.join(tmp_path, "output.bag")
    print(output_path)

    topic_list = ["/alphasense/cam0/image_raw"]

    assert os.path.exists(tmp_path)

    assert not os.path.exists(output_path)

    ros_utils.get_clipped_bag_file(input_bag_path=input_path,
                                   output_bag_path=output_path,
                                   topic_list=topic_list)

    assert os.path.exists(output_path)

    summary_dict = ros_utils.get_bag_info_from_file(output_path)
    topics = [x["Topics"] for x in summary_dict["topics"]]

    assert topics == ["/alphasense/cam0/image_raw"]

    output_path_t = os.path.join(tmp_path, "output_.bag")

    ros_utils.get_clipped_bag_file(input_bag_path=output_path,
                                   output_bag_path=output_path_t,
                                   start_time=1649764528171137838,
                                   end_time=1649764528246129638)

    summary_dict = ros_utils.get_bag_info_from_file(output_path_t)

    assert summary_dict["topics"][0]["Message Count"] == 4

    ros_utils.get_clipped_bag_file(input_bag_path=output_path,
                                   output_bag_path=output_path_t,
                                   start_time=0,
                                   end_time=0.1,
                                   timestamp_type="offset_s")

    summary_dict = ros_utils.get_bag_info_from_file(output_path_t)

    assert summary_dict["topics"][0]["Message Count"] == 5

    with pytest.raises(Exception):
        ros_utils.get_clipped_bag_file(input_bag_path=output_path,
                                       output_bag_path=output_path_t,
                                       timestamp_type="weird_type")


def test_get_images_from_bag(request, tmp_path):
    input_path = get_image_bag_file_path(request.fspath.dirname, "test_images.bag")

    output_folder = tmp_path

    folder_name = ros_utils.replace_ros_topic_name("/alphasense/cam0/image_raw")

    output_folder_imgs = os.path.join(output_folder, folder_name)

    assert not os.path.exists(output_folder_imgs)

    ros_utils.get_images_from_bag(rosbag_path=input_path,
                                  output_folder=output_folder,
                                  file_format="jpg")
    assert os.path.exists(output_folder_imgs)

    list_files = file_utils.get_all_files_of_type_in_directory(output_folder_imgs, "jpg")

    assert len(list_files) == 10
