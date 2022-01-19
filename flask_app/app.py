from flask import Flask, render_template, request, redirect, session, url_for, make_response
import subprocess

app = Flask(__name__)

@app.route("/")#url
def top():
    return render_template("top.html")

@app.route("/capture_akaze")
def capture_akaze():
    cp = subprocess.Popen(["python", "main.py"])
    return render_template("capture.html")

@app.route("/capture_deep")
def capture_deep():
    cp = subprocess.Popen(["python", "main.py", "--deep"])
    return render_template("capture.html")

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=8888) # ポートの変更