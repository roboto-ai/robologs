import click

from . import (clip_rosbag, get_images_from_bag, get_summary_from_bag,
               get_videos_from_bag)


@click.group()
def ros():
    """
    Robologs commands for ROS1 data
    """
    pass


ros.add_command(get_images_from_bag.get_images)
ros.add_command(get_videos_from_bag.get_videos)
ros.add_command(get_summary_from_bag.get_summary)
ros.add_command(clip_rosbag.clip_rosbag)
