import math

# Split deliveries into num_couriers buckets in round-robin order.
# deliveries: list of {"dest": node, "label": str}
# Returns: a list with each entry is a list of deliveries
def assign_round_robin(deliveries, num_couriers):
    if num_couriers <= 0:
        raise ValueError("Number of courier must be positive.")
    
    buckets = [[] for _ in range(num_couriers)]

    for i, d in enumerate(deliveries):
        buckets[i % num_couriers].append(d)
    
    return buckets

# Baseline is the original ordering
def order_in_given(deliveries):
    return deliveries[:]

# Nearest_next ordering
# starting from depot and run Dikstra from current node repeatedly until destination
def order_nearest(depot, deliveries, graph):
    remaining = deliveries[:]
    ordered = []
    cur = depot

    while remaining:
        dist, _ = graph.dijkstra(cur)

        best_idx = 0
        best_dist = math.inf

        for i, d in enumerate(remaining):
            dest = d["dest"]
            if dest in dist and dist[dest] < best_dist:
                best_dist = dist[dest]
                best_idx = i
        
        chosen = remaining.pop(best_idx)
        ordered.append(chosen)
        cur = chosen["dest"]
    
    return ordered

# Local 2-swap improvement on an existing delivery order.
# Try swapping pairs of conditions. If the swap lowers the total route cost
# (via shortest path), keep it. Repeat until no improving swap.
def improve_order_2swap(depot, deliveries, graph):
    n = len(deliveries)
    if n < 3:
        return deliveries[:]
    
    best_order = deliveries[:]
    best_stops = [d["dest"] for d in best_order]
    best_cost = graph.path_cost_through_stops(depot, best_stops)

    improved = True
    while improved:
        improved = False

        for i in range(n):
            for j in range(i+1, n):
                candidate = best_order[:]
                candidate[i], candidate[j] = candidate[j], candidate[i]

                stops = [d["dest"] for d in candidate]
                cost = graph.path_cost_through_stops(depot, stops)

                if cost < best_cost:
                    best_cost = cost
                    best_order = candidate
                    improved = True
                    break
                if improved:
                    break
    return best_order

# Change from an ordered list of deliveries into a node by node route.
def build_route(graph, depot, ordered_deliveries):
    """
    Build a route using Graph.dijkstra + Graph.get_path.
    graph is a Graph object.
    """
    if not ordered_deliveries:
        return [depot]
    
    route = [depot]
    cur = depot

    for d in ordered_deliveries:
        dest = d["dest"]
        dist, parent = graph.dijkstra(cur)
        path = graph.get_path(parent, cur, dest)

        if not path:
            print(f"Warning: No path from {cur} to {dest}, skipping this leg.")
            continue
        
        route.extend(path[1:])
        cur = dest

    return route







