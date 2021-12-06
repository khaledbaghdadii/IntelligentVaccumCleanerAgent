from Sprites.Dirt import Dirt


class MiniMax:
    def __init__(self):
        self.scores=[]
        pass

    
    def getDistance(self,x1,y1,x2,y2):
        return abs(y2-y1)+abs(x2-x1)
    def getScore(self,cleaningAgentTile,dirts_array):
        score=0
        for i in range(len(dirts_array)):
            dirt=dirts_array[i]
            print("Dirts array: ",dirts_array)
            dirtX=dirt[0]
            dirtY=dirt[1]
            #vacuum_position is a tuple in the form of (x,y)
            vacuumX=cleaningAgentTile.x 
            vacuumY=cleaningAgentTile.y
            score=score+self.getDistance(vacuumX,vacuumY,dirtX,dirtY)
        return score
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
            return self.getScore(cleaning_agent_tile,dirts_array),cleaning_agent_tile
        if(not maximizing_player):
            minEval= 999999
            cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array)
            for neighbour in cleaning_agent_neighbours:
                cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                eval,tile= self.minimax(True,depth-1,cleaningAgentNextTile,dirt_agent_tile,tiles_array,dirts_array,count)
                if eval<minEval:
                    return eval,cleaningAgentNextTile
                else:
                    return minEval,cleaning_agent_tile
        if(maximizing_player):
            maxEval=-99999
            dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array)
            for neighbour in dirt_agent_neighbours:
                dirtAgentNextPos=(neighbour.x,neighbour.y)
                dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                if count%3==0:
                    d=(Dirt(dirtAgentNextPos[0],dirtAgentNextPos[1]))
                    dirts_array.append((d.x,d.y))
                    tiles_array[dirtAgentNextPos[0]][dirtAgentNextPos[1]].isDirty=True
                eval,tilee=self.minimax(False,depth-1,cleaning_agent_tile,dirtAgentNextTile,tiles_array,dirts_array,count+1)
                if eval>maxEval: 
                    return eval,cleaning_agent_tile
                else:
                    return maxEval,cleaning_agent_tile





                


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




    
        






        
