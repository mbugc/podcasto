from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl, conint

from app.pipeline import run_pipeline

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

app = FastAPI(title="Podcasto")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class RunRequest(BaseModel):
    playlist_url: HttpUrl
    compress_ratio: conint(ge=10, le=90) = 30


class RunResponse(BaseModel):
    playlist_id: str
    summary_files: List[str]
    podcast_script: str
    audio_file: str | None


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    index_path = BASE_DIR / "static" / "index.html"
    return HTMLResponse(index_path.read_text(encoding="utf-8"))


@app.post("/api/run", response_model=RunResponse)
def run(request: RunRequest) -> RunResponse:
    try:
        result = run_pipeline(
            playlist_url=str(request.playlist_url),
            compress_ratio=request.compress_ratio,
            output_dir=OUTPUT_DIR,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return RunResponse(**result)


@app.get("/api/audio/{playlist_id}")
def get_audio(playlist_id: str) -> FileResponse:
    audio_path = OUTPUT_DIR / "audio" / f"{playlist_id}.mp3"
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(audio_path)
