from flask import Flask, request, render_template_string, redirect, url_for, Response
from functools import wraps

app = Flask(__name__)

# Basic Auth Credentials
USERNAME = "admin"
PASSWORD = "password"

# In-memory Video Data
videos = {
    "1": {
        "title": "Sample Lecture",
        "url": "https://stream.pwjarvis.app/<your-token>/hls/720/main.m3u8",
        "attachments": {
            "Notes": "https://example.com/notes.pdf",
            "DPP": "https://example.com/dpp.pdf"
        }
    }
}

# HTML Templates
VIDEO_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
  <style>
    body { background: #000; color: white; margin: 0; font-family: sans-serif; }
    h1 { text-align: center; padding: 10px 0; font-size: 22px; }
    .video-js { width: 90vw; max-width: 1000px; height: 50vw; max-height: 562px; margin: auto; }
    .controls { margin-top: 10px; display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
    button, select { background: #222; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-size: 16px; cursor: pointer; }
    select { background: #333; }
    .attachments { text-align: center; margin-top: 10px; }
    .attachments button { margin: 0 5px; }
  </style>
</head>
<body oncontextmenu="return false" onkeydown="return false">
  <h1>{{ title }}</h1>
  <video-js id="player" class="video-js vjs-default-skin" controls preload="auto"></video-js>

  <div class="controls">
    <button id="backwardBtn">⏪ 10s</button>
    <button id="speedBtn">Speed: 1x</button>
    <button id="forwardBtn">⏩ 10s</button>
    <select id="qualitySelect">
      <option value="240">240p</option>
      <option value="360">360p</option>
      <option value="480">480p</option>
      <option value="720">720p</option>
    </select>
  </div>

  {% if attachments %}
  <div class="attachments">
    {% for name, link in attachments.items() %}
      <button onclick="window.open('{{ link }}', '_blank')">{{ name }}</button>
    {% endfor %}
  </div>
  {% endif %}

  <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
  <script>
    const player = videojs('player');
    const speedBtn = document.getElementById('speedBtn');
    const forwardBtn = document.getElementById('forwardBtn');
    const backwardBtn = document.getElementById('backwardBtn');
    const qualitySelect = document.getElementById('qualitySelect');
    const baseUrl = '{{ url }}'.replace(/\d{3,4}\/main.m3u8/, '');
    const videoId = '{{ id }}';

    const speeds = [1, 1.5, 2];
    let speedIndex = 0;

    function loadVideo() {
      const quality = qualitySelect.value;
      const finalUrl = `${baseUrl}${quality}/main.m3u8`;
      player.src({ src: finalUrl, type: 'application/x-mpegURL' });
      player.ready(function () {
        player.one('loadedmetadata', function () {
          player.currentTime(14);
        });
        player.play();
      });
    }

    qualitySelect.addEventListener('change', loadVideo);
    speedBtn.addEventListener('click', () => {
      speedIndex = (speedIndex + 1) % speeds.length;
      player.playbackRate(speeds[speedIndex]);
      speedBtn.textContent = 'Speed: ' + speeds[speedIndex] + 'x';
    });
    forwardBtn.addEventListener('click', () => player.currentTime(player.currentTime() + 10));
    backwardBtn.addEventListener('click', () => {
      const newTime = player.currentTime() - 10;
      player.currentTime(newTime < 14 ? 14 : newTime);
    });

    player.on('seeking', function () {
      if (player.currentTime() < 14) player.currentTime(14);
    });

    loadVideo();
  </script>
</body>
</html>
"""

# Auth Decorator
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Login Required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route("/admin", methods=["GET", "POST"])
@requires_auth
def admin():
    if request.method == "POST":
        id = request.form["id"]
        title = request.form["title"]
        url = request.form["url"]
        attachments = {}
        if request.form.get("notes"): attachments["Notes"] = request.form.get("notes")
        if request.form.get("dpp"): attachments["DPP"] = request.form.get("dpp")
        if request.form.get("handwritten"): attachments["Handwritten Notes"] = request.form.get("handwritten")
        videos[id] = {"title": title, "url": url, "attachments": attachments}
    html = """
    <form method="POST">
      ID: <input name="id"><br>
      Title: <input name="title"><br>
      Video URL: <input name="url"><br>
      Notes URL: <input name="notes"><br>
      DPP URL: <input name="dpp"><br>
      Handwritten Notes URL: <input name="handwritten"><br>
      <button type="submit">Save</button>
    </form>
    <hr>
    <h3>Saved Videos:</h3>
    <ul>
      {% for vid, data in videos.items() %}
        <li><a href="/video/{{ vid }}" target="_blank">{{ vid }}: {{ data.title }}</a></li>
      {% endfor %}
    </ul>
    """
    return render_template_string(html, videos=videos)

@app.route("/video/<id>")
def video(id):
    video = videos.get(id)
    if not video:
        return "Invalid ID", 404
    title = video["title"]
    attachments = video.get("attachments", {})
    return render_template_string(VIDEO_TEMPLATE, id=id, title=title, attachments=attachments, url=video["url"])

if __name__ == "__main__":
    app.run(debug=True)
	
