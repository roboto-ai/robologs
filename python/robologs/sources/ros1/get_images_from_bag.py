import argparse
import os.path
import utils.file_utils
from robologs.sources.ros1 import ros_utils
from robologs.sources.ros1 import argument_parsers


def main():
    parser = argparse.ArgumentParser(description="Get Images from Rosbag1",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '-i', '--input',
        help='single rosbag, or folder with rosbags',
        required=True)

    parser.add_argument(
        '-o', '--output',
        help="output folder",
        required=True
    )

    parser.add_argument(
        '-f', '--format',
        default="jpg",
        help="output image format",
    )

    parser.add_argument(
        '-m', '--manifest',
        action='store_true',
        help="save manifest.json with timestamps and metadata",
    )

    parser.add_argument(
        '-t', '--topics',
        type=str,
        help="topic names used for extraction, comma-separated list",
    )

    parser.add_argument(
        '-n', '--naming',
        help="naming convention for output images. Options are: rosbag_timestamp, msg_timestamp, or sequential",
        default="sequential",
    )

    parser.add_argument(
        '-r', '--resize',
        help="resize image to width,height",
    )

    parser.add_argument(
        '-s', '--sample',
        help="only extract every n-th frame",
    )

    parser.add_argument(
        '--start_time',
        type=float,
        help="only extract from start_time",
    )

    parser.add_argument(
        '--end_time',
        type=float,
        help="only extract until end_time",
    )

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    topics = args.topics.split(',') if args.topics is not None else args.topics
    resize = argument_parsers.get_width_height_from_args(args.resize)
    sample = int(args.sample) if args.sample is not None else args.sample
    start_time = args.start_time if args.start_time is not None else args.start_time
    end_time = args.end_time if args.end_time is not None else args.end_time

    if os.path.isdir(input_path):
        rosbag_file_list = utils.file_utils.get_all_files_of_type_in_directory(input_folder=input_path,
                                                                               file_format="bag")
        for rosbag_path in rosbag_file_list:
            ros_utils.get_images_from_bag(rosbag_path=rosbag_path,
                                          output_folder=output_path,
                                          file_format=args.format,
                                          create_manifest=args.manifest,
                                          topics=topics,
                                          naming=args.naming,
                                          resize=resize,
                                          sample=sample,
                                          start_time=start_time,
                                          end_time=end_time)

    if os.path.isfile(input_path):
        ros_utils.get_images_from_bag(rosbag_path=input_path,
                                      output_folder=output_path,
                                      file_format=args.format,
                                      create_manifest=args.manifest,
                                      topics=topics,
                                      naming=args.naming,
                                      resize=resize,
                                      sample=sample,
                                      start_time=start_time,
                                      end_time=end_time)


if __name__ == '__main__':
    main()
