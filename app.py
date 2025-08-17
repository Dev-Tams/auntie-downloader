from flask import Flask, request, redirect, render_template_string
import yt_dlp

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Auntie Downloader</title>
<style>
    body {
        font-family: 'Helvetica', sans-serif;
        background-color: #f9f9f9;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .container {
        background: #fff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 90%;
        max-width: 400px;
        text-align: center;
    }
    h1 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #333;
    }
    input[type="text"] {
        width: 100%;
        padding: 0.75rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        font-size: 1rem;
    }
    button {
        padding: 0.75rem 1rem;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
    }
    button:hover {
        background: #0056b3;
    }
    .note {
        margin-top: 1rem;
        font-size: 0.85rem;
        color: #666;
    }
</style>
</head>
<body>
<div class="container">
    <h1>Auntie Downloader</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Paste video URL here" required>
        <button type="submit">Download</button>
    </form>
    <div class="note">Supports public videos from Vimeo & YouTube shorts (no login required).</div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        ydl_opts = {"format": "best", "quiet": True, "skip_download": True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video_url = info["url"]
            return redirect(video_url)
        except Exception as e:
            return f"<h2>Error: {e}</h2><p><a href='/'>Go back</a></p>"

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
