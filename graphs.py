import math
from copy import deepcopy
import copy


class Edge:
    """ An undirected edge. """

    def __init__(self, v0: int, v1: int):
        """Create edge with endpoints at v0 and v1.

        Args:
        - self: the instance to create.
        - v0, v1: endpoints of the edge

        Returns:
        nothing.
        """
        self.v0, self.v1 = sorted((v0, v1))

    def __repr__(self) -> str:
        """Returns string representation of edge for printing.

        Allows `print()` on instances.

        Args:
        - self: this instance.

        Returns:
        string representation for printing.
        """
        return f'({self.v0}, {self.v1})'

    def __eq__(self, other) -> bool:
        """Does other have the same enpoints?

        Allows `==` on instances.

        Args:
        - self: this instance.
        - other: edge to compare with.

        Returns:
        True if other has the same endpoints as this edge.
        """
        if type(other) == type(self):
            return (self.v0, self.v1) == (other.v0, other.v1)
        return False

    def __hash__(self) -> int:
        """Returns hash of this edge.

        Makes instances hashable, allows adding them to appropraite containers,
        e.g. `set`, `dict`.

        Args:
        - self: this instance.

        Returns:
        a hash of this edge.

        """
        return hash(tuple(sorted(self.__dict__.items())))

    def __contains__(self, v) -> bool:
        """Is v an endpoint of this edge?

        Allows `in` syntax.

        Args:
        - self: this instance.
        - v: the vertex to check.

        Returns:
        True if v is an endpoint, False otherwise.
        """
        return v == self.v0 or v == self.v1

    def nbr(self, v: int) -> int:
        """Returns the neighbor of v along this edge if v is an endpoint.

        Args:
        - self: this instance.
        - v: the vertex whose neighbor is sought.

        Returns:
        the other endpoint if v is an endpoint, otherwise None.
        """
        return self.v0 if v == self.v1 else self.v1 if v == self.v0 else None


class Graph:
    """ Represents an undirected, possibly weighted, graph. """

    def __init__(self, edges: str, imp: str):
        """Creates graph with the given edges using the specified implementation.

        edges consists of multiple lines representing an edge list
        representation of the graph. Each line contains 2 vertices and an
        optional weight. All values in a line are separated by spaces. The vertices have integer values
        and the optional weight is a float. The vertices need not begin at 0.

        the value of imp sepcifies the graph implementation to be used as follows:
        sets   : two sets, one each for the vertices and the edges
        matrix : adjacenccy matrix
        list   : adjacency list

        Args:
        self: the instance to create.
        edges: an edge list representation of the graph
        imp: the implementation to be used

        Returns:
        nothing.
        """
        if imp == "sets":
            self.graph = SetGraph(edges)
        elif imp == "matrix":
            self.graph = AdjacencyMatrix(edges)
        elif imp == "list":
            self.graph = AdjacencyList(edges)

    def vertices(self):
        """Iterates over the vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        return self.graph.vertices()

    def edges(self) -> {Edge}:
        """Iterates over the edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        return self.graph.edges()

    def vertex_count(self) -> int:
        """Returns the number of vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of vertices in the graph.
        """
        return self.graph.vertex_count()

    def edge_count(self) -> int:
        """Returns the number of edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of edges in the graph.
        """
        return self.graph.edge_count()

    def has_vertex(self, v) -> bool:
        """Returns whether v is a vertex in the graph.

        Args:
        - self: the instance to operate on.
        - v: its neighbors in the graph are to be returned.

        Returns:
        True if v is a vertex in the graph, False otherwise.
        """
        return self.graph.has_vertex(v)

    def has_edge(self, v0, v1) -> bool:
        """Returns whether the grpah contains an edge between v0 and v1.

        Args:
        - self: the instance to operate on.
        - v0, v1: does an edge exist between vertices v0 and v1 in the graph?

        Returns:
        True if an edge exists between v0 and v1 in the graph, False otherwise.
        """
        assert self.has_vertex(v0) and self.has_vertex(v1), \
            f'one or more of {v0} and {v1} are not valid vertices'

        return self.graph.has_edge(v0, v1)

    def has_weights(self) -> bool:
        """Returns whether the graph is weighted.

        Args:
        - self: the instance to operate on.

        Returns:
        True if the graph edges are weighted, False otherwise.
        """
        return self.graph.weighted

    def neighbors(self, v):
        """Iterates over the neighbors of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: the vertex whose neighbors in the graph are sought.

        Returns:
        nothing.

        Yields:
        neighbors of v in the graph.
        """
        return self.graph.neighbors(v)

    def degree(self, v) -> {int}:
        """Returns the degree of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: its degree in the graph is to be returned.

        Returns:
        degree of v in the graph.
        """
        return self.graph.degree(v)

    def weight(self, v0: int, v1: int):
        """Returns the weight of the edge between v0 and v1; None if no weight.

        Assumes the presence of the edge between v0 and v1. Check before calling.

        Args:
        - self: the instance to operate on.
        - v0, v1: the weight of the edge between v0 and v1 is sought.

        Returns:
        The weight of the edge between v0 and v1; None if graph is unweighted.
        """
        return self.graph.weight(v0, v1)


# ----------------------------------------------------AdjacencyList----------------------------------------------------------------- #

class AdjacencyList():
    def __init__(self, edges: str):
        """Creates graph with the given edges

        edges consists of multiple lines representing an edge list
        representation of the graph. Each line contains 2 vertices and an
        optional weight. All values in a line are separated by spaces. The vertices have integer values
        and the optional weight is a float. The vertices need not begin at 0.

        Args:
        self: the instance to create.
        edges: an edge list representation of the graph

        Returns:
        nothing."""
        self.weighted = False  # bool for weighted graphs

        self.graph_dict = {}

        for edge in edges.splitlines():
            if len(edge.strip().split()) == 3:
                self.weighted = True
            break

        for edge in edges.splitlines():
            # storing edges in lst after removing spaces, \n etc
            if edge == '':
                continue
            new_edge = edge.strip().split()
            if self.weighted == True:
                new_edge = [float(i) for i in new_edge]
                if new_edge[0] not in self.graph_dict.keys():
                    self.graph_dict[new_edge[0]] = [
                        [Edge(new_edge[0], new_edge[1]), new_edge[2]]]
                else:
                    self.graph_dict[new_edge[0]] = self.graph_dict[new_edge[0]
                                                                   ] + [[Edge(new_edge[0], new_edge[1]), new_edge[2]]]
                if new_edge[1] not in self.graph_dict.keys():
                    self.graph_dict[new_edge[1]] = [
                        [Edge(new_edge[1], new_edge[0]), new_edge[2]]]
                else:
                    self.graph_dict[new_edge[1]] = self.graph_dict[new_edge[1]
                                                                   ] + [[Edge(new_edge[0], new_edge[1]), new_edge[2]]]
            else:
                new_edge = [int(i) for i in new_edge]
                if new_edge[0] not in self.graph_dict.keys():
                    self.graph_dict[new_edge[0]] = [
                        Edge(new_edge[0], new_edge[1])]
                else:
                    self.graph_dict[new_edge[0]] = self.graph_dict[new_edge[0]
                                                                   ] + [Edge(new_edge[0], new_edge[1])]
                if new_edge[1] not in self.graph_dict.keys():
                    self.graph_dict[new_edge[1]] = [
                        Edge(new_edge[1], new_edge[0])]
                else:
                    self.graph_dict[new_edge[1]] = self.graph_dict[new_edge[1]
                                                                   ] + [Edge(new_edge[0], new_edge[1])]

    def vertices(self):
        """Iterates over the vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        for vertex in self.graph_dict.keys():
            yield vertex

    def edges(self) -> {Edge}:
        """Iterates over the edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        edge_count = []
        for vertex in self.graph_dict.keys():
            for edge in self.graph_dict[vertex]:
                if edge not in edge_count:
                    edge_count.append(edge)
                    if self.weighted != True:
                        yield edge
                    else:
                        yield edge[0]

    def vertex_count(self) -> int:
        """Returns the number of vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of vertices in the graph.
        """
        return len(self.graph_dict.keys())

    def edge_count(self) -> int:
        """Returns the number of edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of edges in the graph.
        """
        counted_edges = []
        edge_sum = 0
        for vertex in self.graph_dict.keys():
            for edge in self.graph_dict[vertex]:
                if edge or edge[0] not in counted_edges:
                    counted_edges.append(edge)
                    edge_sum += 1
        return edge_sum

    def has_vertex(self, v) -> bool:
        """Returns whether v is a vertex in the graph.

        Args:
        - self: the instance to operate on.
        - v: its neighbors in the graph are to be returned.

        Returns:
        True if v is a vertex in the graph, False otherwise.
        """
        return (v in self.graph_dict.keys())

    def has_edge(self, v0, v1) -> bool:
        """Returns whether the grpah contains an edge between v0 and v1.

        Args:
        - self: the instance to operate on.
        - v0, v1: does an edge exist between vertices v0 and v1 in the graph?

        Returns:
        True if an edge exists between v0 and v1 in the graph, False otherwise.
        """
        assert self.has_vertex(v0) and self.has_vertex(v1), \
            f'one or more of {v0} and {v1} are not valid vertices'

        for vertex in self.graph_dict.keys():
            for edge in self.graph_dict[vertex]:
                if Edge(v0, v1) == edge or Edge(v0, v1) == edge[0]:
                    return True
        return False

    def has_weights(self) -> bool:
        """Returns whether the graph is weighted.

        Args:
        - self: the instance to operate on.

        Returns:
        True if the graph edges are weighted, False otherwise.
        """
        return self.weighted

    def neighbors(self, v):
        """Iterates over the neighbors of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: the vertex whose neighbors in the graph are sought.

        Returns:
        nothing.

        Yields:
        neighbors of v in the graph.
        """
        for vertex in self.graph_dict.keys():
            if vertex == v:
                continue
            else:
                for edge in self.graph_dict[vertex]:
                    if edge in self.graph_dict[v]:
                        yield vertex

    def degree(self, v) -> {int}:
        """Returns the degree of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: its degree in the graph is to be returned.

        Returns:
        degree of v in the graph.
        """
        assert self.has_vertex(v), \
            f'{v} is not a valid vertex'
        return len(self.graph_dict[v])

    def weight(self, v0: int, v1: int):
        """Returns the weight of the edge between v0 and v1; None if no weight.

        Assumes the presence of the edge between v0 and v1. Check before calling.

        Args:
        - self: the instance to operate on.
        - v0, v1: the weight of the edge between v0 and v1 is sought.

        Returns:
        The weight of the edge between v0 and v1; None if graph is unweighted.
        """
        if self.weighted:
            for edge in self.graph_dict[v0]:
                if Edge(v0, v1) == edge[0]:
                    return edge[1]
            return None
        else:
            return 1

# ----------------------------------------------------AdjacencyMatrix----------------------------------------------------------------- #

class AdjacencyMatrix():

    def __init__(self, edges: str):
        self.f = {}
        self.d = {}
        self.weighted = False
        count_array = []
        # self.edge_c = 0
        # self.vert_c = 0
        track = -1

        for x in edges.splitlines():

            if x == '':
                continue

            #self.edge_c = self.edge_c + 1
            x = x.split()
            x[0] = int(x[0])
            x[1] = int(x[1])

            if len(x) == 3:
                self.weighted = True

            if x[0] not in count_array:
                count_array.append(x[0])
                #self.vert_c = self.vert_c + 1
                track = track + 1
                self.f[x[0]] = track

            if x[1] not in count_array:
                count_array.append(x[1])
                track = track + 1
                #self.vert_c = self.vert_c + 1
                self.f[x[1]] = track

        a = [0] * (track + 2)

        for h in self.f:
            self.d[self.f[h]] = deepcopy(a)

        for i in edges.splitlines():
            if i == '':
                continue
            o = i.split()
            o[0] = int(o[0])
            o[1] = int(o[1])

            val = self.f[o[0]]
            keyval = self.d[val]
            j = self.f[o[1]]

            if self.weighted == False:

                keyval[j] = 1
                self.d[val] = keyval

            if self.weighted == True:
                keyval[j] = float(o[2])
                self.d[val] = keyval

            # since the graph is undirected, we do the same for all the second column vertexes.

            val2 = self.f[o[1]]
            keyval2 = self.d[val2]
            k = self.f[o[0]]

            if self.weighted == False:
                keyval2[k] = 1
                self.d[val2] = keyval2

            if self.weighted == True:
                keyval2[k] = float(o[2])
                self.d[val2] = keyval2

           

    def vertices(self):
        """Iterates over the vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """

        for x in self.f:

            yield x

    def edges(self) -> {Edge}:
        """Iterates over the edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        for i in self.f.keys():
            x = self.f[i]

            count = -1
            lst = self.d[x]
            for l in lst:
                count = count + 1
                if l:

                    for key, value in self.f.items():
                        if value == count:
                            yield Edge(i, key)

    def vertex_count(self) -> int:
        """Returns the number of vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of vertices in the graph.
        """

        c = 0
        for k in self.f:
            c = c + 1

        return c
        # return self.vert_c

    def edge_count(self) -> int:
        """Returns the number of edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of edges in the graph.
        """
        
        e = 0
        for value in self.d.values():
            for i in value:
                # if i == 1:
                if i:
                    e = e + 1

        return e//2
        # return self.edge_c
        # class AdjacencyList(Graph):

    def has_vertex(self, v) -> bool:
        """Returns whether v is a vertex in the graph.

        Args:
        - self: the instance to operate on.
        - v: its neighbors in the graph are to be returned.

        Returns:
        True if v is a vertex in the graph, False otherwise.
        """

        if v in self.f.keys():
            
            return True

        else:
            
            return False

    def has_edge(self, v0, v1) -> bool:
        """Returns whether the grpah contains an edge between v0 and v1.

        Args:
        - self: the instance to operate on.
        - v0, v1: does an edge exist between vertices v0 and v1 in the graph?

        Returns:
        True if an edge exists between v0 and v1 in the graph, False otherwise.
        """
        assert self.has_vertex(v0) and self.has_vertex(v1), \
            f'one or more of {v0} and {v1} are not valid vertices'
        

        ver1 = self.f[v0]
        
        connections = self.d[ver1]
        ver2 = self.f[v1]
        
        if connections[ver2]:
            
            return True

        else:
            
            return False

    def has_weights(self) -> bool:
        """Returns whether the graph is weighted.

        Args:
        - self: the instance to operate on.

        Returns:
        True if the graph edges are weighted, False otherwise.
        """
        return self.weighted

    def neighbors(self, v):
        """Iterates over the neighbors of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: the vertex whose neighbors in the graph are sought.

        Returns:
        nothing.

        Yields:
        neighbors of v in the graph.
        """
        count = -1
        ver1 = self.f[v]
        connections = self.d[ver1]
        #print("conn", connections)
        for i in connections:
            count = count + 1
            #print("i", i)
            # if i == 1:
            if i:
                # print("reached")
                for key, value in self.f.items():
                    if value == count:
                        yield key

    def degree(self, v) -> {int}:
        """
        Returns the degree of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: its degree in the graph is to be returned.

        Returns:
        degree of v in the graph.
        """
        cnt = 0
        i = self.d[self.f[v]]
        for count in i:
            # if count == 1:
            if count:
                cnt = cnt + 1
        return cnt

    def weight(self, v0: int, v1: int):
        if self.weighted and self.has_edge(v0, v1):
            a = self.f[v0]
            b = self.f[v1]
            lst = self.d[a]
            w = lst[b]

            return w
        return 1

# ----------------------------------------------------SetGraph----------------------------------------------------------------- #

class SetGraph():

    def __init__(self, edges: str):
        self.vert = set()
        self.ed = set()
        self.graph = 0
        self.weighted = False
        self.vertcount = 0

        for x in edges.splitlines():
            if x == '':
                continue
            x = x.split()
            x[0] = int(x[0])
            x[1] = int(x[1])
            if len(x) == 3:
                self.weighted = True
                self.ed.add((Edge(x[0], x[1]), float(x[2])))
            else:
                self.ed.add((Edge(x[0], x[1]), 0))

            if x[0] not in self.vert:
                self.vert.add(x[0])
                self.vertcount = self.vertcount + 1
            if x[1] not in self.vert:
                self.vert.add(x[1])
                self.vertcount = self.vertcount + 1

    def vertices(self):
        """Iterates over the vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        for v in self.vert:
            yield v

    def edges(self):
        """Iterates over the edges in the graph.-> {Edge}
        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
        for e in self.ed:
            yield e[0]

    def vertex_count(self) -> int:
        """Returns the number of vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of vertices in the graph.
        """
        return self.vertcount

    def edge_count(self) -> int:
        """Returns the number of edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of edges in the graph.
        """
        return len(self.ed)

    def has_vertex(self, v) -> bool:
        """Returns whether v is a vertex in the graph.

        Args:.
        - self: the instance to operate on.
        - v: its neighbors in the graph are to be returned.

        Returns:
        True if v is a vertex in the graph, False otherwise.
        """
        return v in self.vert

    def has_edge(self, v0, v1) -> bool:
        """Returns whether the grpah contains an edge between v0 and v1.

        Args:
        - self: the instance to operate on.
        - v0, v1: does an edge exist between vertices v0 and v1 in the graph?

        Returns:
        True if an edge exists between v0 and v1 in the graph, False otherwise.
        """
        for i in self.ed:
            if v0 in i[0] and i[0].nbr(v0) == v1:
                return True
        return False

    def has_weights(self) -> bool:
        """Returns whether the graph is weighted.

        Args:
        - self: the instance to operate on.

        Returns:
        True if the graph edges are weighted, False otherwise.
        """
        return self.weighted

    def neighbors(self, v):
        """Iterates over the neighbors of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: the vertex whose neighbors in the graph are sought.

        Returns:
        nothing.

        Yields:
        neighbors of v in the graph.
        """
        for edge in self.ed:
            if v in edge[0]:
                yield edge[0].nbr(v)

    def degree(self, v) -> {int}:
        """
        Returns the degree of the vertex v in the graph.

        Errors if v is not in the graph. Check before calling.

        Args:
        - self: the instance to operate on.
        - v: its degree in the graph is to be returned.

        Returns:
        degree of v in the graph.
        """
        degree = 0
        for edge in self.ed:
            if v in edge[0]:
                degree = degree + 1
        return degree

    def weight(self, v0: int, v1: int):
        if self.weighted and self.has_edge(v0, v1):
            for x in self.ed:
                if v0 in x[0] and x[0].nbr(v0) == v1:
                    return x[1]
        return 1
