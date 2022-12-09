import click
from robologs.destinations.aws.s3 import s3_utils


@click.command()
@click.option('--input', '-i', type=str, required=True, help='Input folder for S3 upload')
@click.option('--bucket_name', '-b', type=str, required=True, help='S3 Bucket Path')
@click.option('--prefix', '-p', type=str, default="rosbag_metadata.json", help='S3 Prefix Path')
def upload_to_s3(input, bucket_name, prefix):
    """Upload a folder to S3"""

    s3_utils.upload_files(path=input,
                         bucket_name=bucket_name,
                         prefix=prefix)

    return


if __name__ == '__main__':
    upload_to_s3()
