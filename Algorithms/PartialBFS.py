
class PartialBFS:
    prev=[[]]
    path=[[]]

    def __init__(self,tilesArray,agentX,agentY,visibleTiles):
        self.tilesArray=tilesArray #We use this copy to access the location of the tile in the original dimension, we also use
        #it to set the isDirty flag to False (clean)
        self.dirtsArray=[]
        self.prev=[[]]
        self.path=[[]]
        self.moves=0
        self.num_explored=0
        self.visibleTiles=visibleTiles
        self.agentX=agentX
        self.agentY=agentY
        if len(visibleTiles)%2==0:
            self.newAgentX= int(len(visibleTiles)/2)-1
        else:
            self.newAgentX= int(len(visibleTiles)/2)
        if len(visibleTiles[0])%2==0:
            self.newAgentY = int(len(visibleTiles[0])/2)-1
        else:
            self.newAgentY = int(len(visibleTiles[0])/2)
    def clean(self):
        frontier = []
        # self.dirtsArray.append((agentX,agentY))
        # explored list covers all the tiles in the grid as booleans
        explored = [[False for x in range(len(self.visibleTiles[0]))] for y in range(len(self.visibleTiles))]
        currentTile = (self.tilesArray[self.agentX][self.agentY],self.newAgentX,self.newAgentY)
        self.prev = [[None for x in range(len(self.visibleTiles[0]))] for y in range(len(self.visibleTiles))]
        frontier.append(currentTile)
        while len(frontier) != 0:
            currentTile = frontier.pop(0) #popping the first tile
            if currentTile[0].isDirty:
                self.tilesArray[currentTile[0].x][currentTile[0].y].isDirty=False
                self.dirtsArray.append((currentTile[0].x,currentTile[0].y))
            explored[currentTile[1]][currentTile[2]] = True
            neighbors = self.getNeighbours(currentTile,self.visibleTiles)
            for tile in neighbors:
                if(not explored[tile[1]][tile[2]]):
                    explored[tile[1]][tile[2]]=True
                    self.num_explored+=1
                    frontier.append(tile)
                    self.prev[tile[1]][tile[2]]=currentTile
                    if (tile[0].isDirty):
                        self.tilesArray[tile[0].x][tile[0].y].isDirty=False
                        self.dirtsArray.append((tile[0].x,tile[0].y))

                        self.path.append(self.backtrack(tile))
                        self.newAgentX=tile[1]
                        self.newAgentY=tile[2]
                        self.agentX=tile[0].x
                        self.agentY=tile[0].y
                        return self.clean()

        return []

    def backtrack(self,endTile):
        path=[]
        path.append(endTile[0])
        # self.tilesArray[endTile[0].x][endTile[0].y].isVisited = True
        prevTile=self.prev[endTile[1]][endTile[2]]
        while prevTile!=None:
            path.append(prevTile[0])
            # self.tilesArray[prevTile[0].x][prevTile[0].y].isVisited = True
            prevTile = self.prev[prevTile[1]][prevTile[2]]
        path.reverse()
        self.moves+=len(path)
        return path

    def getDirts(self):
        return self.dirtsArray
    def getNeighbours(self,currentTile,visibleTiles):
        neighbours = []
        if(not currentTile[0].hasWallLeft() and currentTile[1]>0):
            a = currentTile[1]-1
            b = currentTile[2]
            # in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append((visibleTiles[a][b],a,b))
        if(not currentTile[0].hasWallRight() and currentTile[1]<len(visibleTiles)-1):
            a = currentTile[1]+1
            b = currentTile[2]
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append((visibleTiles[a][b],a,b))
        if(not currentTile[0].hasWallUp() and currentTile[2]>0):
            a = currentTile[1]
            b = currentTile[2]-1
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append((visibleTiles[a][b],a,b))
        if(not currentTile[0].hasWallDown() and currentTile[2]<len(visibleTiles[0])-1):
            a = currentTile[1]
            b = currentTile[2]+1
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append((visibleTiles[a][b],a,b))
        return neighbours





