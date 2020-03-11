from graphs import *
import graphviz


class NetworkOperations:
    def degree_centrality(g: Graph, vtx: int) -> float:
        """Returns the degree centrality of the vertex, vtx in the graph, g.

        Args:
        - g: the graph/network to be checked.
        - vtx: the vertex in g whose degree centrality is sought.

        Returns:
        the degree centrality of vtx in g.
        """
        return (g.degree(vtx) / (g.vertex_count() - 1))

    def clustering_coefficient(g: Graph, vtx: int = None) -> float:
        """Returns the local or average clustering coefficient in g depending on vtx.

        vtx = None : average clustering coefficient of g
        vtx != None : local clustering coefficient of vtx in g

        Args:
        - g: the graph/network to be checked.
        - vtx: the vertex at which local clustering coefficient is sought.

        Returns:
        the local or average clustering coefficient in g.
        """
        
        def for_given_vertex(v):
            total_number_of_edges = 0
            vtx_neighbors = []
            total_neighbors = 0
            for neighbor in g.neighbors(v):
                for neighbor_of_neighbor in g.neighbors(v):
                    if neighbor_of_neighbor == neighbor: # Ignoring self connection
                        continue
                    else:
                        if neighbor_of_neighbor in vtx_neighbors:
                            continue
                        elif neighbor_of_neighbor in g.neighbors(neighbor):
                            total_number_of_edges +=1
                total_neighbors += 1
                vtx_neighbors.append(neighbor) # removing the checked neighbor, cause its alreasy checked with all others
            if total_neighbors == 1:
                return 0
            else:
                return (total_number_of_edges / ((total_neighbors * (total_neighbors - 1)) / 2))
        
        if vtx != None:
            return for_given_vertex(vtx)
        else:
            avg_clustering_coeff = 0
            for vertex in g.vertices():
                avg_clustering_coeff += for_given_vertex(vertex)
            return (avg_clustering_coeff / g.vertex_count())              

    def average_neighbor_degree(g: Graph, vtx: int) -> float:
        """Returns the average neighbor degree of vertex vtx in g.

        Args:
        - g: the graph/network to be checked.
        - vtx: the vertex whose average neighbor degree is sought.

        Returns:
        the average neighbor degree of vtx in g.
        """
        sum_of_degrees = 0
        for each_vertex in g.neighbors(vtx):
            sum_of_degrees += g.degree(each_vertex)
        return (sum_of_degrees / g.degree(vtx))

    def similarity(g: Graph, v0: int, v1: int) -> float:
        """Returns the Jaccard similarity of vertices, v0 and v1, in g.

        Args:
        - g: the graph/network to be checked.
        - v0, v1: the vertices in g who similarity is sought.

        Returns:
        The Jaccard similarity of vertices, v0 and v1, in g.
        """
        number_of_equal_vertices = 0
        for vertex in g.neighbors(v0):
            if vertex in g.neighbors(v1):
                number_of_equal_vertices += 1
        return (number_of_equal_vertices / (g.degree(v0) + g.degree(v1) - number_of_equal_vertices))

    def popular_distance(g: Graph, vtx: int) -> int:
        """Returns the popular distance of the vertex, vtx, in g.

        Args:
        - g: the graph/network to be checked.
        - vtx: the vertex in g whose popular distance is sought.

        Returns:
        the popular distance of the vertex, vtx, in g.
        """
        # finding the popular vertex\vertices
        popular_vertices = []
        for vertex in list(g.vertices()):
            if len(popular_vertices) == 0:
                popular_vertices.append(vertex)
                pop_degree = g.degree(vertex)
            else:
                if g.degree(vertex) > pop_degree:
                    popular_vertices = [vertex]
                    pop_degree = g.degree(vertex) 
                elif g.degree(vertex) ==  pop_degree:
                    popular_vertices.append(vertex)
        # function for the shortest distance of single popular vertex
        def shortest_path(popular_vertex):
            dist={}
            unvisited=[]
            for node in list(g.vertices()):
                dist[node] = math.inf
                unvisited.append(node)
            dist[vtx]= 0
            while unvisited:
                if dist[popular_vertex] != math.inf:
                    return (dist[popular_vertex])
                # searching for next vertex with min weight
                current = unvisited[0]
                for i in unvisited:
                    if dist[i] < dist[current]:
                        current = i
                unvisited.remove(current)
                neighbors = list(g.neighbors(current)) # getting all the neighbors
                for neighbor in neighbors:
                    weight = g.weight(current, neighbor)
                    if dist[current] + weight < dist[neighbor]:
                        dist[neighbor] = dist[current] +  weight
            return (dist[popular_vertex])
        # finding the shortest distance of of all popular vertices
        final_weight = math.inf
        for vertex in popular_vertices:
            temp_weight = shortest_path(vertex)
            if temp_weight < final_weight:
                final_weight = temp_weight
        if final_weight == math.inf:
            return -1
        else:
            return (int(final_weight))

    def visualize(g: Graph) -> None:
        """Visualizes g.

        Args:
        - g: the graph/network to be visualized.

        Returns:
        Nothing.
        """
        # Feel free to play around with the visualization.
        # Graphviz documentation: https://www.graphviz.org
        layout_engine = 'fdp' if g.vertex_count() < 2000 else 'sfdp'
        # graph to be visualized
        vizgraph = graphviz.Graph(engine=layout_engine)
        _ = [vizgraph.node(str(v)) for v in g.vertices()]
        vizgraph.edges(map(lambda e: (str(e.v0), str(e.v1)), g.edges()))
        vizgraph.render(view=True)
