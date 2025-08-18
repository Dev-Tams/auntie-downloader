from flask import Flask, request, redirect, render_template_string, send_file, after_this_request
import yt_dlp
import tempfile
import os
app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auntie Downloader</title>
<style>
    body { font-family: 'Helvetica', sans-serif; background-color: #f9f9f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin:0; }
    .container { background: #fff; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 90%; max-width: 400px; text-align: center; }
    h1 { font-size: 1.5rem; margin-bottom: 1rem; color: #333; }
    input[type="text"] { width: 100%; padding: 0.75rem; margin-bottom: 1rem; border-radius: 0.5rem; border: 1px solid #ddd; font-size: 1rem; }
    button { padding: 0.75rem 1rem; background: #007bff; color: white; border: none; border-radius: 0.5rem; font-size: 1rem; cursor: pointer; width: 100%; }
    button:hover { background: #0056b3; }
    .note { margin-top: 1rem; font-size: 0.85rem; color: #666; }
</style>
</head>
<body>
<div class="container">
    <h1>Auntie Downloader</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Paste video URL here" required>
        <button type="submit">Download</button>
    </form>
    <div class="note">Supports public and private YouTube videos (login required).</div>
</div>
</body>
</html>
"""
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "<h2>No URL provided</h2><p><a href='/'>Go back</a></p>"

        cookies_content = os.getenv("YOUTUBE_COOKIES")
        if not cookies_content:
            return "<h2>Server error: cookies not set</h2>"

        # create temp files for video and cookies
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.close()  # close so yt_dlp can write to it
        temp_cookie = tempfile.NamedTemporaryFile(delete=False)
        temp_cookie.write(cookies_content.encode())
        temp_cookie.close()

        try:
            ydl_opts = {
                "quiet": True,
                "format": "bestvideo+bestaudio/best",
                "outtmpl": temp_video.name,
                "merge_output_format": "mp4",
                "cookiefile": temp_cookie.name
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # stream the file to user
            return redirect(f"/download/{os.path.basename(temp_video.name)}")

        except Exception as e:
            return f"<h2>Error: {e}</h2><p><a href='/'>Go back</a></p>"

        finally:
            # delete cookie file immediately
            try:
                os.remove(temp_cookie.name)
            except:
                pass

    return render_template_string(HTML_PAGE)


# serve the temp video and delete after sending
@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(tempfile.gettempdir(), filename)
    if not os.path.exists(path):
        return "<h2>File not found</h2>"

    from flask import send_file
    response = send_file(path, as_attachment=True)
    # delete file after sending
    try:
        os.remove(path)
    except:
        pass
    return response
