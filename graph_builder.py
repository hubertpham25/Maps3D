import math

def build_routing_graph(nodes, ways):
    intersections = dict()
    for node_id, node_data in nodes.items():
        if len(node_data['ways']) > 1:
            intersections[node_id] = node_data

    graph = dict()

    for intersection_id in intersections:
        graph[intersection_id] = dict()    

    for way_id, way_data in ways:
        if 'highway' not in way_data['tags']:
            continue
        
        if 'maxspeed' not in way_data['tags']:
            maxspeed = 25

        else: 
            maxspeed = int(way_data['tags']['maxspeed'].strip('mmph'))

        way_nodes = way_data['nodes']
        way_intersections = list()
        for way_node in way_nodes:
            if way_node in intersections:
                way_intersections.append(way_node)
        
        for i in range(len(intersections) - 1):
            from_node = way_intersections[i]
            to_node = way_intersections[i + 1]
            
            from_coord = intersections[from_node]['coord']
            to_coord = intersections[to_node]['coord']
            distance = calculate_distance(from_coord, to_coord)
            travel_time = time_weight(distance, maxspeed)

            graph[from_node][to_node] = travel_time
            if way_data['tags'].get('oneway') != 'yes':
                graph[to_node][from_node] = travel_time
                

def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 6371000
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2) + math.sin(dlon/2)**2
    return 2*radius*math.sin(math.sqrt(a))

def time_weight(distance, maxspeed):
    time_minutes = (maxspeed/distance)/60
    return time_minutes