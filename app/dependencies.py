async def exceptions_404(c):
    if "directory" in c:
        if not await aios.path.isdir(c["directory"]):
            raise HTTPException(status_code=404, detail="Directory not found")

    if not await aios.path.isdir(directory):
        raise HTTPException(status_code=404, detail="Directory not found")
