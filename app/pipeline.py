from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from app.services.gemini_client import GeminiClient
from app.services.openai_tts import OpenAITTSClient
from app.services.youtube_client import YouTubeClient


@dataclass
class VideoSummary:
    video_id: str
    title: str
    author: str
    topic_sentence: str
    summary_text: str


class PodcastPipeline:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.youtube_client = YouTubeClient()
        self.gemini_client = GeminiClient()
        self.tts_client = OpenAITTSClient()

    def run(self, playlist_url: str, compress_ratio: int) -> dict:
        playlist_id, video_urls = self.youtube_client.get_playlist_videos(playlist_url)
        if not video_urls:
            raise ValueError("Playlistte video bulunamadı.")

        summaries = []
        for url in video_urls:
            metadata = self.youtube_client.get_video_metadata(url)
            transcript = self.youtube_client.get_transcript(metadata.video_id)
            summary = self.gemini_client.summarize_video(
                transcript=transcript,
                compress_ratio=compress_ratio,
                title=metadata.title,
                author=metadata.author,
            )
            summaries.append(
                VideoSummary(
                    video_id=metadata.video_id,
                    title=metadata.title,
                    author=metadata.author,
                    topic_sentence=summary["topic_sentence"],
                    summary_text=summary["summary_text"],
                )
            )
            self._save_summary(summaries[-1])

        podcast_script = self.gemini_client.build_podcast_script(summaries)
        podcast_path = self._save_podcast_script(playlist_id, podcast_script)

        audio_path = None
        if self.tts_client.is_configured:
            audio_path = self._save_audio(playlist_id, podcast_script)

        return {
            "playlist_id": playlist_id,
            "summary_files": [str(self._summary_path(s.video_id)) for s in summaries],
            "podcast_script": str(podcast_path),
            "audio_file": str(audio_path) if audio_path else None,
        }

    def _summary_path(self, video_id: str) -> Path:
        return self.output_dir / "summaries" / f"{video_id}.txt"

    def _save_summary(self, summary: VideoSummary) -> None:
        path = self._summary_path(summary.video_id)
        content = (
            f"Video: {summary.title}\n"
            f"Kanal: {summary.author}\n"
            f"Ana konu: {summary.topic_sentence}\n\n"
            f"{summary.summary_text}\n"
        )
        path.write_text(content, encoding="utf-8")

    def _save_podcast_script(self, playlist_id: str, script: str) -> Path:
        path = self.output_dir / "podcasts" / f"{playlist_id}.txt"
        path.write_text(script, encoding="utf-8")
        return path

    def _save_audio(self, playlist_id: str, script: str) -> Path:
        audio_path = self.output_dir / "audio" / f"{playlist_id}.mp3"
        audio_path.write_bytes(self.tts_client.synthesize(script))
        return audio_path


def run_pipeline(playlist_url: str, compress_ratio: int, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    for folder in ["summaries", "podcasts", "audio"]:
        (output_dir / folder).mkdir(parents=True, exist_ok=True)

    pipeline = PodcastPipeline(output_dir=output_dir)
    return pipeline.run(playlist_url=playlist_url, compress_ratio=compress_ratio)
