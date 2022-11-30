import shutil
import json
import uuid
import tarfile
import os
import glob
from zipfile import ZipFile
from typing import Union


def split_folder_path_to_list(path: str) -> list:
    """
    This function splits a path into a list.
    Args:
        path (str): file path

    Returns: A list with path components
    """
    path = os.path.normpath(path)
    return path.split(os.sep)


def create_directory(path: str, delete_if_exists: bool = False) -> None:
    """
    This function creates a directory.
    Args:
        path (str): directory path
        delete_if_exists (bool): if True, existing directory will be deleted

    Returns: None
    """
    if delete_if_exists:
        if os.path.exists(path):
            shutil.rmtree(path)

    if not os.path.exists(path):
        os.makedirs(path)
    return


def check_file_exists(path: str) -> None:
    """
    This function checks if a file exists, and
    raises an exception if not
    Args:
        path (str): input file path

    Returns: None
    """
    if not os.path.exists(path):
        raise Exception(f"{path } does not exist.")
    return


def save_json(data: Union[dict, list], path: str) -> None:
    """
    This function saves a list or
    Args:
        data (dict or list):
        path (str):

    Returns:
    """
    with open(path, "w") as f_json:
        json.dump(data, f_json, indent=4, sort_keys=True)

    return


def read_json(json_path: str):
    """
    This function reads a json file and return a JSON object
    Args:
        json_path (str): JSON file path

    Returns: JSON object
    """
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data


def create_uuid() -> str:
    """
    This function returns a UUID
    Returns: UUID
    """
    return str(uuid.uuid4())


def find_sub_folder(sub_folder_name: str, search_path: str) -> list:
    """
    This function finds a filename in a subfolder.
    Args:
        sub_folder_name (str): name of subfolder
        search_path (str): path of folder to be searched

    Returns: A list with filenames
    """

    result = []
    for root, dir, files in os.walk(search_path):
        print(root)
        print(dir)
        if sub_folder_name in dir:
            result.append(os.path.join(root))
    return result


def unzip_file_to_folder(path_zip_file: str, output_folder: str) -> None:
    """
    This function unzips a file to a specific folder location.
    Args:
        path_zip_file (str): absolute path of .zip file
        output_folder (str): absolute path of output folder

    Returns: None
    """
    with ZipFile(path_zip_file, 'r') as zipObj:
        zipObj.extractall(output_folder)
    return


def untar_file_to_folder(path_tar_file: str, output_folder: str) -> None:
    """
    This function untars a file to a specific folder location.

    Args:
        path_tar_file (str): absolute path of .tar file
        output_folder (str): absolute path of output folder

    Returns: None
    """
    tar_file = tarfile.open(path_tar_file)
    tar_file.extractall(output_folder)
    tar_file.close()
    return


def get_all_files_of_type_in_directory(input_folder: str, file_format: str) -> list:
    """
    This function gets a list of all files of type "file_format" in a directory
    Args:
        input_folder (str): input folder path

    Returns: list with .pdf files

    """
    file_string = f"./*.{file_format}"
    return sorted(glob.glob(os.path.abspath(os.path.join(input_folder, file_string))))


def find_substring_path(input_folder: str, substring: str) -> str:
    """
    This function returns files which containa certain substring
    Args:
        input_folder (str): input folder
        substring (str): substring

    Returns: file path
    """
    glob_str = f"{input_folder}*{substring}*"
    return glob.glob(glob_str)