from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from boston_parser import tree_parser
from graph_builder import build_routing_graph, calculate_distance
from run_dijkstra import dijkstra
import os, redis, openai, json

app = Flask(__name__)
redis_client = redis.Redis(host="localhost", port=6379, db=0)
load_dotenv()

print("Loading map data...")
nodes, ways, addresses = tree_parser()
routing_graph, intersections = build_routing_graph(nodes, ways)
print("Map data loaded")

@app.route("/checkPoints", methods=['POST'])
def check_points():
    data = request.get_json()

    from_address = data["from"].lower()
    to_address = data["to"].lower()
    print(f'from address sent: {from_address}')
    print(f'to address sent: {to_address}')

    if from_address not in addresses or to_address not in addresses:
        return jsonify({'error': 'Store not found'}), 404
    
    return jsonify({
        'from_stores': addresses[from_address],
        'to_stores': addresses[to_address],
    })

@app.route("/findRoute", methods=['POST'])
def find_route():
    coord_data = request.get_json()
    from_coord = coord_data["from_coords"]
    to_coord = coord_data["to_coords"]

    from_node = find_nearest_intersection(from_coord, intersections)
    to_node = find_nearest_intersection(to_coord, intersections)

    print("From node:", from_node, intersections[from_node])
    print("To node:", to_node, intersections[to_node])
    print("From neighbors:", routing_graph.get(from_node, {}))
    print("To neighbors:", routing_graph.get(to_node, {}))
    print(f'finding route...')

    route = dijkstra(from_node, to_node, routing_graph)
    print(f'route found: {route}')
    return jsonify({'route': route})

def find_nearest_intersection(coord, intersections):
    min_distance = float('inf')
    nearest_node = None

    for node_id, node_data in intersections.items():
        distance = calculate_distance(coord, node_data['coord'])
        if distance < min_distance:
            min_distance = distance
            nearest_node = node_id

    return nearest_node

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