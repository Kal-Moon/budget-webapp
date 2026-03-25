from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "가계부 앱 시작!"

@app.route("/about")
def introduce():
    return "자기소개"

@app.route("/stats")
def stats():
    return "통계"

@app.route("/settings")
def settings():
    return "설정"

if __name__ == "__main__":
    app.run(debug=True) 