from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def introduce():
    return "자기소개"

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")  

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

if __name__ == "__main__":
    app.run(debug=True) 