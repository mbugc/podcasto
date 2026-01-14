from __future__ import annotations

from dataclasses import dataclass

from pytubefix import Playlist, YouTube
from youtube_transcript_api import YouTubeTranscriptApi


@dataclass
class VideoMetadata:
    video_id: str
    title: str
    author: str


class YouTubeClient:
    def get_playlist_videos(self, playlist_url: str) -> tuple[str, list[str]]:
        playlist = Playlist(playlist_url)
        playlist_id = playlist.playlist_id
        return playlist_id, list(playlist.video_urls)

    def get_video_metadata(self, video_url: str) -> VideoMetadata:
        video = YouTube(video_url)
        return VideoMetadata(video_id=video.video_id, title=video.title, author=video.author)

    def get_transcript(self, video_id: str) -> str:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["tr", "en"])
        return " ".join(item["text"] for item in transcript)
