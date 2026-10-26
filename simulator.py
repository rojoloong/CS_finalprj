# AI USAGE CITATION:
# Used AI assistance to sanity-check the simulation flow at a conceptual level,
# including how the documentary are clearly expressing what I want to mean
# All simulation logic and state tracking were implemented manually.

# node -> deliveries for each courier
def simulate(graph, depot, courier_routes, courier_deliveries, verbose = True):
    """
    Simulate couriers walking along their routes.

    Inputs:
        graph: Graph object (supports graph[node][neighbor] = weight)
        depot: str (starting node)
        courier_routes: list of list of nodes (one route per courier)
        courier_deliveries: list of list of delivery dicts for each courier
                            (each delivery has keys: "dest", "label")
        verbose: if True, print detailed logs

    Returns:
        summary: dict with keys:
            - "total_deliveries": int
            - "courier_times": list of floats
            - "courier_completed": list of list of (delivery_dict, time)
            - "max_delivery_time": float
    """
    delivery_lookup = []

    for bucket in courier_deliveries:
        dmap = {}
        for d in bucket:
            dest = d["dest"]
            if dest not in dmap:
                dmap[dest] = []
            dmap[dest].append(d)
        delivery_lookup.append(dmap)
    
    courier_times = []
    courier_completed = []

    if verbose:
        print("Simulation Start: ")
    
    for idx, route in enumerate(courier_routes):
        name = f"Courier_{idx+1}"
        dmap = delivery_lookup[idx]
        completed = []

        if len(route) <= 1:
            if verbose:
                print("\n{name}: no deliveries assigned.")
            courier_times.append(0.0)
            courier_completed.append(completed)
            continue
        
        if verbose:
            print(f"\n{name} route: {' -> '.join(route)}")
        
        time = 0.0
        cur = route[0]

        for nxt in route[1:]:
            # situation for missing edge: treat as 0 time but warn
            if nxt not in graph[cur]:
                if verbose:
                    print(f"Warning: No edge {cur} -> {nxt}, treating as 0.")
                w = 0.0
            else:
                w = graph[cur][nxt]
            
            time += w
            cur = nxt

            if cur in dmap and dmap[cur]:
                # complete all deliveries at this node
                for d in dmap[cur]:
                    completed.append((d, time))
                    if verbose:
                        print(f"{name}: completed '{d['label']}' at {cur} (t={time})")
                    dmap[cur] = []

        courier_times.append(time)
        courier_completed.append(completed)
        
    if verbose:
        print("\n Simulation ends.")
        
     # summarize the action
    total_deliveries = sum(len(c) for c in courier_completed)
    max_delivery_time = 0.0
    for bucket in courier_completed:
        for d, t in bucket:
            if t > max_delivery_time:
                max_delivery_time = t
        
    summary = {
        "total_deliveries": total_deliveries,
        "courier_times": courier_times,
        "courier_completed": courier_completed,
        "max_delivery_time": max_delivery_time
    }
    return summary
    



