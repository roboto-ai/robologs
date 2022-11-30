import argparse
import os.path

import ros_utils
import utils.file_utils


def main():
    parser = argparse.ArgumentParser(description="Get Summary from Rosbag")
    parser.add_argument(
        '-i', '--input',
        help='single rosbag, or folder with rosbags')

    parser.add_argument(
        '-o', '--output',
        help="output folder, or json path",
    )

    parser.add_argument(
        '-f', '--file_name',
        default="rosbag_metadata.json",
        help="output file name",
    )

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    output_filename = args.file_name

    rosbag_info_dict = ros_utils.get_bag_info_from_file_or_folder(input_path=input_path)

    if os.path.isdir(output_path):
        output_file_path = os.path.join(output_path, output_filename)
        utils.file_utils.save_json(data=rosbag_info_dict,
                                   path=output_file_path)

    if os.path.isfile(output_path):
        utils.file_utils.save_json(data=rosbag_info_dict,
                                   path=output_path)

    return


if __name__ == '__main__':
    main()
