# Podcasto

YouTube oynatma listelerini özetleyip podcast bültenine dönüştüren basit bir demo.

## Özellikler
- Playlist URL + sıkıştırma oranı seçimi (%10-%90)
- Her video için transcript + Gemini özeti
- Özetleri TXT olarak kaydetme
- Özetleri tek bir podcast bülten metnine dönüştürme
- (Opsiyonel) OpenAI TTS ile ses dosyası üretme

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ortam Değişkenleri

```bash
export GEMINI_API_KEY=...
export GEMINI_MODEL=gemini-1.5-pro-latest
export OPENAI_API_KEY=...
export OPENAI_TTS_MODEL=gpt-4o-mini-tts
export OPENAI_TTS_VOICE=alloy
```

## Çalıştırma

```bash
uvicorn app.main:app --reload
```

Ardından tarayıcıda `http://localhost:8000`.

## Çıktılar

- `output/summaries/<video_id>.txt`
- `output/podcasts/<playlist_id>.txt`
- `output/audio/<playlist_id>.mp3`
