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
