
class BFS:
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
        # self.dirtsArray.append((agentX,agentY))
        # explored list covers all the tiles in the grid as booleans
        explored = [[False for x in range(len(self.tilesArray[0]))] for y in range(len(self.tilesArray))]
        currentTile = self.tilesArray[agentX][agentY]
        self.prev = [[None for x in range(len(self.tilesArray[0]))] for y in range(len(self.tilesArray))]
        frontier.append(currentTile)
        while len(frontier) != 0:
            currentTile = frontier.pop(0) #popping the first tile
            if currentTile.isDirty:
                self.tilesArray[currentTile.x][currentTile.y].isDirty=False
                self.dirtsArray.append((currentTile.x,currentTile.y))
            explored[currentTile.x][currentTile.y] = True
            neighbors = self.getNeighbours(currentTile,self.tilesArray)
            for tile in neighbors:
                if(not explored[tile.x][tile.y]):
                    explored[tile.x][tile.y]=True
                    self.num_explored+=1
                    frontier.append(tile)
                    self.prev[tile.x][tile.y]=currentTile
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





