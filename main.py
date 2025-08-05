from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"msg": "Hello World"})

if __name__ == "__main__":
    app.run(debug=True)