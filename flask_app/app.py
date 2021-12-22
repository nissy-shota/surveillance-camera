from flask import Flask, render_template, request, redirect, session, url_for, make_response
import subprocess

app = Flask(__name__)

@app.route("/")#url
def top():
    return render_template("top.html")

@app.route("/check")
def check():
    cp = subprocess.Popen(["python", "test.py"])
    return render_template("check.html")

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=8888) # ポートの変更