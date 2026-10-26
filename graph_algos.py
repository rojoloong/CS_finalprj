# AI USAGE CITATION:
# Used AI assistance to confirm the documentary of function dijkstra, and get_path
# The algorithm, data structures, and all code were written manually.

import heapq
import math

class Graph:
    '''
    Undirected weighted graph with shortest-path.
    Nodes are hashable objects, often in string format.
    '''
    def __init__(self):
        self.adj = {} # node -> {neighbor: weight}
    
    # add undirected edge
    def add_edge(self, u, v, w):
        if w <= 0:
            raise ValueError(f"Edge weight must be positive.")
        if u not in self.adj:
            self.adj[u] = {}
        if v not in self.adj:
            self.adj[v] = {}
        
        self.adj[u][v] = w
        self.adj[v][u] = w
    
    def has_node(self, node):
        return node in self.adj
    
    def neighbors(self, node):
        return self.adj.get(node, {})
    
    def nodes(self):
        return list(self.adj.keys())
    
    # allow graph[node] style access in scheduler and simulator
    def __getitem__(self, node):
        return self.adj[node]
    
    def __iter__(self):
        return iter(self.adj.keys())
    
    # shortest path constructions
    def dijkstra(self, start):
        """
        Run Dijkstra from start.
        Returns (dist, parent):
          dist[node]   = shortest distance from start
          parent[node] = predecessor on shortest path
        """
        dist = {node: math.inf for node in self.adj}
        parent = {node: None for node in self.adj}

        if start not in self.adj:
            return dist, parent
        
        dist[start] = 0
        pq = []
        heapq.heappush(pq, (0, start)) #(cost, node)

        while pq:
            d, u = heapq.heappop(pq)

            if d > dist[u]:
                continue

            for v, w in self.adj[u].items():
                new_d = d + w
                if new_d < dist[v]:
                    dist[v] = new_d
                    parent[v] = u
                    heapq.heappush(pq, (new_d, v))
        return dist, parent

    def get_path(self, parent, start, end):
        """
        Reconstruct shortest path from start to end using parent table.
        Returns [] if unreachable.
        """
        if start == end and start in parent:
            return [start]
        if end not in parent or parent[end] is None:
            return []
        
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = parent[cur]

        path.reverse()
        return path

    def path_cost_through_stops(graph, depot, stops):
        """
        Compute total shortest-path cost starting at depot and
        visiting each stop in order. Returns infinity for unreachable stop.
        """
        if not stops:
            return 0.0
        
        total = 0.0
        cur = depot

        for dest in stops:
            dist, parent = dijkstra(graph, cur)
            if dist.get(dest, math.inf) == math.inf:
                return math.inf
            
            total += dist[dest]
            cur = dest

        return total
