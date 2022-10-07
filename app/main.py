from typing import Union

from fastapi import FastAPI, Header, HTTPException, File, UploadFile
from pydantic import BaseModel
import aiofiles
from uuid import uuid4

app = FastAPI()
out_file_directory = "data"

# uploading files will be a POST request as it will not be idempotent
@app.post("/uploadfile/")
async def post_endpoint(in_file: UploadFile = File(...)):
    uid = str(uuid4())
    out_file = f"{out_file_directory}/{uid}"
    async with aiofiles.open(out_file, "wb") as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    return {"Result": uid}


# retrieving files will be a GET request - obviously


# assuming an image is already uploaded, image processing should use a GET request
