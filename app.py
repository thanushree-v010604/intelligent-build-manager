from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import zipfile
import tempfile

from pipeline import run_pipeline

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Static + Templates
# =========================
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# =========================
# FRONTEND ROUTE
# =========================
@app.get("/", response_class=HTMLResponse)
def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# =========================
# MODELS
# =========================
class GenerateRequest(BaseModel):
    prompt: str
    language: str


class BuildRequest(BaseModel):
    code: str
    language: str


class CodeRequest(BaseModel):
    code: str
    language: str
    prompt: Optional[str] = None


class ExplainRequest(BaseModel):
    code: str
    language: str

# =========================
# API ROUTES
# =========================
@app.post("/generate")
def generate_code(data: GenerateRequest):
    return run_pipeline(
        stage="generate",
        prompt=data.prompt,
        language=data.language
    )


@app.post("/build")
def build_code(data: BuildRequest):
    return run_pipeline(
        stage="build",
        code=data.code,
        language=data.language
    )


@app.post("/suggest")
def suggest_fix(data: CodeRequest):
    return run_pipeline(
        stage="suggest",
        code=data.code,
        language=data.language,
        prompt=data.prompt
    )


@app.post("/explain")
def explain_code(data: ExplainRequest):
    return run_pipeline(
        stage="explain",
        code=data.code,
        language=data.language
    )


# =========================
# DOWNLOAD ROUTE
# =========================
@app.post("/download")
def download_project(data: CodeRequest):

    temp_dir = tempfile.mkdtemp()

    main_file_path = os.path.join(temp_dir, "main.py")
    with open(main_file_path, "w", encoding="utf-8") as f:
        f.write(data.code)

    requirements_path = os.path.join(temp_dir, "requirements.txt")
    with open(requirements_path, "w") as f:
        if data.language == "python":
            f.write("flask\n")
        else:
            f.write("# Add dependencies here\n")

    zip_path = os.path.join(temp_dir, "project.zip")

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(main_file_path, "main.py")
        zipf.write(requirements_path, "requirements.txt")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="project.zip"
    )


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)