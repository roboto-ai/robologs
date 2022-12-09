import pytest
from robologs.sources.ros1 import ros_utils


def test_get_image_name_from_index():
    assert ros_utils.get_image_name_from_index(123, file_format="png", zero_padding=6) == "000123.png"
