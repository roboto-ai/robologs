import os

import boto3


def get_s3_link_from_topic(topic_path: str, bucket: str, prefix: str, split: str = "parquet") -> str:
    """
    This function returns the S3 location of the topic folder name.
    Args:
        topic_path: local folder path
        bucket: bucket where folder is stored
        prefix: prefix where folder is stored
        split: where to split the local folder path

    Returns: S3 link to stored folder

    """
    folder_name = topic_path.split(split)[1]
    s3_path = f"s3://{bucket}/{prefix}{folder_name}"
    return s3_path


def upload_files(path: str, bucket_name: str, prefix: str = "processed/px4") -> None:
    """
    This function uploads a file to S3
    Args:
        path: local path
        bucket_name: bucket name
        prefix: prefix

    Returns: None

    """
    session = boto3.Session()
    s3 = session.resource("s3")
    bucket = s3.Bucket(bucket_name)

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, "rb") as data:

                upload_path = prefix + "/" + full_path[len(path) :]
                bucket.put_object(Key=upload_path, Body=data)
    return
