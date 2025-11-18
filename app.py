# ---------------------------------------------------
# File Name: app.py
# Author: NeonAnurag
# GitHub: https://github.com/MyselfNeon/
# Telegram: https://t.me/MyelfNeon
# Created: 2025-11-21
# Last Modified: 2025-11-22
# Version: Latest
# License: MIT License
# ---------------------------------------------------

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>@MyselfNeon</title>
  <style>
    body {
      background-color: black;
      margin: 0;
      height: 100vh;
      font-family: 'Brush Script MT', cursive;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: center;
      text-align: center;
      overflow: hidden;
      padding-top: 20vh;
    }

    /* Added avatar + neon cyan glow */
    .avatar {
      width: 150px;
      height: 150px;
      border-radius: 50%;
      margin-bottom: 25px;
      box-shadow:
        0 0 8px #00eaff,
        0 0 15px #00eaff,
        0 0 30px #00eaff;
    }

    a {
      text-decoration: none;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: auto;
      width: 100%;
      cursor: pointer;
    }

    h1 {
      font-size: clamp(2.5rem, 8vw, 7rem);
      letter-spacing: 2px;
      margin-bottom: 0.3rem;
      animation: redToBlue 2s infinite alternate ease-in-out;
      text-shadow:
        0 0 1px currentColor,
        0 0 3px currentColor;
    }

    h2 {
      font-size: clamp(1.8rem, 6vw, 4.8rem);
      letter-spacing: 2px;
      color: #39FF14;
      text-shadow:
        0 0 1px #39FF14,
        0 0 3px #00FF00;
    }

    @keyframes redToBlue {
      0% { color: #FF2400; }
      50% { color: #FF1493; }
      100% { color: #00BFFF; }
    }
  </style>
</head>
<body>

  <!-- Added avatar -->
  <img class="avatar" src="https://avatars.githubusercontent.com/u/194442566?v=4">

  <a href="https://t.me/NeonSessionBot" target="_blank">
    <h1>SessionGenerator-Bot</h1>
    <h2>Coded By @MyselfNeon</h2>
  </a>

</body>
</html>
    """

if __name__ == "__main__":
    app.run()


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
