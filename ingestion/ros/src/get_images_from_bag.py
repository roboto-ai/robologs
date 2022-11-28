import argparse
import os.path

import ros_utils
import utils.file_utils
import argument_parsers


def main():
    parser = argparse.ArgumentParser(description="Get Images from Rosbag")

    parser.add_argument(
        '-i', '--input',
        help='single rosbag, or folder with rosbags')

    parser.add_argument(
        '-o', '--output',
        help="output folder",
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
        help="naming convention for output images. Options are: rosbag_timestamp, message_timestamp, or sequential",
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

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    topics = args.topics.split(',') if args.topics is not None else args.topics
    resize = argument_parsers.get_width_height_from_args(args.resize)
    sample = int(args.sample) if args.sample is not None else args.sample

    # rosbag_info_dict = ros_utils.get_bag_info_from_file_or_folder(input_path)

    # if os.path.isdir(output_path):
    #     output_file_path = os.path.join(output_path, output_filename)
    #     utils.file_utils.save_json(rosbag_info_dict, output_file_path)

    if os.path.isfile(input_path):
        if not topics:
            all_topics_dict = ros_utils.get_bag_info_from_file(rosbag_path=input_path)["topics"]
            img_topic_types = ros_utils.get_image_topic_types()
            print(img_topic_types)
            print(all_topics_dict)
            topics = ros_utils.get_topic_names_of_type(all_topics=all_topics_dict,
                                                       filter_topic_types=img_topic_types)
            print(topics)
            exit()
        ros_utils.get_images_from_bag(rosbag_path=input_path,
                                      output_folder=output_path,
                                      file_format=args.format,
                                      create_manifest=args.manifest,
                                      topics=topics,
                                      naming=args.naming,
                                      resize=resize,
                                      sample=sample)


if __name__ == '__main__':
    main()
