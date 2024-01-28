from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path
<<<<<<< HEAD
from .data import get_resume_to_text
=======
from .data import get_resume_to_text, add_batch_resumes
>>>>>>> 1962557977b056e40b734cf1630d36505516c057

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
async def upload_file(file: UploadFile):
    Path("./app/db/files").mkdir(parents=True, exist_ok=True)
    with open(f"./app/db/files/{file.filename}", "wb") as f:
        shutil.copyfileobj(file.file, f)

    # [{filename: 'test.pdf', contents: []}, {filename: 'test2.pdf', contents: []}]
    file_texts = get_resume_to_text("./app/db/files", content_type="text")
    add_batch_resumes(file_texts)
    return {"filename": file.filename}


@router.get("/")
async def get_files():
    path = Path("./app/db/files")
    path.mkdir(parents=True, exist_ok=True)
    file_names = list(path.glob("*.pdf"))
    file_names = [x.name for x in file_names]
    return {"files": file_names}
