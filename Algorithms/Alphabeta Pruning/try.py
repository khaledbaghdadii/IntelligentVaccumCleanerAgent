from Sprites.Dirt import Dirt
from sys import maxint

class MiniMax:
    def __init__(self,cleaning_agent,dirt_agent,tiles_object,dirts_object):
        self.cleaning_agent= cleaning_agent
        self.dirt_agent=dirt_agent
        self.tiles_object=tiles_object
        self.dirts_object=dirts_object
        self.tiles_array=tiles_object.tiles
        self.dirts_array=dirts_object.dirts

    
    def getDistance(self,x1,y1,x2,y2):
        return abs(y2-y1)+abs(x2-x1)
    def getScore(self,cleaningAgentPos,dirts_array):
        score=0
        for i in range(len(dirts_array)):
            dirt=dirts_array[i]
            dirtX=dirt.x
            dirtY=dirt.y
            #vacuum_position is a tuple in the form of (x,y)
            vacuumX=cleaningAgentPos[0] 
            vacuumY=cleaningAgentPos[1]
            score=score+1/self.getDistance(vacuumX,vacuumY,dirtX,dirtY)
        return score
    def getMax(self,arr):
        max=-maxint
        index=0
        for i in range  (len(arr)):
            if arr[i]>max:
                max=arr[i]
                index=i
        return max,index


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

    def move(self,cleaning_agent_tile,dirt_agent_tile,tiles_array,dirts_array,score,current_depth,max_depth,scores=[],tiles_state=[]):
        if(current_depth==max_depth):
            return score
        cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array)
        dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array)



        for neighbour in cleaning_agent_neighbours:
            cleaningAgentNextPos=(neighbour.x,neighbour.y)
            cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
            if self.dirt_agent.count%3==0:
                addDirt=True
                
            else:
                addDirt=False
            self.dirt_agent.count+=1
            for dirt_agent_neighbour in dirt_agent_neighbours:
                dirtAgentNextPos=(dirt_agent_neighbour.x,dirt_agent_neighbour.y)
                dirtAgentNextTile=tiles_array[dirt_agent_neighbour.x][dirt_agent_neighbour.y]
                if addDirt:
                    dirts_array.append(Dirt(x=dirtAgentNextPos[0]),dirtAgentNextPos[1])
                    tiles_array[dirtAgentNextPos[0]][dirtAgentNextPos[1]].isDirty=True
                # self.dirt_agent.addDirtXY(dirtAgentNextPos[0],dirtAgentNextPos[1])
                s=self.getScore(cleaningAgentNextPos,dirts_array)

                scores.append(self.move(cleaningAgentNextTile,dirtAgentNextTile,tiles_array,dirts_array,score+s,current_depth+1,max_depth,scores,tiles_state))
                tiles_state.append(tiles_array)
                if addDirt:
                    dirts_array.pop()
                    tiles_array[dirtAgentNextPos[0]][dirtAgentNextPos[1]].isDirty=False

        maxScore,maxIndex=self.getMax(scores)
        return maxScore,tiles_state[maxIndex]
    
        






        
