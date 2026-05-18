from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.utils.image_utils import encode_image_to_base64, validate_image_file


def test_encode_image_to_base64():
    encoded_image = encode_image_to_base64(b"test-image")

    assert isinstance(encoded_image, str)
    assert encoded_image


def test_validate_image_file_valid():
    file = Mock()
    file.content_type = "image/png"

    assert validate_image_file(file) is True


def test_validate_image_file_invalid():
    file = Mock()
    file.content_type = "text/plain"

    with pytest.raises(HTTPException):
        validate_image_file(file)
