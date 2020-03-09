class AdjacencyMatrix():

    def __init__(self, edges: str):
        self.f = {}
        self.d = {}
        self.weighted = False
        #self.edges = deepcopy(edges)
        count_array = []
        track = -1
        edg = edges.splitlines()

        for x in edg:
            # print(x)
            x = x.split()
            # print(x)
            if len(x) == 3:
                self.weighted = True

            if x[0] not in count_array:
                count_array.append(x[0])
                track = track + 1
                self.f[x[0]] = track
            if x[1] not in count_array:
                count_array.append(x[1])
                track = track + 1
                self.f[x[1]] = track

        # f= {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '10': 9, '11': 10, '12': 11, '13': 12, '17': 13, '19': 14, '21': 15, '31': 16, '30': 17, '9': 18, '27': 19, '28': 20, '32': 21, '16': 22, '33': 23, '14': 24, '15': 25, '18': 26, '20': 27, '22': 28, '23': 29, '25': 30, '29': 31, '24': 32, '26': 33}
        # track = 33
        a = [0] * (track + 2)

        for h in self.f:
            self.d[self.f[h]] = deepcopy(a)

        #ed = deepcopy(edges)
        #edges = open('datasets/hep.txt', "r")
        for i in edg:

            o = i.split()
            # print(o)
            val = self.f[o[0]]
            keyval = self.d[val]
            j = self.f[o[1]]

            keyval[j] = 1
            self.d[val] = keyval

            # since the graph is undirected, we do the same for all the second column vertexes.

            val2 = self.f[o[1]]
            #print("vallll2", val2)
            keyval2 = self.d[val2]
            k = self.f[o[0]]
            keyval2[k] = 1
            self.d[val2] = keyval2

            if self.weighted == True:
                keyval[track + 1] = o[2]
                self.d[val] = keyval
                keyval2[track +1] = o[2]
                self.d[val2] = keyval2

        #print("dict1", self.f)

        #print("FinalDict", self.d)

        # return self.f

    def vertices(self):
        """Iterates over the vertices in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        nothing.

        Yields:
        vertices in the graph.
        """
#         print("wtff")
        for x in self.f:
#             print(x)
            yield x

    def edges(self)-> {Edge}:
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
                if l == 1:

                    for key, value in self.f.items():
                        if value == count:
#                               print(i, key)
#                               print (Edge(i, key))
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
        print(c)
        return c

    def edge_count(self) -> int:
        """Returns the number of edges in the graph.

        Args:
        - self: the instance to operate on.

        Returns:
        the number of edges in the graph.
        """
        # y = 0
        # print(edges)
        # for e in edges:
        #     print(e)
        #     y = y + 1
        # print(y)
        # return y
        e = 0
        for value in self.d.values():
            for i in value:
                if i == 1:
                    e = e + 1
#         print("e", e//2)
        return e//2
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
            #print("vert", True)
            return True

        else:
            #print("no_vert", False)
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
        # pass

        ver1 = self.f[v0]
        print(ver1)
        connections = self.d[ver1]
        ver2 = self.f[v1]
        print(ver2)

        if connections[ver2] == 1:
#             print("u", True)
            return True

        else:
#             print("d", False)
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
        count = 0
        ver1 = self.f[v]
        connections = self.d[ver1]
        print("conn", connections)
        for i in connections:
            count = count + 1
            #print("i", i)
            if i == 1:
                # print("reached")
                for key, value in self.f.items():
                    if value == count:
                        print(key)

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
            if count == 1:
                cnt = cnt + 1
#         print(cnt)
        return cnt
