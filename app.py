from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<title>Video Downloader</title>
<h1>Enter video URL</h1>
<form method=post>
  <input type=text name=url placeholder="Video URL" required>
  <input type=submit value=Download>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        try:
            # Extract video info but don't download
            with yt_dlp.YoutubeDL({"format": "best"}) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info.get("url")
                if not video_url:
                    return "Error: Could not get video URL", 400

            # Redirect the user directly to the video
            return redirect(video_url)

        except Exception as e:
            return f"Error: {str(e)}", 400

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
