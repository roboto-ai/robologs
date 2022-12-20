import json
import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key


def upload_json_to_table(json_path: str, table_name: str, region_name: str = "us-west-2") -> None:
    """
    This function uploads a dictionary to a DynamoDB table (currently only used for anomaly detection)
    Args:
        json_path: path to json file
        table_name: name of table (currently only used for anomaly detection)
        region_name: AWS region name of DynamoDB database

    Returns: None

    """

    print(f"upload_json_to_table -> json_path: {json_path}")

    with open(json_path, "r") as f:
        data = json.load(f, parse_float=Decimal)

    dynamodb = boto3.resource("dynamodb", region_name=region_name)

    table = dynamodb.Table(table_name)

    print(f"upload_json_to_table -> length DynamoDB: {str(len(data))}")

    with table.batch_writer() as writer:
        for entry in data:
            print(entry)
            if entry:
                writer.put_item(Item=entry)
            else:
                print(f"upload_json_to_table -> no entry found")
    print("upload_json_to_table -> done uploading")
    return


def update_field_in_table(
    table_name: str, key_name: str, key_value: str, update_dict: dict, region_name: str = "us-west-2"
) -> None:
    """
    This function updates a field in a table
    Args:
        table_name: AWS Table name
        key_name: name of column to be updated in table
        key_value: value of column to be updated
        update_dict: the dictionary which should be entered (with key, value pairs)
        region_name: AWS region name of DynamoDB database

    Returns: None

    """

    update_expression = ["set "]
    update_values = dict()
    dynamodb = boto3.resource("dynamodb", region_name=region_name)

    table = dynamodb.Table(table_name)

    for key, val in update_dict.items():
        update_expression.append(f" {key} = :{key},")
        update_values[f":{key}"] = val

    a, v = "".join(update_expression)[:-1], update_values

    r = table.update_item(
        Key={key_name: key_value},
        UpdateExpression=a,
        ExpressionAttributeValues=dict(v),
    )

    return


def update_tags_field_in_table(
    table_name: str, key_name: str, key_value: str, update_dict: dict, region_name: str = "us-west-2"
) -> None:
    """
    This function updates the tags field in the dataset table.
    It first gets all existing tags, then appends them to the new tags.
    And then updates the table.

    Args:
        table_name: AWS Table name
        key_name: column name of dataset_id, usually 'id'
        key_value: UUID of the dataset
        update_dict: dictionary with tag dictionary
        region_name: AWS region name of DynamoDB database

    Returns: None

    """

    update_expression = ["set "]
    update_values = dict()
    dynamodb = boto3.resource("dynamodb", region_name=region_name)

    table = dynamodb.Table(table_name)

    resp = table.query(KeyConditionExpression=Key(key_name).eq(key_value))
    print(resp)

    if len(resp["Items"]) != 1:
        print("update_tags_field_in_table -> Couldn't update tags field. Mismatch number of dataset table items.")
        return

    if ("tags" in resp["Items"][0]) and ("tags" in update_dict.keys()):

        for old_tag in resp["Items"][0]["tags"]:
            if old_tag not in update_dict["tags"]:
                update_dict["tags"].append(old_tag)

    for key, val in update_dict.items():
        update_expression.append(f" {key} = :{key},")
        update_values[f":{key}"] = val

    a, v = "".join(update_expression)[:-1], update_values

    r = table.update_item(
        Key={key_name: key_value},
        UpdateExpression=a,
        ExpressionAttributeValues=dict(v),
    )

    return


def update_dataset_table(json_path: str, table_name: str, region_name: str = "us-west-2") -> None:
    """
    This function updates the AWS Dataset table with the dataset.json values
    Args:
        json_path: path to dataset.json
        table_name: name of AWS dataset table
        region_name: AWS region name of DynamoDB database

    Returns: None

    """

    print(f"update_dataset_table -> json path: {json_path}")

    with open(json_path, "r") as f:
        data = json.load(f, parse_float=Decimal)

    dynamodb = boto3.resource("dynamodb", region_name=region_name)

    table = dynamodb.Table(table_name)

    print(f"update_dataset_table -> length DynamoDB: {str(len(data))}")

    if len(data) == 1:
        dataset_entry = data[0]
        update_expression = ["set "]
        update_values = dict()
        for key, val in dataset_entry.items():

            # we are not updating the dataset table with the ID, Tags, Timestamp and Description, as these fields are
            # populated by the user upload.

            if key == "id":
                continue

            if key == "tags":
                continue

            if key == "description":
                continue

            if key == "timestamp":
                update_expression.append(f"#t = :{key},")
            else:
                update_expression.append(f" {key} = :{key},")
            update_values[f":{key}"] = val

        a, v = "".join(update_expression)[:-1], update_values

        for kk in v.keys():
            if type(v[kk]).__name__ == "float":
                v[kk] = Decimal(v[kk])

        if "id" in dataset_entry.keys():
            response = table.update_item(
                Key={"id": dataset_entry["id"]},
                UpdateExpression=a,
                ExpressionAttributeValues=dict(v),
                ExpressionAttributeNames={"#t": "timestamp"},
            )
    return


def upload_tables(
    base_folder: str,
    args: dict,
    name_topic_table: str,
    name_dataset_table: str,
    update_instead_of_replace: bool = False,
    region_name: str = "us-west-2",
) -> str:
    """
    This function uploads the dataset.json and the topics.json to the dataset and topic table
    Args:
        base_folder: base ingestion path
        args: configuration dict
        name_topic_table: name of AWS topic table
        name_dataset_table: name of AWS dataset table
        update_instead_of_replace: if True, then the table gets updated, as opposed to creating a new entry
        region_name: region name of dynamo DB table
    Returns: dataset id

    """

    tables_folder = os.path.join(base_folder, "tables")

    if args["upload_topics"]:
        topic_json = os.path.join(tables_folder, "topic.json")
        print("Uploading Topics table...")
        upload_json_to_table(topic_json, name_topic_table, region_name)

    if args["upload_datasets"]:
        dataset_json = os.path.join(tables_folder, "dataset.json")
        print("Uploading Dataset table...")
        if update_instead_of_replace:
            update_dataset_table(dataset_json, name_dataset_table, region_name)
        else:
            upload_json_to_table(dataset_json, name_dataset_table, region_name)

    dataset_json = os.path.join(tables_folder, "dataset.json")
    with open(dataset_json, "r") as f:
        data = json.load(f, parse_float=Decimal)
    return data[0]["id"]
