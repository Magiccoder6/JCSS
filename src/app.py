from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def signin():
    return render_template("auth-signin.html")

if __name__ == "__main__":
    app.run(debug=True)