from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Aarambh Live By Team Flower</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
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
    #speedBtn {
      margin-top: 10px;
      background: #222;
      color: #fff;
      border: none;
      padding: 10px 20px;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    #qualitySelect {
      margin-top: 10px;
      font-size: 16px;
      padding: 5px 10px;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <video-js id="player" class="video-js vjs-default-skin" controls preload="auto"></video-js>

  <select id="qualitySelect">
    <option value="1">Quality 1 (Low)</option>
    <option value="2">Quality 2 (Medium)</option>
    <option value="3">Quality 3 (High)</option>
  </select>

  <button id="speedBtn">Speed: 1x</button>

  <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
  <script>
    const player = videojs('player');
    const speedBtn = document.getElementById('speedBtn');
    const qualitySelect = document.getElementById('qualitySelect');

    const baseUrl = "{{ url }}";
    if (!baseUrl) {
      alert("No video URL provided in query param `url`");
    }

    const speeds = [1, 1.5, 2];
    let speedIndex = 0;

    function getQualityUrl(base, q) {
      // Replace index.m3u8 with index_q.m3u8
      return base.replace('index.m3u8', `index_${q}.m3u8`);
    }

    function loadVideo() {
      const q = qualitySelect.value;
      const finalUrl = getQualityUrl(baseUrl, q);
      player.src({ src: finalUrl, type: 'application/x-mpegURL' });
      player.play();
    }

    qualitySelect.addEventListener('change', () => {
      loadVideo();
    });

    speedBtn.addEventListener('click', () => {
      speedIndex = (speedIndex + 1) % speeds.length;
      player.playbackRate(speeds[speedIndex]);
      speedBtn.textContent = 'Speed: ' + speeds[speedIndex] + 'x';
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
	
