import heapq

def dijkstra(start, end, graph):
    distances = {node_id: float('inf') for node_id in graph}
    distances[start] = 0

    previous = {node_id: None for node_id in graph}
    visited = set()

    to_visit = list()
    heapq.heappush(to_visit, (0, start))

    while to_visit:
        current_cost, current_node = heapq.heappop(to_visit)
        if distances[current_node] < current_cost:
            continue

        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight

            
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(to_visit, (new_cost, neighbor))
    return distances

