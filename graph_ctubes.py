from ctubes import *

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return str(self.src) + '->' + str(self.dest)

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight = 1.0):
        self.src = src
        self.dest = dest
        self.weight = weight
    def getWeight(self):
        return self.weight
    def __str__(self):
        return str(self.src) + '->(' + str(self.weight) + ')'\
            + str(self.dest)

class Digraph(object):
    def __init__(self):
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def getEdges(self):
        return self.edges
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = res + str(k) + '->' + str(d) + '\n'
        return res[:-1]

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


def printPath(path):
    # a path is a list of nodes
    result = ''
    for i in range(len(path)):
        if i == len(path) - 1:
            result = result + str(path[i])
        else:
            result = result + str(path[i]) + '->'
    return result

def genGraph(segments):
    """
    Returns a graph object with all the Nodes and Edges.
    segments: List of carbon tubes objects
    """
    graph = Graph() #initializing graph object
    for segment in segments:   #for each segment
        for node in segment.getIntersects().values():
            if not graph.hasNode(node):
                graph.addNode(node)
    for segment in segments:
        nodelist = segment.getIntersects().values()
        for i in range(len(nodelist) - 1):
            for j in range(i + 1, len(nodelist)):
                edge = Edge(nodelist[i], nodelist[j])
                graph.addEdge(edge)
    return graph

def plotGraph(graph):
    """
    Plots the graph using object 'graph'.
    """
    plt.figure()
    edges = graph.getEdges()    #dictionary with {src:[dest1, dest2], ... }
    for src in edges.keys():
        destlist = edges[src]   #list of [dest1, dest2,..] for given src
        for dest in destlist:
            xi, yi = src.getPos()
            xf, yf = dest.getPos()
            x = [xi, xf]
            y = [yi, yf]
            plt.plot(x, y)
    plt.title("Graph represntation")
    plt.axis([-2.,12,-2.,12])

def DFS(graph, start, end, path = [], shortest = None):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    #print 'Current dfs path:', printPath(path)
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            newPath = DFS(graph,node,end,path,shortest)
            if newPath != None:
                return newPath

def DFSShortest(graph, start, end, path = [], shortest = None):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    #print 'Current dfs path:', printPath(path)
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            if shortest == None or len(path)<len(shortest):
                newPath = DFSShortest(graph,node,end,path)
                if newPath != None:
                    shortest = newPath
    return shortest

def BFS(graph, start, end, q = []):
    initPath = [start]
    q.append(initPath)
    while len(q) != 0:
        tmpPath = q.pop(0)
        lastNode = tmpPath[len(tmpPath) - 1]
        #print 'Current dequeued path:', printPath(tmpPath)
        if lastNode == end:
            return tmpPath
        for linkNode in graph.childrenOf(lastNode):
            if linkNode not in tmpPath:
                newPath = tmpPath + [linkNode]
                q.append(newPath)
    return None

def plotpath(path):
    """
    Plots path from the given list 'path'
    """
    plt.figure()
    x = []
    y = []
    for node in path:
        x.append(node.getPos()[0])
        y.append(node.getPos()[1])
    plt.plot(x, y)
    plt.title("Final path")
    plt.axis([-2.,12,-2.,12])
    
if __name__ == '__main__':
    seglist = generateseg(10, 15, (10,10))
    initial = seglist[0]
    final = seglist[1]
    c = intersect(seglist)
    print c
    plotseg(seglist, (12,12), "All segments")
    intersecting = getIntersects(seglist)
    plotseg(intersecting, (10, 10), "Only Intersecting")
    graph = genGraph(seglist)
    print len(graph.nodes)
    #print graph
    plotGraph(graph)
    print "left intersects =", initial.getIntersects().values()
    print "right intersects = ", final.getIntersects().values() 
    for start in initial.getIntersects().values():
        for end in final.getIntersects().values():
            path = BFS(graph, start, end)
            if path != None:
                plotpath(path)
    plt.show()
    
    
