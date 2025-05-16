from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>HLS Player</title>
  <link href="https://unpkg.com/video.js/dist/video-js.css" rel="stylesheet" />
  <style>
    html, body { margin: 0; padding: 0; height: 100%; background: #000; overflow: hidden; }
    .player-container { position: relative; width: 100%; height: 100%; background: #000; }
    video { width: 100%; height: 100%; object-fit: contain; background: #000; }
    .controls {
      position: absolute; bottom: 20px; left: 50%;
      transform: translateX(-50%);
      z-index: 1000; display: flex; gap: 10px;
      background: rgba(0, 0, 0, 0.5);
      padding: 10px 15px; border-radius: 10px;
    }
    .controls button, .controls select {
      padding: 6px 12px; font-size: 14px;
      background: #222; color: #fff;
      border: none; border-radius: 5px; cursor: pointer;
    }
    .controls button:hover, .controls select:hover {
      background: #444;
    }
  </style>
</head>
<body>

<div class="player-container">
  <video id="video" controls></video>

  <div class="controls">
    <button onclick="seekBackward()">⏪ 10s</button>
    <button onclick="seekForward()">10s ⏩</button>
    <select id="speed" onchange="changeSpeed(this.value)">
      <option value="0.5">0.5x</option>
      <option value="1" selected>1x</option>
      <option value="1.5">1.5x</option>
      <option value="2">2x</option>
    </select>
    <button onclick="goLive()">🔴 Go Live</button>
    <select id="qualitySelect"></select>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
<script>
  const video = document.getElementById('video');
  const qualitySelect = document.getElementById('qualitySelect');
  const urlParams = new URLSearchParams(window.location.search);
  const videoSrc = urlParams.get("url");

  if (!videoSrc) {
    alert("No video URL provided in query (?url=...)");
  }

  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);

    hls.on(Hls.Events.MANIFEST_PARSED, function () {
      video.play();

      hls.levels.forEach((level, i) => {
        const option = document.createElement('option');
        option.value = i;
        option.text = `${level.height}p`;
        qualitySelect.appendChild(option);
      });

      qualitySelect.onchange = function () {
        hls.currentLevel = parseInt(this.value);
      };
    });
  } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = videoSrc;
    video.addEventListener('loadedmetadata', function () {
      video.play();
    });
  }

  function seekBackward() { video.currentTime -= 10; }
  function seekForward() { video.currentTime += 10; }
  function changeSpeed(rate) { video.playbackRate = parseFloat(rate); }
  function goLive() { video.currentTime = video.duration; }
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
	
