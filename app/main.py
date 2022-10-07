from typing import Union, Tuple, Literal
from io import BytesIO
import os
from fastapi import FastAPI, Header, HTTPException, File, UploadFile
from pydantic import BaseModel
from fastapi.responses import FileResponse, Response, StreamingResponse
import aiofiles
import aiofiles.os as aios
from uuid import uuid4
from PIL import Image
from pydantic import BaseModel, Field
import uvicorn
import shutil

app = FastAPI()
out_file_directory = "data"  # TODO: replace with real database


@app.post("/uploadfile/")
async def post_endpoint(in_file: UploadFile = File(...)):
    if in_file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    uid = str(uuid4())
    await aios.mkdir(os.path.join(out_file_directory, uid))
    file_extension = in_file.content_type.split("/")[-1]
    file_path = f"{out_file_directory}/{uid}/image"
    contents = await in_file.read()

    if in_file.content_type != "image/png":  # convert to png
        image = Image.open(BytesIO(contents))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        async with aiofiles.open(f"{file_path}.png", "wb") as out_file:
            await out_file.write(buffer.getbuffer())

    async with aiofiles.open(f"{file_path}.{file_extension}", "wb") as out_file:
        await out_file.write(contents)  # async write chunk

    return {"Result": uid}


@app.get(
    "/imagefile",
    response_class=FileResponse,
)
async def get_image_file(image_name: str, format: str):
    if format not in ["png", "jpeg"]:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    if format == "png":
        return FileResponse(f"{out_file_directory}/{image_name}/image.png")

    if format == "jpeg":
        if not await aios.path.isfile(f"{out_file_directory}/{image_name}/image.jpeg"):
            image = Image.open(f"{out_file_directory}/{image_name}/image.png")
            image = image.convert("RGB")
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            async with aiofiles.open(
                f"{out_file_directory}/{image_name}/image.jpeg", "wb"
            ) as out_file:
                await out_file.write(buffer.getbuffer())

        return FileResponse(f"{out_file_directory}/{image_name}/image.jpeg")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# assuming an image is already uploaded, image processing should use a GET request
