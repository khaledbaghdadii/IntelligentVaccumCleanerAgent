from Tiles import Tiles
import pygame
import constants
from queue import PriorityQueue
v = 14
graph = [[] for i in range(v)]

# Function For Implementing Best First Search
# Gives output path having lowest cost


def best_first_search(source, target, n):
	visited = [0] * n
	visited = True
	pq = PriorityQueue()
	pq.put((0, source))
	while pq.empty() == False:
		u = pq.get()[1]
		# Displaying the path having lowest cost
		print(u, end=" ")
		if u == target:
			break

		for v, c in graph[u]:
			if visited[v] == False:
				visited[v] = True
				pq.put((c, v))
	print()

# Function for adding edges to graph


def addedge(x, y, cost):
	graph[x].append((y, cost))
	graph[y].append((x, cost))


# The nodes shown in above example(by alphabets) are
# implemented using integers addedge(x,y,cost);

source = 0
target = 9
best_first_search(source, target, v)

# This code is contributed by Jyotheeswar Ganne







pygame.init()
BG_COLOR = constants.BG_COLOR
lock = pygame.time.Clock()
pygame.display.set_caption("{}".format(constants.TITLE))
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
font = pygame.font.Font(None, 40)
tiles_object=Tiles(4,5)
tiles_object.addDirtXY(0,2,True)
tiles_object.addDirtXY(3,4,True)
tiles_object.addDirtXY(3,2,True)
tiles_object.addDirtXY(1,3,True)
#Describe your graph here  


dict={}
for i,tiles in enumerate(tiles_object.tiles):
    for j,tile in enumerate(tiles):
        key="A"+str(i)+str(j)
        dict[key]=[]
        if(not tile.has_walls_right):
            addedge(i+1,j,1)
        if(not tile.has_walls_up):
            addedge(i+1,j-1,1)
        if(not tile.has_walls_down):
            addedge(i,j+1,1)
        if(not tile.has_walls_left):
            neighbor=(("A"+str(i-1)+str(j)),1)
            dict[key].append(neighbor)
print()
print()
print()
print()
Graph_nodes=dict
aStarAlgo("A00","A02")

print(dict)



