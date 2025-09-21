from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse

app = FastAPI()

def upload(uploaded_file: UploadFile, index: int = 1):
    file = uploaded_file.file
    filename, ext = uploaded_file.filename.split(".")

    with open(f"uploaded_files/{filename}_{index}.{ext}", "wb") as f:
        f.write(file.read())

@app.post("/files")
async def upload_file(uploaded_file: UploadFile):
    upload(uploaded_file)
    return {"status": "ok"}

@app.post("/multiple_files")
async def upload_files(uploaded_files: list[UploadFile]):
    for i, uploaded_file in enumerate(uploaded_files, 1):
        upload(uploaded_file, i)

    return {"status": "ok"}

@app.get("/files/{filename}")
async def get_file(filename: str):
    return FileResponse(filename)

def iter_file(filename: str):
    with open(filename, "rb") as file:
        while chunk := file.read(1024 * 1024):
            yield chunk

@app.get("/streaming_files/{filename}")
async def get_streaming_file(filename: str):
    return StreamingResponse(iter_file(filename), media_type="video/mp4")