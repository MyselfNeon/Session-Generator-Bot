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
    <body style="background-color:black; color:#39FF14; display:flex; justify-content:center; align-items:flex-start; height:100vh; margin:0; font-family:sans-serif; padding-top:20vh; font-size:4rem;">
        Coded By @MyselfNeon
    </body>
    """

if __name__ == "__main__":
    app.run()


# MyselfNeon
# Don't Remove Credit 🥺
# Telegram Channel @NeonFiles
