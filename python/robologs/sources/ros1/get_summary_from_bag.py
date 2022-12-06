import click
import os.path

from robologs.utils.file_utils import file_utils
from robologs.sources.ros1 import ros_utils

@click.command()
@click.option('--input', '-i', type=str, required=True, help='A single rosbag, or folder with rosbags')
@click.option('--output', '-o', type=str, required=True, help='Output directory, or json path')
@click.option('--file-name', '-f', type=str, default="rosbag_metadata.json", help='Output file name')
def get_summary(input, output, file_name):
    """Get summary of Rosbag1 data"""

    input_path = input
    output_path = output
    output_filename = file_name

    rosbag_info_dict = ros_utils.get_bag_info_from_file_or_folder(input_path=input_path)

    if os.path.isdir(output_path):
        output_file_path = os.path.join(output_path, output_filename)
        file_utils.save_json(data=rosbag_info_dict,
                             path=output_file_path)

    if os.path.isfile(output_path):
        file_utils.save_json(data=rosbag_info_dict,
                             path=output_path)

    return

if __name__ == '__main__':
    get_summary()
