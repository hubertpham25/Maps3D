from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from boston_parser import tree_parser
# from graph_builder import build_routing_graph
import os, redis, openai, json

app = Flask(__name__)
load_dotenv()

# print("Loading map data...")
nodes, ways, addresses = tree_parser()
# routing_graph = build_routing_graph(nodes, ways)
# print("Map data loaded")
@app.route("/checkPoints", methods=['POST'])
def check_points():
    data = request.get_json()

    from_address = data["from"]
    to_address = data["to"]

    if from_address not in addresses or to_address not in addresses:
        return jsonify({'error': 'Store not found'}), 404
    
    return jsonify({
        'from_stores': addresses[from_address],
        'to_stores': addresses[to_address],
    })

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