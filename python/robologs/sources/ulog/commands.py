import click

@click.group()
def ulog():
    """
    Robologs commands for ULOG data
    """
    pass

@ulog.command()
def noop():
    click.echo('This is the noop subcommand of the ulog command')