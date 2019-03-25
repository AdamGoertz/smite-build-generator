import pickle
from typing import List, Tuple, Dict, Any

class WeightedGraph:
    def __init__(self, graph=None, *, label="WeightedGraph"):
        self.label = label

        if not graph:
            self.graph = {}
        else:
            if isinstance(graph, str):
                self.load(graph)
            elif isinstance(graph, dict):
                self.graph = graph
            else:
                raise TypeError("Unable to create graph from source.")

    def __str__(self):
        newline = '\n'
        return f"{self.label}:\n{newline.join([str(k) + ' : ' + str(v) for k,v in self.graph.items()])}"

    def addVertex(self, key: Any):
        if key not in self.graph:
            self.graph[key] = {}


    def removeVertex(self, key: Any):
        # Remove the vertex from the graph
        self.graph.pop(key, None)

        # Remove any edges connected to the vertex
        for k in self.graph:
            self.graph[k].pop(key, None)

    def removeEdge(self, v1, v2):
        if v1 not in self.graph or v2 not in self.graph:
            raise ValueError("One or more vertices not found in graph")

        self.graph[v1].pop(v2, None)
        self.graph[v2].pop(v1, None)

    def incrementEdgeWeight(self, v1: Any, v2: Any, amt: int):
        """Adds an edge of the specified weight, if it does not exist. Otherwise, increments the weight of the existing edge.

                Parameters:
                    v1 : Any -> the value of the one vertex
                    v2 : Any -> the value fo the second vertex
                    amt : int -> the amount by which the weight should be incremented
                Returns:
                    None
                Throws:
                    TypeError -> amt was not an integer
                    ValueError -> one or both of the vertices do not exist
                    AssertionError -> the vertices have mismatched weights for the same edge
        """

        if not isinstance(amt, int):
            raise TypeError("Increment amount must be an integer")
        if v1 not in self.graph or v2 not in self.graph:
            raise ValueError("One or more vertices not found in graph")

        try:
            self.graph[v1][v2] += amt
            self.graph[v2][v1] += amt
        except KeyError:
            self.graph[v1][v2] = amt
            self.graph[v2][v1] = amt

        # check that the both vertices have the same weight for the same edge
        assert self.graph[v1][v2] == self.graph[v2][v1]

    def loadFromList(self, vertices, complete:bool=True):
        """Takes a list of vertices, and adds them to the current graph.

            Parameters:
                vertices : List[Any] -> the list of vertices to be added to the graph
                complete : bool      -> if true, then the new graph is assummed to be a complete graph (i.e. every vertex is connected to every other with weight 1).
            """
        if not isinstance(complete, bool):
            raise TypeError("connected must be of type bool")
        if not isinstance(vertices, List) and not isinstance(vertices, Tuple):
            raise TypeError("vertices must be a collection")

        for v in vertices:
            self.addVertex(v)

        if complete:
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    self.incrementEdgeWeight(vertices[i], vertices[j], 1)


    def empty(self):
        return self.graph == {}

    def save(self, filename: str):
        """Saves the graph to a binary file.

            Parameters:
                filename : str -> the name of the file
        """

        if not isinstance(filename, str):
            raise TypeError("filename must be a string")
        pickle.dump(self.graph, open(filename, "wb"))

    def load(self, filename: str):
        """Loads the data into the graph from a binary file.

            Parameters:
                filename : str -> the name of the file to load from
        """

        if not isinstance(filename, str):
            raise TypeError("filename must be a string")
        self.graph = pickle.load(open(filename, "rb"))