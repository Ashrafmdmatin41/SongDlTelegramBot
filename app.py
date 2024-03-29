from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("home.html")

if __name__ == "__maain__":
    app.run(debug=True)