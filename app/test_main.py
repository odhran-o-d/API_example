import re
from fastapi.testclient import TestClient
import pytest
from .main import app
import requests

client = TestClient(app)


# remember: must start all test functions with test_


def test_create_item():
    fpath = "./image.jpeg"
    response = client.post(
        "/upload_image",
        files={"in_file": ("filename", open(fpath, "rb"), "image/jpeg")},
    )
    assert response.status_code == 200


def test_validate_conversion_of_json_to_png():
    fpath = "./image.jpeg"
    response = client.post(
        "/upload_image",
        files={"in_file": ("filename", open(fpath, "rb"), "image/jpeg")},
    )
    image_identifier = response.json()["Result"]
    response = client.get(f"/imagefile?name={image_identifier}.png")
    assert response.status_code == 200


def test_validate_conversion_of_png_to_json():
    fpath = "./image.png"
    response = client.post(
        "/upload_image",
        files={"in_file": ("filename", open(fpath, "rb"), "image/png")},
    )
    image_identifier = response.json()["Result"]
    response = client.get(f"/imagefile?name={image_identifier}.jpeg")
    assert response.status_code == 200


def test_get_png_file():
    response = client.get("/imagefile?name=test2.png")
    assert response.status_code == 200


def test_get_jpeg_file():
    response = client.get("/imagefile?name=test2.jpeg")
    assert response.status_code == 200


def test_get_bad_extension():
    response = client.get("/imagefile?name=test2.jpegs")
    assert response.status_code == 415


def test_get_bad_name():
    response = client.get("/imagefile?name=test3.jpeg")
    assert response.status_code == 404


# def test_read_item_bad_token():
#     response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Invalid X-Token header"}


# def test_read_inexistent_item():
#     response = client.get(
#         "/items/baz",
#         headers={"X-Token": "coneofsilence"},
#     )
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}
