from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.pipeline import PipelineError, run_pipeline


WEB_DIR = Path(__file__).resolve().parent.parent / "web"

app = FastAPI(title="Podcasto")

app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")


class PlaylistRequest(BaseModel):
    playlist_url: str = Field(..., example="https://www.youtube.com/playlist?list=XYZ")
    compression_ratio: float = Field(0.3, ge=0.1, le=0.6)


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.post("/api/summarize")
async def summarize(request: PlaylistRequest) -> dict[str, str]:
    try:
        result = run_pipeline(request.playlist_url, request.compression_ratio)
    except PipelineError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result
