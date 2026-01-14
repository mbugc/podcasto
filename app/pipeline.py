from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


OUTPUT_ROOT = Path(__file__).resolve().parent.parent / "outputs"
SUMMARY_DIR = OUTPUT_ROOT / "summaries"
PODCAST_DIR = OUTPUT_ROOT / "podcasts"
AUDIO_DIR = OUTPUT_ROOT / "audio"


@dataclass
class VideoMetadata:
    title: str
    video_id: str
    channel: str
    speakers: list[str]
    topic: str


@dataclass
class SummaryResult:
    metadata: VideoMetadata
    summary: str


class PipelineError(RuntimeError):
    pass


def ensure_output_dirs() -> None:
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)
    PODCAST_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def parse_playlist_id(playlist_url: str) -> str:
    if "list=" not in playlist_url:
        raise PipelineError("Playlist URL does not contain a list parameter.")
    return playlist_url.split("list=")[-1].split("&")[0]


def build_mock_videos(playlist_id: str) -> list[VideoMetadata]:
    return [
        VideoMetadata(
            title="Günün Öne Çıkan Haberleri",
            video_id=f"{playlist_id}-news",
            channel="Örnek Haber",
            speakers=["Sunucu"],
            topic="Günün politika ve ekonomi gelişmeleri",
        ),
        VideoMetadata(
            title="Genel Kültür Notları",
            video_id=f"{playlist_id}-culture",
            channel="Örnek Kültür",
            speakers=["Anlatıcı"],
            topic="Tarihsel perspektif ve kültürel arka plan",
        ),
        VideoMetadata(
            title="Gündem Analizi",
            video_id=f"{playlist_id}-analysis",
            channel="Örnek Analiz",
            speakers=["Yorumcu"],
            topic="Günün ana tartışması ve çıkarımlar",
        ),
    ]


def compress_text(text: str, ratio: float) -> str:
    words = text.split()
    if not words:
        return text
    target_count = max(1, int(len(words) * ratio))
    return " ".join(words[:target_count])


def summarize_video(metadata: VideoMetadata, compression_ratio: float) -> SummaryResult:
    base_summary = (
        f"{metadata.title} videosunda anlatıcı, {metadata.topic} etrafında ana başlıkları "
        "sakin ama net bir tonla sıralıyor. Önce günün verileri ve başlıkları özetliyor, "
        "sonra her başlığın arka planını kısa bir hikaye ile destekliyor. Kritik noktalar "
        "vurgulanırken karşıt görüşlere de kısa değiniliyor ve kapanışta genel çıkarımlar "
        "paylaşılıyor."
    )
    compressed = compress_text(base_summary, compression_ratio)
    return SummaryResult(metadata=metadata, summary=compressed)


def write_summary_file(result: SummaryResult) -> Path:
    filename = f"{result.metadata.video_id}.txt"
    path = SUMMARY_DIR / filename
    header = (
        f"Title: {result.metadata.title}\n"
        f"Video ID: {result.metadata.video_id}\n"
        f"Channel: {result.metadata.channel}\n"
        f"Speakers: {', '.join(result.metadata.speakers)}\n"
        f"Main topic: {result.metadata.topic}\n\n"
    )
    path.write_text(f"{header}{result.summary}\n", encoding="utf-8")
    return path


def build_podcast_script(results: Iterable[SummaryResult]) -> str:
    segments = []
    for result in results:
        segments.append(
            "\n".join(
                [
                    (
                        f"{result.metadata.channel} kanalından {result.metadata.title} videosuna "
                        "geçiyoruz."
                    ),
                    result.summary,
                ]
            )
        )
    intro = "Günün seçkisine hoş geldiniz. Başlıklarımıza hızlıca geçiyoruz."
    outro = "Bültenimiz burada sona eriyor. Yarın yeniden görüşmek üzere."
    return "\n\n".join([intro, *segments, outro])


def write_podcast_script(playlist_id: str, script: str) -> Path:
    path = PODCAST_DIR / f"{playlist_id}.txt"
    path.write_text(script + "\n", encoding="utf-8")
    return path


def write_audio_placeholder(playlist_id: str) -> Path:
    path = AUDIO_DIR / f"{playlist_id}.txt"
    path.write_text(
        "OpenAI TTS çıktısı burada olacak. (Uygulama iskeletinde ses üretilmiyor.)\n",
        encoding="utf-8",
    )
    return path


def run_pipeline(playlist_url: str, compression_ratio: float) -> dict[str, str]:
    ensure_output_dirs()
    playlist_id = parse_playlist_id(playlist_url)
    videos = build_mock_videos(playlist_id)
    results = [summarize_video(video, compression_ratio) for video in videos]
    for result in results:
        write_summary_file(result)
    podcast_script = build_podcast_script(results)
    podcast_path = write_podcast_script(playlist_id, podcast_script)
    audio_path = write_audio_placeholder(playlist_id)

    return {
        "playlist_id": playlist_id,
        "podcast_script_path": str(podcast_path),
        "audio_path": str(audio_path),
        "summary_count": str(len(results)),
    }
