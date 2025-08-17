import datetime
from flask import Flask, request, send_file, render_template_string
import yt_dlp
import os
import uuid

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Auntie's Downloader</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f8f9fa;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .container {
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      text-align: center;
      width: 90%;
      max-width: 400px;
    }
    h2 {
      margin-bottom: 20px;
      color: #333;
    }
    input[type="text"] {
      width: 100%;
      padding: 10px;
      border-radius: 6px;
      border: 1px solid #ccc;
      margin-bottom: 15px;
    }
    button {
      background: #007bff;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 6px;
      cursor: pointer;
    }
    button:hover {
      background: #0056b3;
    }
    label {
      margin-right: 10px;
    }
  </style>
  <script>
    function showLoading(btn) {
      btn.innerText = "Downloading...";
      btn.disabled = true;
      btn.form.submit();
    }
  </script>
</head>
<body>
  <div class="container">
    <h2>Auntie's Video Downloader</h2>
    <form method="POST">
      <input type="text" name="url" placeholder="Paste video link here"><br>
      <label><input type="radio" name="type" value="video" checked> Video</label>
      <label><input type="radio" name="type" value="audio"> Audio (MP3)</label><br><br>
      <button type="button" onclick="showLoading(this)">Download</button>
    </form>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        media_type = request.form["type"]
        user_ip = request.remote_addr  # Capture client IP

        # Log with IP
        print(f"[{datetime.datetime.now()}] {user_ip} requested {media_type.upper()} from {url}")
        tmp_filename = f"{uuid.uuid4()}.%(ext)s"
        

        ydl_opts = {
            "outtmpl": tmp_filename,
        }

        if media_type == "audio":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            })
        else:
            ydl_opts.update({"format": "best"})

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return send_file(filename, as_attachment=True)

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
