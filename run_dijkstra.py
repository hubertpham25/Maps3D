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

def reconstruct_path(previous, start, end):
    path = list()
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    return path[::-1] if path[-1] == start else list()

