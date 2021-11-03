from queue import PriorityQueue


class Djikstra:
    prev=[[]]
    path=[[]]

    def __init__(self,tilesArray):
        self.tilesArray=tilesArray
        self.dirtsArray=[]
        self.prev=[[]]
        self.path=[[]]
        self.moves=0
        self.num_explored=0

    def clean(self,agentX,agentY):
        frontier = []
        self.dirtsArray.append((agentX,agentY))
        # explored list covers all the tiles in the grid as booleans
        explored = [[False for x in range(len(self.tilesArray[0]))] for y in range(len(self.tilesArray))]
        currentTile = self.tilesArray[agentX][agentY]
        start = (currentTile.x,currentTile.y)
        self.prev = [[None for x in range(len(self.tilesArray[0]))] for y in range(len(self.tilesArray))]

        frontier.append((0,currentTile))
        frontier.sort(reverse=True)
        came_from = dict()
        cost_so_far = dict()
        # came_from[currentTile] = None
        # cost_so_far[currentTile] = 0
        came_from[start] = None
        cost_so_far[start] = 0

        while len(frontier)!=0:
            currentTile = frontier.pop(0)[1] #popping the first tile
            cT = (currentTile.x,currentTile.y)
            if currentTile.isDirty:
                self.tilesArray[currentTile.x][currentTile.y].isDirty=False
                self.dirtsArray.append((currentTile.x,currentTile.y))
                print("added")
            explored[currentTile.x][currentTile.y] = True
            self.num_explored+=1
            neighbors = self.getNeighbours(currentTile,self.tilesArray)
            for tile in neighbors:
                tileT = (tile.x,tile.y)

                new_cost = cost_so_far[cT] + 1
                # print(new_cost)
                if tileT in cost_so_far.keys():
                    isIt = True
                    id = new_cost < int(cost_so_far[tileT])
                else: isIt = False
                if (tileT not in cost_so_far.keys()) or (id):
                    cost_so_far[tileT] = new_cost
                    # print("COst so far ",cost_so_far)
                    priority = new_cost
                    frontier.append((priority,tile))
                    frontier.sort(key=lambda x: x[0])
                    came_from[tileT] = currentTile
                    #self.path.append(currentTile)
                    
                
                    if (tile.isDirty):
                        self.tilesArray[tile.x][tile.y].isDirty=False
                        self.dirtsArray.append((tile.x,tile.y))
                        self.path.append(self.backtrack(tile,came_from))
                        print(tile.x,tile.y)
                       # print(self.path) 
                        return self.clean(tile.x,tile.y)
                           
        return []

    def backtrack(self,endTile,came_from):
        path=[]
        path.append(endTile)
        prevTile=came_from[(endTile.x,endTile.y)]
        while prevTile!=None:
            path.append(prevTile)
            prevTile=came_from[(prevTile.x,prevTile.y)]
        path.reverse()
        self.moves+=len(path)
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





