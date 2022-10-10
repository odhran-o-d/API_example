"""
PLEASE NOTE: THIS COODE IS WIP

"""


@app.put("/crop_image", response_class=Response)
async def crop_image(image_name: str, crop: Tuple[int, int, int, int] = [1, 1, 1, 1]):
    c = crop
    directory = f"{out_file_directory}/{image_name}"
    image = directory + "/original_image"
    out_file = directory + f"/crop{c[0]}_{c[1]}_{c[2]}_{c[3]}"

    if not await aios.path.isdir(directory):
        raise HTTPException(status_code=404, detail="Directory not found")

    async with aiofiles.open(image, mode="rb") as f:
        contents: bytes = await f.read()

    """below code is not async"""
    image = Image.open(io.BytesIO(contents))
    if crop is not None:
        image = image.crop(crop)
    bytes = image.tobytes()
    """above code is not async"""

    async with aiofiles.open(out_file, "wb") as out_file:
        await out_file.write(bytes)

    return Response(content=bytes, media_type="image/png")
