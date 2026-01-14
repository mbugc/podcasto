const playlistInput = document.getElementById("playlist");
const compressInput = document.getElementById("compress");
const compressValue = document.getElementById("compress-value");
const runButton = document.getElementById("run");
const status = document.getElementById("status");
const summaryList = document.getElementById("summary-list");
const podcastScript = document.getElementById("podcast-script");
const audioElement = document.getElementById("audio");

compressInput.addEventListener("input", () => {
  compressValue.textContent = `%${compressInput.value}`;
});

runButton.addEventListener("click", async () => {
  const playlistUrl = playlistInput.value.trim();
  if (!playlistUrl) {
    status.textContent = "Lütfen bir playlist URL girin.";
    return;
  }

  status.textContent = "Özetler hazırlanıyor...";
  runButton.disabled = true;
  summaryList.innerHTML = "";
  podcastScript.textContent = "";
  audioElement.removeAttribute("src");

  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        playlist_url: playlistUrl,
        compress_ratio: Number(compressInput.value),
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "İşlem başarısız oldu.");
    }

    const data = await response.json();
    data.summary_files.forEach((path) => {
      const item = document.createElement("li");
      item.textContent = path;
      summaryList.appendChild(item);
    });
    podcastScript.textContent = data.podcast_script;

    if (data.audio_file) {
      audioElement.src = `/api/audio/${data.playlist_id}`;
    }

    status.textContent = "Tamamlandı!";
  } catch (error) {
    status.textContent = error.message;
  } finally {
    runButton.disabled = false;
  }
});
