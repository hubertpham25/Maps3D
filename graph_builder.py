from boston_parser import tree_parser, nodes, ways
import math

def build_routing_graph():
    intersections = dict()
    for node_id, node_data in nodes.items():
        if len(nodes['ways']) > 1:
            intersections[node_id] = node_data

    

def time_weight(coord_distance, maxspeed):
