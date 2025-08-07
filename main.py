from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os, redis, openai, json

app = Flask(__name__)
load_dotenv()

# client = OpenAI(api_key=os.getenv("openai_key"))

@app.route("/askAi")
def ask_ai():
    #loads askAi.html
    return render_template("askAi.html")

@app.route("/")
def index():
    cesium_token = os.getenv("ces_token") #grabs cesium token from .env

    #checks if token loads
    if cesium_token:
        print("Cesium Token Loaded")
    else: 
        print("Cesium Token not loaded")
    return render_template("index.html", cesium_token=cesium_token)

if __name__ == "__main__":
    app.run(debug=True)