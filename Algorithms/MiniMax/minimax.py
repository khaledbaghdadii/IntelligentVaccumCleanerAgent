from Sprites.Dirt import Dirt


class MiniMax:
    def __init__(self):
        self.scores=[]
        pass

    
    def getDistance(self,x1,y1,x2,y2):
        return abs(y2-y1)+abs(x2-x1)
    def getScore(self,cleaningAgentTile,dirts_array):
        score=0
        agent_on_dirt=False
        for i in range(len(dirts_array)):
            dirt=dirts_array[i]
            # print("Dirts array: ",dirts_array)
            dirtX=dirt[0]
            dirtY=dirt[1]
            #vacuum_position is a tuple in the form of (x,y)
            vacuumX=cleaningAgentTile.x 
            vacuumY=cleaningAgentTile.y
            if(self.getDistance(vacuumX,vacuumY,dirtX,dirtY)==0):
                agent_on_dirt=True
            score=score+self.getDistance(vacuumX,vacuumY,dirtX,dirtY)
        return score,agent_on_dirt
    def getMin(self,arr):
        min=1234865
        index=0
        for i in range  (len(arr)):
            if arr[i]<min and arr[i]!=0:
                min=arr[i]
                index=i
        return min,index


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
    

    #move and consider adding dirt
    def dirtAgentMove(self,dx,dy,newX,newY):
        self.dirt_agent.move(dx,dy)
        if self.dirt_agent.count%3==0:
            self.tiles_object.addDirtXY(newX,newY)
            self.dirts_object.addDirtXY(newX,newY)
    def minimax(self,maximizing_player,depth,cleaning_agent_tile,dirt_agent_tile,tiles_array,dirts_array,count):
        if(depth==0):
            print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScore(cleaning_agent_tile,dirts_array)[0],None,None
        if(not maximizing_player):
            minEval= 9999999999
            tilee=cleaning_agent_tile
            cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array)
            for neighbour in cleaning_agent_neighbours:
                
                cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                if (neighbour.x,neighbour.y) in dirts_array:
                    index= dirts_array.index((neighbour.x,neighbour.y))
                    dirts_array.pop(index)
                eval= self.minimax(True,depth-1,cleaningAgentNextTile,dirt_agent_tile,tiles_array,dirts_array,count)[0]
                if eval<minEval:
                    minEval=eval
                    tilee=cleaningAgentNextTile
                else:
                    pass
            return minEval,tilee,dirt_agent_tile
        if(maximizing_player):
            maxEval=-9999999999
            dtile=dirt_agent_tile
            dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array)
            for neighbour in dirt_agent_neighbours:
                dirtAgentNextPos=(neighbour.x,neighbour.y)
                dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                
                if count%3==0:
                    d=(Dirt(dirtAgentNextPos[0],dirtAgentNextPos[1]))
                    dirts_array.append((d.x,d.y))
                    tiles_array[dirtAgentNextPos[0]][dirtAgentNextPos[1]].isDirty=True
                eval=self.minimax(False,depth-1,cleaning_agent_tile,dirtAgentNextTile,tiles_array,dirts_array,count+1)[0]
                if eval>maxEval: 
                    maxEval=eval
                    dtile=dirtAgentNextTile
                else:
                    pass
            return maxEval,None,dtile





                


    # def minimax(self,dirt_agent_count,cleaning_agent_tile,dirt_agent_tile,tiles_array,dirts_array,score,current_depth,max_depth,scores=[],tiles_state=[]):
    #     if(current_depth==max_depth):
    #         return score,tiles_array
    #     cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array)
    #     dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array)



    #     for neighbour in cleaning_agent_neighbours:
    #         cleaningAgentNextPos=(neighbour.x,neighbour.y)
    #         cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
    #         if dirt_agent_count%3==0:
    #             addDirt=True
                
    #         else:
    #             addDirt=False
    #         dirt_agent_count+=1
    #         for dirt_agent_neighbour in dirt_agent_neighbours:
    #             dirtAgentNextPos=(dirt_agent_neighbour.x,dirt_agent_neighbour.y)
    #             dirtAgentNextTile=tiles_array[dirt_agent_neighbour.x][dirt_agent_neighbour.y]
    #             if addDirt:
    #                 d=(Dirt(dirtAgentNextPos[0],dirtAgentNextPos[1]))
    #                 print("Dirtttt: ",d)
    #                 dirts_array.append(d)
    #                 tiles_array[dirtAgentNextPos[0]][dirtAgentNextPos[1]].isDirty=True
    #             # self.dirt_agent.addDirtXY(dirtAgentNextPos[0],dirtAgentNextPos[1])
    #             s=self.getScore(cleaningAgentNextPos,dirts_array)

    #             self.scores.append(self.minimax(dirt_agent_count,cleaningAgentNextTile,dirtAgentNextTile,tiles_array,dirts_array,score+s,current_depth+1,max_depth,scores,tiles_state)[0])
    #             #the name is not relevant/ initia;y it used to give state of tiles now it is a list to store cleaning agent position at the current state
    #             tiles_state.append(cleaningAgentNextPos)
                
    #             if addDirt:
    #                 dirts_array.pop()
    #                 tiles_array[dirtAgentNextPos[0]][dirtAgentNextPos[1]].isDirty=False
    #     if(current_depth==0):
    #         return self.getResult()


    def getResult(self):
        minScore,minIndex=self.getMin(self.scores)
        return minScore,minIndex




    
        






        
