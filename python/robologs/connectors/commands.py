import click
from . import s3_upload


@click.group()
def connectors():
    """
    Robologs commands for connectors
    """
    pass


connectors.add_command(s3_upload.upload_to_s3)
