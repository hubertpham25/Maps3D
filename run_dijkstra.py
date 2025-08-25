import heapq
from graph_builder import calculate_distance

def dijkstra(start, end, graph):
    distances = {node_id: float('inf') for node_id in graph}
    distances[start] = 0
    
    previous = {node_id: None for node_id in graph}
    
    to_visit = []
    heapq.heappush(to_visit, (0, start))
    
    visited = set()
    
    while to_visit:
        current_distance, current_node = heapq.heappop(to_visit)
        
        if current_node in visited:
            continue
        visited.add(current_node)
        
        if current_node == end:
            return reconstruct_path(previous, start, end)
        
        for neighbor, weight in graph.get(current_node, {}).items():
            if neighbor in visited:
                continue
            
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(to_visit, (new_distance, neighbor))
    
    print("No path found")
    return []

def heuristic(current_node, end_node, intersections):
    current_coord = intersections[current_node]['coord']
    end_coord = intersections[end_node]['coord']
    return calculate_distance(current_coord, end_coord)

def filter_intersections(intersections, start_coord, end_coord, radius_miles=0.3):
    filtered = dict()
    for node_id, node_data in intersections.items():
        node_coord = node_data['coord']
        dist_to_start = calculate_distance(start_coord, node_coord)
        dist_to_end = calculate_distance(end_coord, node_coord)

        if (dist_to_start <= radius_miles) or (dist_to_end <= radius_miles):
            filtered[node_id] = node_data

    return filtered

def filter_graph(graph, relevant_nodes):
    filtered_graph = dict()
    for node in graph:
        if node in relevant_nodes:
            filtered_graph[node] = graph[node]
    return filtered_graph

def reconstruct_path(previous, start, end):
    path = list()
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    return path[::-1] if path[-1] == start else list()

