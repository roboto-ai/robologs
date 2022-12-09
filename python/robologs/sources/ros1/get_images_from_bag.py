import click
import os.path
from robologs.utils.file_utils import file_utils
from robologs.sources.ros1 import ros_utils
from robologs.sources.ros1 import argument_parsers


@click.command()
@click.option('--input', '-i', type=str, required=True, help='A single rosbag, or folder with rosbags')
@click.option('--output', '-o', type=str, required=True, help='Output directory')
@click.option('--format', '-f', type=str, default="jpg", help='Output image format')
@click.option('--manifest', '-m', is_flag=True, help='Save manifest.json with timestamps and metadata')
@click.option('--topics', '-t', type=str, help='Topic names used for extraction, comma-separated list')
@click.option('--naming', '-n', default="sequential", help='Naming convention for output images. Options are: rosbag_timestamp, msg_timestamp, or sequential')
@click.option('--resize', '-r', help='Resize image to width,height')
@click.option('--sample', '-s', help='Only extract every n-th frame')
@click.option('--start-time', type=float, help='Only extract from start time')
@click.option('--end-time', type=float, help='Only extract until end time')
def get_images(input, output, format, manifest, topics,
               naming, resize, sample, start_time, end_time):
    """Get images from Rosbag1 format"""

    input_path = input
    output_path = output
    topics = topics.split(',') if topics is not None else topics
    resize = argument_parsers.get_width_height_from_args(resize)
    sample = int(sample) if sample is not None else sample
    start_time = start_time if start_time is not None else start_time
    end_time = end_time if end_time is not None else end_time

    if os.path.isdir(input_path):
        rosbag_file_list = file_utils.get_all_files_of_type_in_directory(input_folder=input_path,
                                                                               file_format="bag")
        for rosbag_path in rosbag_file_list:
            ros_utils.get_images_from_bag(rosbag_path=rosbag_path,
                                          output_folder=output_path,
                                          file_format=format,
                                          create_manifest=manifest,
                                          topics=topics,
                                          naming=naming,
                                          resize=resize,
                                          sample=sample,
                                          start_time=start_time,
                                          end_time=end_time)

    if os.path.isfile(input_path):
        ros_utils.get_images_from_bag(rosbag_path=input_path,
                                      output_folder=output_path,
                                      file_format=format,
                                      create_manifest=manifest,
                                      topics=topics,
                                      naming=naming,
                                      resize=resize,
                                      sample=sample,
                                      start_time=start_time,
                                      end_time=end_time)


if __name__ == '__main__':
    get_images()
