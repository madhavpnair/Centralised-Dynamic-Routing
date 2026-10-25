import heapq
from math import inf


class DynamicSSSP:

    def __init__(self, graph, sink):
        """
        graph is an adjacency dictionary. It is a directed graph.
        graph[u] = {v: weight, ...} = dictionary of dictionaries,
        where each value dictionary represents the outgoing edges from vertex u and their weights.

        sink is the destination vertex

        we assume that all edge weights are strictly positive.

        - graph[vertex].items() returns a list of (destination, weight) pairs for all outgoing edges from vertex.
        - self.dist[vertex] = inf means that vertex cannot reach the sink. (unreachable vertex)
        """


        self.graph = {}
        self.sink = sink
        self.vertices = set() 
        self.pred = {}  # pred[v] stores all vertices having an edge to v.
        self.dist = {}  # dist[v] stores the shortest distance from v to the sink.
        self.sp = {}    # sp[v] stores all vertices reachable from v in the shortest-path subgraph SP(G).
        self.outdegree_sp = {}  # outdegree_sp[v] stores the outdegree of vertex v in the SP(G).

        for vertex, edges in graph.items():
            self.graph[vertex] = dict(edges)

        # Add vertices that appear only as edge destinations (with no outgoing edges)
        for edges in list(self.graph.values()):
            for destination in edges:
                if destination not in self.graph:
                    self.graph[destination] = {}

        
        for vertex in self.graph:
            self.vertices.add(vertex)

        
        for vertex in self.vertices:
            self.pred[vertex] = set()

        for vertex, edges in self.graph.items():
            for destination in edges:
                self.pred[destination].add(vertex)

        # Calculate initial shortest distances to the sink.
        self.dist = self.find_initial_distances()

        # Construct the shortest-path subgraph SP(G).
        self.sp = {}

        for vertex in self.vertices:
            self.sp[vertex] = set()

        for vertex, edges in self.graph.items():
            for destination, weight in edges.items():

                if self.dist[vertex] == inf:
                    continue

                if self.dist[destination] == inf:
                    continue

                # Check whether this edge belongs to a shortest path using SP(G) property: dist[u] = weight(u, v) + dist[v]
                if self.dist[vertex] == weight + self.dist[destination]:
                    self.sp[vertex].add(destination)

        # Count outgoing shortest-path edges of every vertex in SP(G).
        self.outdegree_sp = {}

        for vertex in self.vertices:
            self.outdegree_sp[vertex] = len(self.sp[vertex])

    def find_initial_distances(self):
        """
        Use Dijkstra's algorithm on the reversed graph
        to calculate distances to the sink.
        """

        # Build the reversed graph.
        reverse_graph = {}

        for vertex in self.vertices:
            reverse_graph[vertex] = []

        for vertex, edges in self.graph.items():
            for destination, weight in edges.items():
                reverse_graph[destination].append((vertex, weight))

        # Initially, every vertex has infinite distance.
        distances = {}

        for vertex in self.vertices:
            distances[vertex] = inf

        # Distance from the sink to itself is zero.
        distances[self.sink] = 0

        # A min-priority queue stores (distance, vertex).
        priority_queue = []
        heapq.heappush(priority_queue, (0, self.sink))

        while priority_queue:

            distance, vertex = heapq.heappop(priority_queue)

            # Ignore an outdated queue entry.
            if distance != distances[vertex]:
                continue

            # Check all incoming edges in the original graph.
            for predecessor, weight in reverse_graph[vertex]:

                new_distance = distance + weight

                if new_distance < distances[predecessor]:

                    distances[predecessor] = new_distance

                    heapq.heappush(
                        priority_queue,
                        (new_distance, predecessor)
                    )

        return distances

    def increment_edge(self, source, destination, weight):
        """
        Increment the weight of the edge source -> destination to weight.
        Using the two-phase Ramalingam-Reps algorithm to update the distances and SP(G) incrementally.

        Return the set of affected vertices.
        """

        """
        Approach:
        1. delete the edge from the SP(G) but keep it in the original graph with its new weight.
        2. find affected vertices
        recalculate distances and update SP(G) for affected vertices

        change in the approach from last meeting: 
        Don't delete the edge from the graph but keep it in the graph with its new weight.
        Include the incremented edge in the recalculation of distances and update of SP(G) for affected vertices.
        """

        # Check whether the edge exists.
        if destination not in self.graph.get(source, {}):
            raise ValueError(
                f"Edge {source} -> {destination} does not exist"
            )


        # If the edge is not in SP(G), distances do not change.
        if destination not in self.sp[source]:
            self.graph[source][destination] = weight
            return set()

        # if the edge is in SP(G), remove the edge from SP(G).

        self.graph[source][destination] = weight
        self.sp[source].remove(destination)

        self.outdegree_sp[source] -= 1

        # If another shortest-path edge remains, stop.
        if self.outdegree_sp[source] > 0:
            return set()


        '''
        if u -> v in SP(G) and outdegree_sp[source] == 0 (after removing the edge from SP(G)), 
        we do the two-phase Ramalingam-Reps algorithm to update the distances and SP(G)
        '''
        # Phase 1: Find all affected vertices
        # ------------------------------------------------

        work_set = [source]
        affected_vertices = set()

        while work_set:

            # Take one vertex out of the work set.
            vertex = work_set.pop()

            if vertex in affected_vertices:
                continue

            # Mark this vertex as affected.
            affected_vertices.add(vertex)

            # check vertices having edges into this vertex.
            for predecessor in list(self.pred[vertex]):

                # Check whether the incoming edge is in SP(G).
                if vertex in self.sp[predecessor]:

                    self.sp[predecessor].remove(vertex)

                    self.outdegree_sp[predecessor] -= 1

                    # If no shortest-path edge remains,
                    # this predecessor may also be affected.
                    if self.outdegree_sp[predecessor] == 0:

                        if predecessor not in affected_vertices:
                            work_set.append(predecessor)

        
        # Phase 2: Recalculate distances and update SP(G) for affected vertices
        # ------------------------------------------------

        """
        Recalculate distances from the unaffected vertices into the affected set.
        The incremented edge remains in self.graph with its new weight,
        so it is considered here just like every other edge.
        """

        """
        The following approach failed because it assumed that 
        if the source vertex of the incremented edge uses the incremented edge in its new shortest path, 
        then all affected vertices use the same incremented edge in their new shortest paths, 
        and their distances increase by the same amount.
        However, this assumption is not always true. 
        The affected vertices may have different new shortest paths that do not use the incremented edge
        """

        """
        source may or may not use the incremented edge in its new shortest path.
        (1) If it does, all the affected vertices use the same incremented edge in their new shortest paths,
            and their distances increase by the same amount. 
            Recomputation of distances is easy in this case. No need to depend on successors of affected vertices.
        (2) If it does not, the new shortest path for source uses a different edge, 
            and the new shortest paths for affected vertices may use different edges, 
            and their distances may increase by different amounts. 
            We need to recompute the distances for all affected vertices individually in this case.

        To check case (1), we find the new distance for source using the incremented edge, 
        and compare it with the best distance for source using other edges. 
        If the new distance using the incremented edge is less than or equal to the best distance using other edges, 
        then case (1) holds, and we can update the distances of all affected vertices by the same amount. 

        Otherwise, case (2) holds, and we need to find new distances for all affected vertices individually.

        
        we know that u -> v belongs to SP(G)
        So, self.dist[source] = self.dist[destination] + old_weight
        
        """
        

        """
        1. Find the new distance for source using the incremented edge.
        2. Find the best distance for source using other edges.
        3. Compare the two distances.
        """

        '''
        old_distance_src = self.dist[source]
        old_distance_dest = self.dist[destination]
        new_dist_scr_using_incremented_edge = old_distance_dest + weight

        # find new distance for the source vertex of the deleted edge
        best_distance = inf

        for destination, weight in self.graph[source].items():

            if destination in affected_vertices:
                continue

            if self.dist[destination] == inf:
                continue

            candidate_distance = weight + self.dist[destination]

            if candidate_distance < best_distance:
                best_distance = candidate_distance

        self.dist[source] = best_distance

    
        if best_distance >= new_dist_scr_using_incremented_edge:
            self.dist[source] = new_dist_scr_using_incremented_edge
            self.outdegree_sp[source] = 1
            self.sp[source].add(destination)

            for vertex in affected_vertices:
                if vertex == source:
                    continue

                else:
                    self.dist[vertex] = self.dist[vertex] + (new_dist_scr_using_incremented_edge - old_distance_src)

            return affected_vertices

        # If we reach here, case (2) holds, and we need to find new distances for all affected vertices individually.
        else:
        '''

        priority_queue = []
        # Start by treating every affected vertex as unreachable.
        for vertex in affected_vertices:
            self.dist[vertex] = inf
            self.sp[vertex].clear()
            self.outdegree_sp[vertex] = 0

        """
        Find candidate paths from affected vertices to unaffected vertices.
        Update distances of affected vertices if a shorter path is found.
        Distances of unaffected successors is the boundary information for the affected vertices.
        """
        for vertex in affected_vertices:
            for next_vertex, edge_weight in self.graph[vertex].items():
                if next_vertex in affected_vertices:
                    continue
                if self.dist[next_vertex] == inf:
                    continue
                candidate_distance = edge_weight + self.dist[next_vertex]
                if candidate_distance < self.dist[vertex]:
                    self.dist[vertex] = candidate_distance
            # Add reachable affected vertices to the priority queue.
            if self.dist[vertex] != inf:
                heapq.heappush(
                    priority_queue,
                    (self.dist[vertex], vertex)
                )
                
        """
        Propagate new distances backwards through the affected set.
        Update predecessors of affected vertices.
        """
        settled = set()
        while priority_queue:
            distance, vertex = heapq.heappop(priority_queue)
            # Ignore an outdated queue entry.
            if distance != self.dist[vertex]:
                continue
            # Do not process a finalized vertex again.
            if vertex in settled:
                continue
            settled.add(vertex)
            # Update affected predecessors of this vertex.
            for predecessor in self.pred[vertex]:
                if predecessor not in affected_vertices:
                    continue
                if predecessor in settled:
                    continue
                edge_weight = self.graph[predecessor][vertex]
                candidate_distance = edge_weight + self.dist[vertex]
                if candidate_distance < self.dist[predecessor]:
                    self.dist[predecessor] = candidate_distance
                    heapq.heappush(
                        priority_queue,
                        (candidate_distance, predecessor)
                    )

        """
        Restore shortest-path edges for affected vertices.
        Update outdegree_sp for affected vertices.
        Update SP(G)
        """
        for vertex in affected_vertices:
            for next_vertex, edge_weight in self.graph[vertex].items():
                if self.dist[vertex] == inf:
                    continue
                if self.dist[next_vertex] == inf:
                    continue
                if self.dist[vertex] == edge_weight + self.dist[next_vertex]:
                    self.sp[vertex].add(next_vertex)
            self.outdegree_sp[vertex] = len(self.sp[vertex])

        """
        An unaffected predecessor may still have a shortest-path edge
        into an affected vertex. Check those edges using the new distances.
        Update SP(G) and outdegree_sp for unaffected predecessors.
        """
        for vertex in affected_vertices:
            for predecessor in self.pred[vertex]:
                if predecessor in affected_vertices:
                    continue
                edge_weight = self.graph[predecessor][vertex]
                if self.dist[predecessor] == edge_weight + self.dist[vertex]:
                    if vertex not in self.sp[predecessor]:
                        self.sp[predecessor].add(vertex)
                        self.outdegree_sp[predecessor] += 1

        # Handle vertices that can no longer reach the sink.
        for vertex in affected_vertices:
            if self.dist[vertex] == inf:
                self.sp[vertex].clear()
                self.outdegree_sp[vertex] = 0


        return affected_vertices
    
        
    def print_state(self):

        print("Distances:")

        for vertex in sorted(self.vertices):
            print(f"  dist[{vertex}] = {self.dist[vertex]}")

        print("\nSP(G):")

        for vertex in sorted(self.vertices):
            print(f"  {vertex} -> {sorted(self.sp[vertex])}")

        print("\nSP outdegrees:")

        for vertex in sorted(self.vertices):
            print(
                f"  outdegree_SP[{vertex}] = "
                f"{self.outdegree_sp[vertex]}"
            )


# Example usage
# =========================================================

if __name__ == "__main__":

    print("Dynamic SSSP Edge weight increment tests")
    print("----------------------------------------------------")

    print("test 1: Incrementing an edge that will remain as a part of a shortest path")
    graph1 = {
        "A": {"B": 2, "C": 5, "T": 10},
        "B": {"T": 3},
        "C": {"T": 2},
        "T": {},
    }
    graph2 = {
        "A" :{"C":1},
        "B" : {"D":2},
        "C" : {"E":3},
        "D" : {"C":2, "F":2},
        "E" : {"T":2},
        "F" : {"T":4}

    }

    sssp = DynamicSSSP(graph2, sink="T")

    print("BEFORE INCREMENT")
    sssp.print_state()

    print("\nIncrementing edge A -> T")

    # affected = sssp.increment_edge("C", "E", weight=1)
    affected = sssp.increment_edge("C", "E", weight=5)


    print("\nAffected vertices:", sorted(affected))

    print("\nAFTER INCREMENT")
    sssp.print_state()

    
    
    print("\n\n----------------------------------------------------")
    print("test 2: Incrementing an edge that will no longer be a part of a shortest path")
    sssp = DynamicSSSP(graph1, sink="T")

    print("BEFORE INCREMENT")
    sssp.print_state()

    print("\nIncrementing edge A -> T")

    affected = sssp.increment_edge("A", "T", weight=10)

    print("\nAffected vertices:", sorted(affected))

    print("\nAFTER INCREMENT")
    sssp.print_state()
