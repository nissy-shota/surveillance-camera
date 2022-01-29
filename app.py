from flask import Flask, render_template, request, redirect, session, url_for, make_response
import subprocess

app = Flask(__name__)
cp = None

@app.route("/")#url
def top():
    return render_template("top.html")

@app.route("/capture_akaze")
def capture_akaze():
    cp = subprocess.Popen(["python", "main.py"],shell=False)
    return render_template("capture.html")

@app.route("/capture_deep")
def capture_deep():
    cp = subprocess.Popen(["python", "main.py", "--deep"],shell=False)
    return render_template("capture.html")

@app.route("/capture_back_image")
def capture_back():
    cp = subprocess.Popen(["python", "update_back_image.py"])
    return render_template("top.html")

@app.route("/return_top")
def return_top():
    cp = subprocess.Popen(["pkill", "python", "main.py"], shell=False)
    cp = subprocess.Popen(["pkill", "python", "main.py", "--deep"], shell=False)
    return render_template("top.html")

if __name__ == '__main__':
    app.run(debug=True,  host='0.0.0.0', port=8888) # ポートの変更