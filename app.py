from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aarambh Class 10th</title>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
</head>
<body>
    <h2>Aarambh Class 10th By Team flower (Live / Recorded support)</h2>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter .m3u8 URL" required style="width: 400px;"><br><br>
        <input type="text" name="quality" placeholder="Optional Quality (e.g., 240, 360)"><br><br>
        <button type="submit">Play</button>
    </form>

    {% if video_url %}
        <hr>
        <video id="video" controls width="640" height="360"></video>
        <script>
            var video = document.getElementById('video');
            if(Hls.isSupported()) {
                var hls = new Hls();
                hls.loadSource("{{ video_url }}");
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED,function() {
                    video.play();
                });
            }
            else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = "{{ video_url }}";
                video.addEventListener('loadedmetadata',function() {
                    video.play();
                });
            }
        </script>
        <p><b>Playing:</b> {{ video_url }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = ''
    if request.method == 'POST':
        raw_url = request.form['url'].strip()
        quality = request.form.get('quality', '').strip()

        if quality:
            # Try to convert to quality-based URL
            try:
                base_url = raw_url.rsplit('/', 1)[0]
                filename = raw_url.split('/')[-1]
                new_filename = f"{quality}p30.m3u8"
                video_url = f"{base_url}/{new_filename}"
            except Exception:
                video_url = raw_url
        else:
            # Use the raw input URL as-is
            video_url = raw_url

    return render_template_string(HTML, video_url=video_url)

if __name__ == '__main__':
    app.run(debug=True)
	
