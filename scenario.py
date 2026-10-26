# AI USAGE CITATION:
# Used AI assistance to help reason about some of input file validation cases
# (e.g., missing sections, invalid delivery destinations) and to clarify
# error-handling behavior. All parsing logic and file format decisions
# were coded manually by myslef

from graph_algos import Graph

def parse_scenario(path):
    """
    Parse a scenario file and return:
        graph: Graph object
        depot: str
        deliveries: list of {"dest": node, "label": str}
        num_couriers: int
    """
    section = None
    graph = Graph()
    depot = None
    deliveries = []
    num_couriers = None

    with open(path, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue

            upper = line.upper()
            if upper in {"MAP:", "DEPOT:", "DELIVERIES:", "COURIERS:"}:
                section = upper[:-1]
                continue

            if section == "MAP":
                parts = line.split()
                if len(parts) != 3:
                    raise ValueError(f"Invalid MAP line: {line}")
                u, v, w_str = parts
                w = float(w_str)
                graph.add_edge(u, v, w)
            
            elif section == "DEPOT":
                if depot is not None:
                    raise ValueError("Multiple DEPOT lines are found.")
                depot = line
            
            elif section == "DELIVERIES":
                # example is DEST(:label)
                # delivery goes to node dest and labeled (label)
                if ":" in line:
                    dest, label = line.split(":", 1)
                    deliveries.append({
                        "dest": dest.strip(),
                        "label": label.strip()
                    })
                else:
                    dest = line.strip()
                    deliveries.append({
                        "dest": dest,
                        "label": dest
                    })
                
            elif section == "COURIERS":
                if num_couriers is not None:
                    raise ValueError("Multiple COURIER lines are found.")
                num_couriers = int(line)
        
        # Basic Validation
        if depot is None:
            raise ValueError("DEPOT section missing.")
        if num_couriers is None:
            raise ValueError("COURIERS section missing.")
        if not graph.has_node(depot):                 
            raise ValueError(f"Depot '{depot}' not in MAP nodes.")
        
        for d in deliveries:
            dest = d["dest"]
            if not graph.has_node(dest):
                raise ValueError(f"Delivery destination '{dest}' not in MAP nodes.")
            
        return graph, depot, deliveries, num_couriers
    
def print_map_overview(graph, depot, deliveries):
    '''
    print a text overview of the graph
    mark the depot and nodes that are delivery destinations
    graph is a Graph object
    '''
    delivery_nodes = {d["dest"] for d in deliveries} 

    print("Map overview:")
    for node in sorted(graph.nodes()):
        tags = []
        if node == depot:
            tags.append("DEPOT")
        if node in delivery_nodes:
            tags.append("DELIVERY")
        tag_str = f"[{' ,'.join(tags)}]" if tags else ""
            
        neighbors = ", ".join(
            f"{nbr}({graph[node][nbr]})" for nbr in graph[node]
        )
        print(f" {node}{tag_str} -> {neighbors}")



                