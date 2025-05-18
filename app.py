from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title> Aarambh Batch Class 10th By Team Flower</title>
  <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
  <style>
    body { font-family: sans-serif; text-align: center; background: #f9f9f9; }
    video { width: 90%; max-width: 700px; margin-top: 20px; border: 1px solid #ccc; }
    .buttons { margin: 20px; }
    button { padding: 8px 16px; margin: 5px; font-size: 16px; }
  </style>
</head>
<body>

<h2>Aarambh Batch Class 10th Powered By Team Flower</h2>

<video id="video" controls></video>

<div class="buttons">
  <button onclick="changeQuality('240')">240p</button>
  <button onclick="changeQuality('360')">360p</button>
  <button onclick="changeQuality('480')">480p</button>
  <button onclick="changeQuality('720')">720p</button>
</div>

<script>
  const video = document.getElementById('video');
  let hls;

  const baseURL = "{{ base_url }}";
  const startQuality = "{{ quality }}";
  const ext = "{{ suffix }}";

  function playStream(url) {
    if (hls) {
      hls.destroy();
    }

    hls = new Hls();
    hls.loadSource(url);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function() {
      video.play();
    });
  }

  function changeQuality(q) {
    const newUrl = `${baseURL}/${q}${ext}`;
    playStream(newUrl);
  }

  // Auto-play on page load
  window.onload = function() {
    const initialUrl = `${baseURL}/${startQuality}${ext}`;
    playStream(initialUrl);
  };
</script>

</body>
</html>
'''

@app.route('/')
def index():
    full_url = request.args.get('url', '').strip()
    quality = request.args.get('quality', '360').strip()

    if not full_url:
        return "❌ URL not provided. Use ?url=...&quality=360"

    try:
        base_url = full_url.rsplit('/', 1)[0]
        suffix = full_url.rsplit('/', 1)[-1].replace(quality, '{quality}')
        suffix = suffix.replace('{quality}', '')  # remove quality, keep postfix like "p30.m3u8"
    except Exception:
        return "❌ Invalid URL format"

    return render_template_string(HTML, base_url=base_url, quality=quality, suffix=suffix)

if __name__ == '__main__':
    app.run(debug=True)
	
