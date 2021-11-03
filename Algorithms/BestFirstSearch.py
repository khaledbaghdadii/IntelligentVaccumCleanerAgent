from heapq import heapify
import pygame
import constants
from Sprites.Tiles import Tiles
# This class represent a graph
class Graph:
    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()
    # Create an undirected graph by adding symmetric edges
    def make_undirected(self):
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.graph_dict.setdefault(b, {})[a] = dist
    # Add a link from A and B of given distance, and also add the inverse link if the graph is undirected
    def connect(self, A, B, distance=1):
        self.graph_dict.setdefault(A, {})[B] = distance
        if not self.directed:
            self.graph_dict.setdefault(B, {})[A] = distance
    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)
    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
# This class represent a node
class Node:
    # Initialize the class
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost
    # Compare nodes
    def __eq__(self, other):
        return self.name == other.name
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))
# Best-first search
def best_first_search(graph, heuristics, start, end):
    num_explored=0
    moves=0
    # Create lists for open nodes and closed nodes
    open = []
    closed = []
    # Create a start node and an goal node
    start_node = Node(start, None)
    goal_node = Node(end, None)
    # Add the start node
    open.append(start_node)
    
    # Loop until the open list is empty
    while len(open) > 0:
        # Sort the open list to get the node with the lowest cost first
        open.sort()
        # Get the node with the lowest cost
        current_node = open.pop(0)
        num_explored+=1
        # Add the current node to the closed list
        closed.append(current_node)
        
        # Check if we have reached the goal, return the path
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append((int(current_node.name[0]),(int(current_node.name[1]))))
                current_node = current_node.parent
            path.append((int(start_node.name[0]),int((start_node.name[1]))))
            # Return reversed path
            return path[::-1], num_explored
        # Get neighbours
        neighbors = graph.get(current_node.name)
        # Loop neighbors
        for key, value in neighbors.items():
            # Create a neighbor node
            neighbor = Node(key, current_node)
            # Check if the neighbor is in the closed list
            if(neighbor in closed):
                continue
            # Calculate cost to goal
            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.h
            # Check if neighbor is in open list and if it has a lower f value
            if(add_to_open(open, neighbor) == True):
                # Everything is green, add neighbor to open list
                open.append(neighbor)
    # Return None, no path is found
    return None
# Check if a neighbor should be added to open list
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f >= node.f):
            return False
    return True
# The main entry point for this module
def generateGraph(tiles_object):
    # Create a graph
    graph = Graph()
    heuristics = {}
    for i,tiles in enumerate(tiles_object.tiles):
        for j,tile in enumerate(tiles):
            if(not tile.has_walls_right):
                graph.connect((str(i)+str(j)),(str(i+1)+str(j)),1)
            if(not tile.has_walls_up):
                graph.connect((str(i)+str(j)),(str(i)+str(j-1)),1)
            if(not tile.has_walls_down):
                graph.connect((str(i)+str(j)),(str(i)+str(j+1)),1)
            if(not tile.has_walls_left):
                graph.connect((str(i)+str(j)),(str(i-1)+str(j)),1)
            heuristics[(str(i)+str(j))]=1
    
    return graph,heuristics

def generatePaths(graph,heuristics,nodes_path):
    paths=[]
    num_explored=0
    moves=0
    # Run search algorithm
    for i in range(len(nodes_path)-1):
        path,explored = best_first_search(graph, heuristics, str(nodes_path[i][0])+str(nodes_path[i][1]), str(nodes_path[i+1][0])+str(nodes_path[i+1][1]))
        paths.append(path)
        num_explored+=explored
        moves+=len(path)-1

    return paths,num_explored,moves
    
# Tell python to run main method
