from __future__ import annotations

import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai


class GeminiClient:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY tanımlı değil.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest"))

    def summarize_video(self, transcript: str, compress_ratio: int, title: str, author: str) -> dict:
        prompt = (
            "Aşağıdaki transcript'i belirtilen sıkıştırma oranıyla Türkçe özetle. "
            "Özet, anlatıcının tonunu ve konuşmanın ruhunu korumalı. "
            "Önce tek cümlelik ana konu özetini ver, sonra detaylı özeti yaz. "
            "Detaylar kaybolmamalı.\n\n"
            f"Video başlığı: {title}\n"
            f"Kanal: {author}\n"
            f"Sıkıştırma oranı: %{compress_ratio}\n\n"
            "Çıktıyı şu formatta ver:\n"
            "Ana konu: <cümle>\n"
            "Özet: <metin>\n\n"
            f"Transcript:\n{transcript}"
        )
        response = self.model.generate_content(prompt)
        text = response.text or ""
        return self._parse_summary(text)

    def build_podcast_script(self, summaries: list) -> str:
        summary_blocks = []
        for item in summaries:
            summary_blocks.append(
                "\n".join(
                    [
                        f"Video: {item.title}",
                        f"Kanal: {item.author}",
                        f"Ana konu: {item.topic_sentence}",
                        item.summary_text,
                    ]
                )
            )

        prompt = (
            "Aşağıdaki özetleri tek bir podcast bülteni metnine dönüştür. "
            "Anlatı akıcı olmalı, geçişlerde sunucu dili kullan. "
            "Örnek: 'Nevşin Mengü'den günün yorumuna geçiyoruz...' "
            "Her bölümün başında video ve kanal bilgisini kısa bir girişle an. "
            "Türkçe ve seslendirmeye uygun yaz.\n\n"
            f"Özetler:\n{'\n\n'.join(summary_blocks)}"
        )
        response = self.model.generate_content(prompt)
        return response.text or ""

    def _parse_summary(self, text: str) -> dict:
        topic_sentence = ""
        summary_text = text
        for line in text.splitlines():
            if line.lower().startswith("ana konu"):
                topic_sentence = line.split(":", 1)[-1].strip()
            if line.lower().startswith("özet"):
                summary_text = line.split(":", 1)[-1].strip()
        if not topic_sentence:
            topic_sentence = "Ana konu tespit edilemedi."
        return {"topic_sentence": topic_sentence, "summary_text": summary_text}
