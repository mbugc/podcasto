# Podcasto

Youtube oynatma listelerinden günlük özet podcast akışı için iskelet uygulama.

## Özellikler

- Playlist URL girip sıkıştırma oranını seçebileceğiniz web arayüzü.
- Her video için özet TXT dosyası oluşturma.
- Özetleri bülten metnine dönüştürme ve tek bir dosyada birleştirme.
- TTS adımı için placeholder çıktı.

> Not: Bu sürüm, YouTube ve Gemini/OpenAI entegrasyonlarını demo verilerle temsil eder.
> API anahtarları eklendiğinde `app/pipeline.py` içindeki TODO adımlarını gerçek
> servis çağrılarına bağlayabilirsiniz.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
uvicorn app.main:app --reload
```

Ardından tarayıcıda `http://localhost:8000` adresini açın.

## Üretilen Dosyalar

- `outputs/summaries/` → Her video için TXT özet.
- `outputs/podcasts/` → Playlist bazlı bülten metni.
- `outputs/audio/` → TTS çıktısı (şimdilik placeholder).
