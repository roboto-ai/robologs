import os.path

import click

from robologs.sources.ros1 import ros_utils
from robologs.utils.file_utils import file_utils


@click.command()
@click.option("--input", "-i", type=str, required=True, help="A single rosbag or folder with rosbags")
@click.option("--output", "-o", type=str, required=True, help="Output directory")
@click.option("--topics", type=str, help="Topic names used for extraction, comma-separated list")
@click.option("--start-time", type=float, help="Only extract from start time")
@click.option("--end-time", type=float, help="Only extract until end time")
@click.option("--name", type=str, help="Output name of rosbag, only is used when there is a single input bag")
@click.option("--timestamp_type", type=str, help="valid values are [rosbag_ns, offset_s]", default="rosbag_ns")
def clip_rosbag(input, output, topics, start_time, end_time, name, timestamp_type):
    """Get images from Rosbag1 format"""

    input_path = input
    output_path = output
    topics = topics.split(",") if topics is not None else topics
    start_time = start_time if start_time is not None else start_time
    end_time = end_time if end_time is not None else end_time
    timestamp_type = timestamp_type

    if os.path.isdir(input_path):
        rosbag_file_list = file_utils.get_all_files_of_type_in_directory(input_folder=input_path, file_format="bag")
        for it, rosbag_path in enumerate(rosbag_file_list):

            _, output_name = os.path.split(rosbag_path)
            output_name = output_name.replace(".bag", "_cropped_.bag")

            output_path_cropped_bag = os.path.join(output_path, output_name)

            ros_utils.get_clipped_bag_file(
                input_bag_path=rosbag_path,
                output_bag_path=output_path_cropped_bag,
                start_time=start_time,
                end_time=end_time,
                topic_list=topics,
                timestamp_type=timestamp_type,
            )

    if os.path.isfile(input_path):
        if name:
            output_name = name
        else:
            _, output_name = os.path.split(input_path)
            output_name = output_name.replace(".bag", "_cropped.bag")
        output_path_cropped_bag = os.path.join(output_path, output_name)
        ros_utils.get_clipped_bag_file(
            input_bag_path=input_path,
            output_bag_path=output_path_cropped_bag,
            start_time=start_time,
            end_time=end_time,
            topic_list=topics,
            timestamp_type=timestamp_type,
        )


if __name__ == "__main__":
    clip_rosbag()
