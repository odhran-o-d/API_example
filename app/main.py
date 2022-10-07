from io import BytesIO
import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import aiofiles
import aiofiles.os as aios
from uuid import uuid4
from PIL import Image
import uvicorn
from pydantic import BaseModel


app = FastAPI()
out_file_directory = "data"  # TODO: replace with real database


def test_file_name(name):
    if len(name.split(".")) != 2:
        raise HTTPException(status_code=400, detail="Invalid file name")


def test_media_type(format, types=["png", "jpeg"]):
    if format not in types:
        raise HTTPException(status_code=415, detail="Unsupported media type")


async def test_file_exists(filepath):
    if not await aios.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="File not found")


@app.post("/upload_image")
async def upload_image(in_file: UploadFile = File(...)):
    file_type = in_file.content_type
    test_media_type(file_type, types=["image/png", "image/jpeg"])

    file_extension = file_type.split("/")[-1]
    uid = str(uuid4())
    await aios.mkdir(os.path.join(out_file_directory, uid))
    file_path = f"{out_file_directory}/{uid}/image"
    contents = await in_file.read()

    if file_type != "image/png":
        image = Image.open(BytesIO(contents))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        async with aiofiles.open(f"{file_path}.png", "wb") as out_file:
            await out_file.write(buffer.getbuffer())

    async with aiofiles.open(f"{file_path}.{file_extension}", "wb") as out_file:
        await out_file.write(contents)

    return {"Result": uid}


class image_url(BaseModel):
    url: str


@app.post("/upload_from_url")
async def upload_from_url(item: image_url):
    file_type = in_file.content_type
    test_media_type(file_type, types=["image/png", "image/jpeg"])

    file_extension = file_type.split("/")[-1]
    uid = str(uuid4())
    await aios.mkdir(os.path.join(out_file_directory, uid))
    file_path = f"{out_file_directory}/{uid}/image"
    contents = await in_file.read()

    if file_type != "image/png":
        image = Image.open(BytesIO(contents))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        async with aiofiles.open(f"{file_path}.png", "wb") as out_file:
            await out_file.write(buffer.getbuffer())

    async with aiofiles.open(f"{file_path}.{file_extension}", "wb") as out_file:
        await out_file.write(contents)

    return {"Result": uid}


@app.get(
    "/imagefile",
    response_class=FileResponse,
)
async def get_image_file(name: str):
    test_file_name(name)

    image_name, format = name.split(".")
    test_media_type(format)

    image_path = f"{out_file_directory}/{image_name}/image"
    await test_file_exists(image_path + ".png")

    if format == "png":
        return FileResponse(image_path + ".png")

    if format == "jpeg":
        if not await aios.path.isfile(image_path + ".jpeg"):
            image = Image.open(image_path + ".png").convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            async with aiofiles.open(image_path + ".jpeg", "wb") as out_file:
                await out_file.write(buffer.getbuffer())

        return FileResponse(image_path + ".jpeg")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    fpath = "image.jpeg"
    url = "http://localhost:8000/"

    packet = upload_image(files={"file": ("filename", open(fpath, "rb"), "image/jpeg")})


# feature order:

# 1: add some 404s etc
# 2: right some pytest
