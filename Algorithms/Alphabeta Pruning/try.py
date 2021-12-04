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
    def getScore(self,vacuum_position):
        dirts_array=self.dirts_object.dirts
        score=0
        for i in range(len(dirts_array)):
            dirt=dirts_array[i]
            dirtX=dirt.x
            dirtY=dirt.y
            #vacuum_position is a tuple in the form of (x,y)
            vacuumX=vacuum_position[0] 
            vacuumY=vacuum_position[1]
            score=score+1/self.getDistance(vacuumX,vacuumY,dirtX,dirtY)
        return score

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

    def move(self,cleaning_agent,dirt_agent,tiles_array,dirts_array):
        cleaning_agent_tile= self.tiles_array[cleaning_agent.x][cleaning_agent.y]
        cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array)
        dirt_agent_tile= self.tiles_array[dirt_agent.x][dirt_agent.y]
        dirt_agent_neighbours = self.getNeighbours(dirt_agent,tiles_array)



        for neighbour in cleaning_agent_neighbours:
            cleaningAgentNextPos=(neighbour.x,neighbour.y)
            for dirt_agent_neighbour in dirt_agent_neighbours:
                dirtAgentNextPos=(dirt_agent_neighbour.x,dirt_agent_neighbour.y)
                self.dirt_agent.addDirtXY(dirtAgentNextPos[0],dirtAgentNextPos[1])
                self.getScore(cleaning_agent)
                self.dirt_agent.removeDirtXY(dirtAgentNextPos[0],dirtAgentNextPos[1])






        
