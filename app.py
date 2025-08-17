from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_PAGE = """
<form method="POST">
    Video URL: <input type="text" name="url">
    <input type="submit" value="Download">
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return "No URL provided", 400

        # Extract best video URL (without downloading)
        with yt_dlp.YoutubeDL({"format": "best"}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info["url"]

        # Redirect the user's browser directly to YouTube's CDN URL
        return redirect(video_url)

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
