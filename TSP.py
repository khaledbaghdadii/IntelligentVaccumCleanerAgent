# Python3 program to implement traveling salesman
# problem using naive approach.
from sys import maxsize
import sys
import queue
from Tiles import Tiles
from BFS import BFS
from VacuumCleaner import VacuumCleaner
from itertools import permutations
import pygame
import constants
from BestFirstSearch import generateGraph,generatePaths

class Cell  :
    def __init__(self, x, y, dist, prev) :
        self.x = x
        self.y = y
        self.dist = dist; #distance to start
        self.prev = prev; #parent cell in the path
 
    def __str__(self):
        return "("+ str(self.x) + "," + str(self.y) + ")" 

def createGraph(tiles, agent):
    nodes=[] #dirt nodes of the graph

    for tiless in tiles:
        for tile in tiless:
            if not tile.isDirty:
                pass
            else:
                nodes.append((tile.x,tile.y))

    nodes.insert(0,(agent.x,agent.y))

    graph=[[0 for x in range(len(nodes))] for y in range(len(nodes))]
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            dist=abs(nodes[i][0]-nodes[j][0])+abs(nodes[i][1]-nodes[j][1])
            graph[i][j]=dist
    
    return graph,nodes


# # implementation of traveling Salesman Problem
def travellingSalesmanProblem(graph, nodes):
    # store all vertex apart from source vertex
    vertex = []
    path = []
    s=0
    nodePath=[]
    # path.append(s)
    V=len(nodes)
    for i in range(V):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation=permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        k = s

        for j in i:
            current_pathweight += graph[k][j]
            k = j
        current_pathweight += graph[k][s]

        # update minimum
        if current_pathweight<min_path:
            path=i

        # nodePath.append(nodes[s])

        min_path = min(min_path, current_pathweight)

    nodePath.append(nodes[s])
    for m in list(path):
        nodePath.append(nodes[m])

    return min_path, nodePath

def generatePathsList(tiles_object,vacuum):
    graph,nodes=createGraph(tiles_object.tiles,vacuum)
    min_path,nodes_path=travellingSalesmanProblem(graph,nodes)
    adjacency_matrix,heuristics=generateGraph(tiles_object)
    paths=generatePaths(adjacency_matrix,heuristics,nodes_path)
    return paths




