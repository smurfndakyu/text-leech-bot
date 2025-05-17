from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title> Aarambh Batch Class 10th By Team Flower</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
  <style>
    body {
      margin: 0;
      background: #000;
      color: white;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
    }
    .video-js {
      width: 80vw;
      max-width: 900px;
      height: 45vw;
      max-height: 506px;
    }
    .controls {
      margin-top: 10px;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
    }
    button, select {
      background: #222;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
    }
    select {
      background: #333;
    }
    .watermark {
      position: absolute;
      bottom: 60px;
      right: 20px;
      color: rgba(255, 255, 255, 0.8);
      font-size: 16px;
      font-weight: bold;
      background: rgba(0, 0, 0, 0.4);
      padding: 4px 10px;
      border-radius: 4px;
      pointer-events: none;
    }
    .player-container {
      position: relative;
      width: 80vw;
      max-width: 900px;
    }
  </style>
</head>
<body>
  <div class="player-container">
    <video-js id="player" class="video-js vjs-default-skin" controls preload="auto"></video-js>
    <div class="watermark">Powered by Team Flower Dm @Teamflowersupportfree_bot </div>
  </div>

  <div class="controls">
    <button id="backwardBtn">⏪ 10s</button>
    <button id="speedBtn">Speed: 1x</button>
    <button id="forwardBtn">⏩ 10s</button>
    <select id="qualitySelect">
      <option value="1">240p</option>
      <option value="2">360p</option>
      <option value="3">480p</option>
      <option value="5">720p</option>
    </select>
  </div>

  <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
  <script>
    const player = videojs('player');
    const speedBtn = document.getElementById('speedBtn');
    const forwardBtn = document.getElementById('forwardBtn');
    const backwardBtn = document.getElementById('backwardBtn');
    const qualitySelect = document.getElementById('qualitySelect');

    const baseUrl = "{{ url }}";
    if (!baseUrl) {
      alert("No video URL provided via ?url=");
    }

    const speeds = [1, 1.5, 2];
    let speedIndex = 0;

    function getQualityUrl(base, q) {
      return base.replace('index.m3u8', `index_${q}.m3u8`);
    }

    function loadVideo() {
      const q = qualitySelect.value;
      const finalUrl = getQualityUrl(baseUrl, q);
      player.src({ src: finalUrl, type: 'application/x-mpegURL' });
      player.play();
    }

    qualitySelect.addEventListener('change', loadVideo);

    speedBtn.addEventListener('click', () => {
      speedIndex = (speedIndex + 1) % speeds.length;
      player.playbackRate(speeds[speedIndex]);
      speedBtn.textContent = 'Speed: ' + speeds[speedIndex] + 'x';
    });

    forwardBtn.addEventListener('click', () => {
      player.currentTime(player.currentTime() + 10);
    });

    backwardBtn.addEventListener('click', () => {
      player.currentTime(player.currentTime() - 10);
    });

    loadVideo();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    url = request.args.get("url", "")
    return render_template_string(HTML, url=url)

if __name__ == "__main__":
    app.run(debug=True)
	
