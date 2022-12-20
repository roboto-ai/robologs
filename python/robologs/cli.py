from inspect import getmembers

import click

from robologs.connectors.commands import connectors
from robologs.sources.ros1.commands import ros
from robologs.sources.ros2.commands import ros2
from robologs.sources.ulog.commands import ulog


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(
            """
               __          __                
   _________  / /_  ____  / /___  ____ ______
  / ___/ __ \/ __ \/ __ \/ / __ \/ __ `/ ___/
 / /  / /_/ / /_/ / /_/ / / /_/ / /_/ (__  ) 
/_/   \____/_.___/\____/_/\____/\__, /____/  
                               /____/        
"""
        )
    if ctx.invoked_subcommand is None:
        click.echo("Robologs is an open source collection of sensor data transforms")
        click.echo("Run robologs --help to see a list of available commands")
        click.echo("")


cli.add_command(ros)
cli.add_command(ros2)
cli.add_command(ulog)
cli.add_command(connectors)


def main():
    cli()


if __name__ == "__main__":
    main()
