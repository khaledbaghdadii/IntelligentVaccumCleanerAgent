from Algorithms.PartialBFS import PartialBFS
import random as rnd
class PartiallyObservable:

    def __init__(self,tilesArray):
        self.tilesArray=tilesArray
        self.dirtsArray=[]
        # self.prev=[[]]
        self.path=[[]]
        self.agent = None
        # self.moves=0
        # self.num_explored=0

    def clean(self,agentX,agentY):
        radius=1
        currentAgentX=agentX
        currentAgentY=agentY
        self.tilesArray[currentAgentX][currentAgentY].isVisited=True
        visibleTiles,visibleTilesTuples=self.getVisibleTiles(radius,currentAgentX,currentAgentY)
        while(self.allScanned(self.tilesArray)==False):
            lastTile=None
            self.tilesArray[currentAgentX][currentAgentY].isVisited=True
            bfs=PartialBFS(self.tilesArray,currentAgentX,currentAgentY,visibleTiles)
            bfs.clean()
            dirts = bfs.getDirts()
            for dirt in dirts:
                self.dirtsArray.append(dirt)
            path = bfs.path
            # self.tilesArray[currentAgentX][currentAgentY].isVisited=True
            for subpath in path:
                if len(subpath)>=1:
                    self.path.append(subpath)
                    for i in subpath:
                        self.tilesArray[i.x][i.y].isVisited = True
            lastpath = path[len(path)-1]
            if len(lastpath)==0: # visible array is cleam

                print("empty last path")
                #go to last unvisited
                #get neighbors of the current tile in the visible tiles array
                #check if one of them is not visited -> your next move
                #if all are visited, go randomly
                neighbors = self.getNeighbours(self.tilesArray[currentAgentX][currentAgentY],self.tilesArray)
                # shuffled_neighbors = rnd.sample(neighbors,len(neighbors))
                for tilee in neighbors:
                    if (((tilee.x,tilee.y) in visibleTilesTuples) and tilee.isVisited==False):
                        # self.tilesArray[tilee.x][tilee.y].count-=1 #can visit the tile twice
                        lastTile=tilee
                        break
                if lastTile == None: # no unvisited neighbor
                    # break
                    shuffled_neighbors = rnd.sample(neighbors,len(neighbors)) #select  random neighbor if it is visible
                    for i in shuffled_neighbors:
                        if((i.x,i.y) in visibleTilesTuples):
                            # self.tilesArray[i.x][i.y].count-=1
                            lastTile=i
                            break

                if lastTile == None:
                    break
                self.path.append([self.tilesArray[currentAgentX][currentAgentY],lastTile])
            else:
                lastTile=lastpath[len(lastpath)-1]

            currentAgentX=lastTile.x
            currentAgentY=lastTile.y
            self.tilesArray[currentAgentX][currentAgentY].isVisited=True
            visibleTiles,visibleTilesTuples=self.getVisibleTiles(radius,currentAgentX,currentAgentY)
        print("DONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")


    def allScanned(self,tilesArray):
        for i in tilesArray:
            for j in i:
                if j.isVisited==False and j.possibleVisible==True:
                    return False
        return True # if there are no more tiles that can be seen and are still not visited

    def getVisibleTiles(self,radius,agentX,agentY):
        startX= agentX-radius
        startY= agentY-radius
        endX= agentX+radius
        endY= agentY+radius
        if startX<0:
            startX=0
        if startY<0:
            startY=0
        if endX>len(self.tilesArray)-1:
            endX=len(self.tilesArray)-1
        if endY>len(self.tilesArray[0])-1:
            endY=len(self.tilesArray[0])-1
        # visibleTiles = [self.tilesArray[i][startX:endX+1] for i in range(startY,endY+1)]
        visibleTiles=[]
        visibleTilesTuples=[]
        for i in range(startX,endX+1):
            temp=[]
            for j in range(startY,endY+1):
                # self.tilesArray[i][j].possibleVisible=True
                temp.append(self.tilesArray[i][j])
                visibleTilesTuples.append((self.tilesArray[i][j].x,self.tilesArray[i][j].y))
            visibleTiles.append(temp)
        return visibleTiles,visibleTilesTuples

    def getNeighbours(self,currentTile,tilesArray):
        neighbours = []
        if(not currentTile.hasWallLeft()):
            a = currentTile.x-1
            b = currentTile.y
            self.tilesArray[a][b].possibleVisible=True
            # in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        else:
            to_be_updated = [self.tilesArray[i][currentTile.y]for i in range(0,currentTile.x)]
            for tile in to_be_updated:
                self.tilesArray[tile.x][tile.y].possibleVisible=False
        if(not currentTile.hasWallRight()):
            a = currentTile.x+1
            b = currentTile.y
            self.tilesArray[a][b].possibleVisible=True
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        else:
            to_be_updated = [self.tilesArray[i][currentTile.y]for i in range(currentTile.x+1,len(self.tilesArray))]
            for tile in to_be_updated:
                self.tilesArray[tile.x][tile.y].possibleVisible=False
        if(not currentTile.hasWallUp()):
            a = currentTile.x
            b = currentTile.y-1
            self.tilesArray[a][b].possibleVisible=True
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        else:
            to_be_updated = [self.tilesArray[currentTile.x][i]for i in range(0,currentTile.y)]
            for tile in to_be_updated:
                self.tilesArray[tile.x][tile.y].possibleVisible=False
        if(not currentTile.hasWallDown()):
            a = currentTile.x
            b = currentTile.y+1
            self.tilesArray[a][b].possibleVisible=True
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        else:
            to_be_updated = [self.tilesArray[currentTile.x][i]for i in range(currentTile.y+1,len(self.tilesArray[0]))]
            for tile in to_be_updated:
                self.tilesArray[tile.x][tile.y].possibleVisible=False

        # if there is a corner, it wont see behind it
        # if(currentTile.hasWallDown()):
        #     if(currentTile.hasWallRight):
        #         for i in range(currentTile.x+1,len(self.tilesArray)):
        #             for j in range(currentTile.y+1,len(self.tilesArray[0])):
        #                 self.tilesArray[i][j].possibleVisible = False
        #     if(currentTile.hasWallLeft):
        #         for i in range(0,currentTile.x):
        #             for j in range(currentTile.y+1,len(self.tilesArray[0])):
        #                 self.tilesArray[i][j].possibleVisible = False
        #
        # if(currentTile.hasWallUp()):
        #     if(currentTile.hasWallRight):
        #         for i in range(currentTile.x+1,len(self.tilesArray)):
        #             for j in range(0,currentTile.y):
        #                 self.tilesArray[i][j].possibleVisible = False
        #     if(currentTile.hasWallLeft):
        #         for i in range(0,currentTile.x):
        #             for j in range(0,currentTile.y):
        #                 self.tilesArray[i][j].possibleVisible = False





        return neighbours

    def getDirts(self):
        return self.dirtsArray