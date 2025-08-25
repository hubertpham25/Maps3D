import math

def build_routing_graph(nodes, ways):
    graph = {}
    road_nodes = set()
    
    for way_id, way_data in ways.items():
        if 'highway' not in way_data['tags']:
            continue
            
        highway_type = way_data['tags']['highway']
        if highway_type in ['footway', 'cycleway', 'pedestrian', 'steps']:
            continue
        
        if 'maxspeed' not in way_data['tags']:
            maxspeed = 25
        else: 
            maxspeed_str = way_data['tags']['maxspeed']
            if 'mph' in maxspeed_str:
                maxspeed = int(maxspeed_str.strip(' mph'))
            else:
                maxspeed = 25
        
        way_nodes = way_data['nodes']
        
        for node in way_nodes:
            if node in nodes:
                road_nodes.add(node)
        
        for i in range(len(way_nodes) - 1):
            from_node = way_nodes[i]
            to_node = way_nodes[i + 1]
            
            if from_node not in nodes or to_node not in nodes:
                continue
            
            from_coord = nodes[from_node]['coord']
            to_coord = nodes[to_node]['coord']
            distance = calculate_distance(from_coord, to_coord)
            travel_time = time_weight(distance, maxspeed)
            
            if from_node not in graph:
                graph[from_node] = {}
            if to_node not in graph:
                graph[to_node] = {}
            
            graph[from_node][to_node] = travel_time
            if way_data['tags'].get('oneway') != 'yes':
                graph[to_node][from_node] = travel_time
    
    road_connected_nodes = {nid: nodes[nid] for nid in road_nodes if nid in graph and graph[nid]}
    
    return graph, road_connected_nodes
                

def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 3959
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return radius*c

def time_weight(distance, maxspeed):
    time_minutes = (distance/maxspeed)*60
    return time_minutes