from Queue import PriorityQueue


class GreedyAlgo:
    prev=[[]]
    path=[[]]

    def __init__(self,tilesArray):
        self.tilesArray=tilesArray
        self.dirtsArray=[]
        self.prev=[[]]
        self.path=[[]]


    def clean(self,agentX,agentY):
        frontier = PriorityQueue()
        self.dirtsArray.append((agentX,agentY))
        # explored list covers all the tiles in the grid as booleans
        explored = [[False for x in range(len(self.tilesArray[0]))] for y in range(len(self.tilesArray))]
        currentTile = self.tilesArray[agentX][agentY]
        # start = (currentTile.x,currentTile.y)
        self.prev = [[None for x in range(len(self.tilesArray[0]))] for y in range(len(self.tilesArray))]

        frontier.put((currentTile,currentTile.x,currentTile.y),0)
        came_from = dict()
        cost_so_far = dict()
        came_from[(currentTile,currentTile.x,currentTile.y)] = None
        cost_so_far[(currentTile,currentTile.x,currentTile.y)] = 0
        print("COst so far ",cost_so_far)

        while not frontier.empty():
            currentTile = frontier.get() #popping the first tile
            if currentTile[0].isDirty:
                self.tilesArray[currentTile[0].x][currentTile[0].y].isDirty=False
                self.dirtsArray.append((currentTile[0].x,currentTile[0].y))
                print("added")
            explored[currentTile[0].x][currentTile[0].y] = True
            neighbors = self.getNeighbours(currentTile[0],self.tilesArray)
            for tile in neighbors:
                new_cost = cost_so_far[currentTile] + 1
                # print("new cost")
                # print(new_cost)
                # print(type(new_cost))
                # print("cost so far")
                # print(cost_so_far[(tile,tile.x,tile.y)])
                # print(type(cost_so_far[(tile,tile.x,tile.y)]))
                if tile not in cost_so_far:
                    cost_so_far[(tile,tile.x,tile.y)]=0
                if tile not in cost_so_far or new_cost < cost_so_far[(tile,tile.x,tile.y)]:
                    cost_so_far[tile] = new_cost
                    priority = new_cost
                    frontier.put(tile, priority)
                    came_from[tile] = currentTile
                    if (tile.isDirty):
                        self.tilesArray[tile.x][tile.y].isDirty=False
                        self.dirtsArray.append((tile.x,tile.y))

                        self.path.append(self.backtrack(tile))
                        return self.clean(tile.x,tile.y)
        return []

    def backtrack(self,endTile):
        path=[]
        path.append(endTile)
        prevTile=self.prev[endTile.x][endTile.y]
        while prevTile!=None:
            path.append(prevTile)
            prevTile = self.prev[prevTile.x][prevTile.y]
        path.reverse()

        return path
    

    def getDirts(self):
        return self.dirtsArray
    def getNeighbours(self,currentTile,tilesArray):
        neighbours = []
        if(not currentTile.hasWallLeft()):
            a = currentTile.x-1
            b = currentTile.y
            # in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        if(not currentTile.hasWallRight()):
            a = currentTile.x+1
            b = currentTile.y
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        if(not currentTile.hasWallUp()):
            a = currentTile.x
            b = currentTile.y-1
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        if(not currentTile.hasWallDown()):
            a = currentTile.x
            b = currentTile.y+1
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        return neighbours