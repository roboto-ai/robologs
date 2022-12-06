import click

@click.group()
def ros2():
    """
    Robologs commands for ROS2 data
    """
    pass

@ros2.command()
def noop():
    click.echo('This is the noop subcommand of the ros2 command')