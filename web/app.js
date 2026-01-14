const form = document.getElementById("playlist-form");
const ratioInput = document.getElementById("ratio");
const ratioValue = document.getElementById("ratio-value");
const summaryCount = document.getElementById("summary-count");
const scriptPath = document.getElementById("script-path");
const audioPath = document.getElementById("audio-path");

function updateRatioLabel(value) {
  ratioValue.textContent = `%${value}`;
}

ratioInput.addEventListener("input", (event) => {
  updateRatioLabel(event.target.value);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  summaryCount.textContent = "Özetleme yapılıyor...";
  scriptPath.textContent = "";
  audioPath.textContent = "";

  const playlistUrl = form.elements.playlist_url.value;
  const compressionRatio = Number(ratioInput.value) / 100;

  try {
    const response = await fetch("/api/summarize", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        playlist_url: playlistUrl,
        compression_ratio: compressionRatio,
      }),
    });

    if (!response.ok) {
      const payload = await response.json();
      throw new Error(payload.detail || "Özetleme sırasında hata oluştu.");
    }

    const data = await response.json();
    summaryCount.textContent = `${data.summary_count} video özeti kaydedildi.`;
    scriptPath.textContent = `Podcast metni: ${data.podcast_script_path}`;
    audioPath.textContent = `Ses dosyası (placeholder): ${data.audio_path}`;
  } catch (error) {
    summaryCount.textContent = `Hata: ${error.message}`;
  }
});

updateRatioLabel(ratioInput.value);
