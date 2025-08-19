from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from boston_parser import tree_parser
# from graph_builder import build_routing_graph
import os, redis, openai, json

app = Flask(__name__)
load_dotenv()

# print("Loading map data...")
nodes, ways, stores = tree_parser()
# routing_graph = build_routing_graph(nodes, ways)
# print("Map data loaded")
@app.route("/checkPoints", methods=['POST'])
def check_points():
    data = request.get_json()

    from_store = data["from"]
    to_store = data["to"]

    if from_store not in stores or to_store not in stores:
        return jsonify({'error': 'Store not found'}), 404
    
    return jsonify({
        'From stores': stores[from_store]["locations"],
        'To stores': stores[to_store]["locations"],
        'Message': 'Multiple locations found. Please choose one.'
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