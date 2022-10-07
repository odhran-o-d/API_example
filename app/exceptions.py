from fastapi import HTTPException
import aiofiles.os as aios


def test_file_name(name):
    if len(name.split(".")) != 2:
        raise HTTPException(status_code=400, detail="Invalid file name")


def test_media_type(format, types=["png", "jpeg"]):
    if format not in types:
        raise HTTPException(status_code=415, detail="Unsupported media type")


async def test_file_exists(filepath):
    if not await aios.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found")
