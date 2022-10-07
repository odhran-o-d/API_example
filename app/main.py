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

app = FastAPI()
out_file_directory = "data"  # TODO: replace with real database


async def exceptions_404(c):
    if "directory" in c:
        if not await aios.path.isdir(c["directory"]):
            raise HTTPException(status_code=404, detail="Directory not found")


# uploading files will be a POST request as it will not be idempotent
@app.post("/uploadfile/")
async def post_endpoint(in_file: UploadFile = File(...)):
    uid = str(uuid4())
    await aios.mkdir(os.path.join(out_file_directory, uid))

    if in_file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    file_extension = in_file.content_type.split("/")[-1]

    out_file = f"{out_file_directory}/{uid}/original_image"
    async with aiofiles.open(out_file, "wb") as out_file:
        while content := await in_file.read(
            1024
        ):  # TODO: security check data + check is image
            await out_file.write(content)  # async write chunk
    return {"Result": uid}


@app.get(
    "/image",
    response_class=Response,
)
async def get_image(image_name: str, format: str):
    directory = f"{out_file_directory}/{image_name}"

    image = directory + "/original_image"

    if not await aios.path.isdir(directory):
        raise HTTPException(status_code=404, detail="Directory not found")

    async with aiofiles.open(image, mode="rb") as f:
        contents: bytes = await f.read()

    if format == "png":
        return Response(content=contents, media_type="image/png")

    if format == "jpeg":
        pil_image = Image.open(BytesIO(contents))
        pil_image = pil_image.convert("RGB")
        with BytesIO() as f:
            pil_image.save(f, format="JPEG")
            f.seek(0)
            ima_jpg = Image.open(f)

        return Response(content=ima_jpg, media_type="image/jpeg")


@app.post("/")
def image_filter(img: UploadFile = File(...)):
    original_image = Image.open(img.file)

    filtered_image = BytesIO()
    original_image.save(filtered_image, "JPEG")
    filtered_image.seek(0)

    return StreamingResponse(filtered_image, media_type="image/jpeg")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# assuming an image is already uploaded, image processing should use a GET request
