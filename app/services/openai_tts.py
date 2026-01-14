from __future__ import annotations

import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI


class OpenAITTSClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.voice = os.getenv("OPENAI_TTS_VOICE", "alloy")
        self.model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
        self._client = OpenAI(api_key=self.api_key) if self.api_key else None

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    def synthesize(self, text: str) -> bytes:
        if not self._client:
            raise RuntimeError("OPENAI_API_KEY tanımlı değil.")
        response = self._client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
            format="mp3",
        )
        return response.read()
