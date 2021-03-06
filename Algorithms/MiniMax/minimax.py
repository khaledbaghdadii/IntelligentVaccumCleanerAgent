from Sprites.Dirt import Dirt
from copy import deepcopy

class MiniMax:
    def __init__(self,freq):
        self.scores=[]
        self.dirts_freq = freq
        pass

    
    def getDistance(self,x1,y1,x2,y2):
        return abs(y2-y1)+abs(x2-x1)
    def getScore(self,cleaningAgentTile,dirts_array):
        # print(dirts_array)
        score=0
        agent_on_dirt=False
        for i in range(len(dirts_array)):
            dirt=dirts_array[i]
            
            dirtX=dirt[0]
            dirtY=dirt[1]
            #vacuum_position is a tuple in the form of (x,y)
            vacuumX=cleaningAgentTile.x 
            vacuumY=cleaningAgentTile.y
            if(self.getDistance(vacuumX,vacuumY,dirtX,dirtY)==0):
                agent_on_dirt=True
            score=score+self.getDistance(vacuumX,vacuumY,dirtX,dirtY)
        return score,agent_on_dirt
    def getScoreMulti(self,cleaning_agents_tiles,dirts_array):
        score=0
        for cleaningAgentTile in cleaning_agents_tiles:
           for i in range(len(dirts_array)):
                dirt=dirts_array[i]
                
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

    def AgentsPos(self,agents_tiles):
        agents_pos=[]
        for agent_tile in agents_tiles:
            agent_pos=(agent_tile.x,agent_tile.y)
            agents_pos.append(agent_pos)
        return agents_pos


    def getNeighboursWalls(self,currentTile,tilesArray,cleaning_agents_tiles,dirt_agents_tiles):
        neighbours = []
        cleaning_agents_pos=self.AgentsPos(cleaning_agents_tiles)
        dirt_agents_pos=self.AgentsPos(dirt_agents_tiles)
        if(not currentTile.hasWallLeft()  and (currentTile.x-1,currentTile.y) not in cleaning_agents_pos and (currentTile.x-1,currentTile.y) not in dirt_agents_pos):
            a = currentTile.x-1
            b = currentTile.y
            # in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        if(not currentTile.hasWallRight() and (currentTile.x+1,currentTile.y) not in cleaning_agents_pos and (currentTile.x+1,currentTile.y) not in dirt_agents_pos):
            a = currentTile.x+1
            b = currentTile.y
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        if(not currentTile.hasWallUp() and (currentTile.x,currentTile.y-1) not in cleaning_agents_pos and (currentTile.x,currentTile.y-1) not in dirt_agents_pos):
            a = currentTile.x
            b = currentTile.y-1
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        if(not currentTile.hasWallDown() and (currentTile.x,currentTile.y+1) not in cleaning_agents_pos and (currentTile.x,currentTile.y+1) not in dirt_agents_pos):
            a = currentTile.x
            b = currentTile.y+1
            #in case it hits the max borders, it is handled in initializing the borders upon creation
            neighbours.append(tilesArray[a][b])
        return neighbours



    def getNeighbours(self,currentTile,tilesArray,dirt_agent_pos=(0,0),clean_agent_pos=(0,0),caller=0):
        neighbours = []
        if caller==0:
            if(not currentTile.hasWallLeft() and (currentTile.x-1,currentTile.y)!=(dirt_agent_pos)):
                a = currentTile.x-1
                b = currentTile.y
                # in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            if(not currentTile.hasWallRight() and (currentTile.x+1,currentTile.y)!=(dirt_agent_pos)):
                a = currentTile.x+1
                b = currentTile.y
                #in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            if(not currentTile.hasWallUp() and (currentTile.x,currentTile.y-1)!=(dirt_agent_pos)):
                a = currentTile.x
                b = currentTile.y-1
                #in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            if(not currentTile.hasWallDown()and (currentTile.x,currentTile.y+1)!=(dirt_agent_pos)):
                a = currentTile.x
                b = currentTile.y+1
                #in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            return neighbours
        else:
            if(not currentTile.hasWallLeft() and (currentTile.x-1,currentTile.y)!=(clean_agent_pos)):
                a = currentTile.x-1
                b = currentTile.y
                # in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            if(not currentTile.hasWallRight() and (currentTile.x+1,currentTile.y)!=(clean_agent_pos)):
                a = currentTile.x+1
                b = currentTile.y
                #in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            if(not currentTile.hasWallUp() and (currentTile.x,currentTile.y-1)!=(clean_agent_pos)):
                a = currentTile.x
                b = currentTile.y-1
                #in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            if(not currentTile.hasWallDown() and (currentTile.x,currentTile.y+1)!=(clean_agent_pos)):
                a = currentTile.x
                b = currentTile.y+1
                #in case it hits the max borders, it is handled in initializing the borders upon creation
                neighbours.append(tilesArray[a][b])
            return neighbours

    

    #move and consider adding dirt
    def dirtAgentMove(self,dx,dy,newX,newY):
        self.dirt_agent.move(dx,dy)
        if self.dirt_agent.count%self.dirts_freq==0:
            self.tiles_object.addDirtXY(newX,newY)
            self.dirts_object.addDirtXY(newX,newY)
    def minimax(self,maximizing_player,depth,cleaning_agent_tile,dirt_agent_tile,tiles_array,dirts_array,count):
        print("Dirts array: ",dirts_array)
        if(depth==0):
            # print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScore(cleaning_agent_tile,dirts_array)[0],None,None
        if(not maximizing_player):
            minEval= float('inf')
            tilee=cleaning_agent_tile
           
            cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array,(dirt_agent_tile.x,dirt_agent_tile.y),(tilee.x,tilee.y),0)
            for neighbour in cleaning_agent_neighbours:
                popped=False
                dirt_popped=(0,0)
                cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                if (neighbour.x,neighbour.y) in dirts_array:
                    index= dirts_array.index((neighbour.x,neighbour.y))
                    dirts_array.pop(index)
                    popped=True
                    dirt_popped=(neighbour.x,neighbour.y)
                eval= self.minimax(True,depth-1,cleaningAgentNextTile,dirt_agent_tile,tiles_array,(dirts_array),count)[0]
                if popped:
                    dirts_array.append(dirt_popped)
                if eval<minEval:
                    minEval=eval
                    tilee=cleaningAgentNextTile
                else:
                    pass
            return minEval,tilee,dirt_agent_tile
        if(maximizing_player):
            maxEval=-float('inf')
            dtile=dirt_agent_tile
            
            dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array,(dtile.x,dtile.y),(cleaning_agent_tile.x,cleaning_agent_tile.y),1)
            if(len(dirt_agent_neighbours)==0):
                eval=self.minimax(False,depth-1,cleaning_agent_tile,dirt_agent_tile,tiles_array,(dirts_array),count+1)[0]
                dirtAgentNextTile=dirt_agent_tile
            else:
                for neighbour in dirt_agent_neighbours:
                    added=False
                    dirt_added=()
                    dirtAgentNextPos=(neighbour.x,neighbour.y)
                    dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if count%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                        d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                        dirts_array.append((d.x,d.y))
                        tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                        added=True
                        dirt_added=(d.x,d.y)

                    
                    eval=self.minimax(False,depth-1,cleaning_agent_tile,dirtAgentNextTile,tiles_array,(dirts_array),count+1)[0]
                    if added:
                        index=dirts_array.index(dirt_added)
                        dirts_array.pop(index)
                if eval>maxEval: 
                    maxEval=eval
                    dtile=dirtAgentNextTile
                else:
                    pass
            return maxEval,None,dtile


    def minimax2(self,maximizing_player,depth,cleaning_agent_tile,dirt_agent_tile,dirt_agent2_tile,d_turn,tiles_array,dirts_array,count,count2):
        print("Dirts array: ",dirts_array)
        if(depth==0):
            # print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScore(cleaning_agent_tile,dirts_array)[0],None,None,None
        if(not maximizing_player):
            minEval= float('inf')
            tilee=cleaning_agent_tile
           
            cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array,(dirt_agent_tile.x,dirt_agent_tile.y),(tilee.x,tilee.y),0)
            for neighbour in cleaning_agent_neighbours:
                popped=False
                dirt_popped=(0,0)
                cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                if (neighbour.x,neighbour.y) in dirts_array:
                    index= dirts_array.index((neighbour.x,neighbour.y))
                    dirts_array.pop(index)
                    popped=True
                    dirt_popped=(neighbour.x,neighbour.y)
                eval= self.minimax2(True,depth-1,cleaningAgentNextTile,dirt_agent_tile,dirt_agent2_tile,1,tiles_array,(dirts_array),count,count2)[0]
                if popped:
                    dirts_array.append(dirt_popped)
                if eval<minEval:
                    minEval=eval
                    tilee=cleaningAgentNextTile
                else:
                    pass
            return minEval,tilee,dirt_agent_tile,None
        if(maximizing_player):
            if d_turn==1:

                maxEval=-float('inf')
                dtile=dirt_agent_tile
                
                dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array,(dtile.x,dtile.y),(cleaning_agent_tile.x,cleaning_agent_tile.y),1)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimax2(False,depth-1,cleaning_agent_tile,dirt_agent_tile,dirt_agent2_tile,2,tiles_array,(dirts_array),count+1,count2)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile,None
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if count%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)

                        
                        eval=self.minimax2(True,depth-1,cleaning_agent_tile,dirtAgentNextTile,dirt_agent2_tile,2,tiles_array,(dirts_array),count+1,count2)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        else:
                            pass
                    return maxEval,None,dtile,None
            if d_turn==2:

                maxEval=-float('inf')
                dtile=dirt_agent2_tile
                
                dirt_agent_neighbours = self.getNeighbours(dirt_agent2_tile,tiles_array,(dtile.x,dtile.y),(cleaning_agent_tile.x,cleaning_agent_tile.y),1)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimax2(False,depth-1,cleaning_agent_tile,dirt_agent_tile,dirt_agent2_tile,1,tiles_array,(dirts_array),count,count2+1)[0]
                    # dirtAgentNextTile=dirt_agent2_tile
                    return eval,None,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if count2%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)

                        
                        eval=self.minimax2(False,depth-1,cleaning_agent_tile,dirt_agent_tile,dirtAgentNextTile,1,tiles_array,(dirts_array),count,count2+1)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        else:
                            pass
                    return maxEval,None,None,dtile
    def alphabeta(self,maximizing_player,depth,alpha,beta,cleaning_agent_tile,dirt_agent_tile,tiles_array,dirts_array,count):
        if(depth==0):
            print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScore(cleaning_agent_tile,dirts_array)[0],None,None
        if(not maximizing_player):
            minEval= float('inf')
            tilee=cleaning_agent_tile
            cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array)
            for neighbour in cleaning_agent_neighbours:
                
                cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                if (neighbour.x,neighbour.y) in dirts_array:
                    index= dirts_array.index((neighbour.x,neighbour.y))
                    dirts_array.pop(index)
                eval= self.alphabeta(True,depth-1,alpha,beta,cleaningAgentNextTile,dirt_agent_tile,tiles_array,dirts_array,count)[0]
                if eval<minEval:
                    minEval=eval
                    tilee=cleaningAgentNextTile
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval,tilee,dirt_agent_tile
        if(maximizing_player):
            maxEval=-float('inf')
            dtile=dirt_agent_tile
            if count%self.dirts_freq==0 and ((dirt_agent_tile.x,dirt_agent_tile.y) not in dirts_array):
                    d=(Dirt(dirt_agent_tile.x,dirt_agent_tile.y))
                    dirts_array.append((d.x,d.y))
                    tiles_array[dirt_agent_tile.x][dirt_agent_tile.y].isDirty=True
            dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array)
            if(len(dirt_agent_neighbours)==0):
                eval=self.minimax(False,depth,cleaning_agent_tile,dirt_agent_tile,tiles_array,dirts_array,count+1)[0]
            else:
                for neighbour in dirt_agent_neighbours:
                    dirtAgentNextPos=(neighbour.x,neighbour.y)
                    dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    eval=self.alphabeta(False,depth-1,alpha,beta,cleaning_agent_tile,dirtAgentNextTile,tiles_array,dirts_array,count+1)[0]
                    if eval>maxEval: 
                        maxEval=eval
                        dtile=dirtAgentNextTile
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return maxEval,None,dtile


    def alphabeta2(self,maximizing_player,depth,alpha,beta,cleaning_agent_tile,dirt_agent_tile,dirt_agent2_tile,d_turn,tiles_array,dirts_array,count,count2):
        print("Dirts array: ",dirts_array)
        if(depth==0):
            # print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScore(cleaning_agent_tile,dirts_array)[0],None,None,None
        if(not maximizing_player):
            minEval= float('inf')
            tilee=cleaning_agent_tile
           
            cleaning_agent_neighbours = self.getNeighbours(cleaning_agent_tile,tiles_array,(dirt_agent_tile.x,dirt_agent_tile.y),(tilee.x,tilee.y),0)
            for neighbour in cleaning_agent_neighbours:
                popped=False
                dirt_popped=(0,0)
                cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                if (neighbour.x,neighbour.y) in dirts_array:
                    index= dirts_array.index((neighbour.x,neighbour.y))
                    dirts_array.pop(index)
                    popped=True
                    dirt_popped=(neighbour.x,neighbour.y)
                eval= self.minimax2(True,depth-1,cleaningAgentNextTile,dirt_agent_tile,dirt_agent2_tile,1,tiles_array,(dirts_array),count,count2)[0]
                if popped:
                    dirts_array.append(dirt_popped)
                if eval<minEval:
                    minEval=eval
                    tilee=cleaningAgentNextTile
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval,tilee,dirt_agent_tile,None
        if(maximizing_player):
            if d_turn==1:

                maxEval=-float('inf')
                dtile=dirt_agent_tile
                
                dirt_agent_neighbours = self.getNeighbours(dirt_agent_tile,tiles_array,(dtile.x,dtile.y),(cleaning_agent_tile.x,cleaning_agent_tile.y),1)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimax2(True,depth-1,cleaning_agent_tile,dirt_agent_tile,dirt_agent2_tile,2,tiles_array,(dirts_array),count+1,count2)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile,None
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if count%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)

                        
                        eval=self.minimax2(True,depth-1,cleaning_agent_tile,dirtAgentNextTile,dirt_agent2_tile,2,tiles_array,(dirts_array),count+1,count2)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break


                    return maxEval,None,dtile,None
            if d_turn==2:

                maxEval=-float('inf')
                dtile=dirt_agent2_tile
                
                dirt_agent_neighbours = self.getNeighbours(dirt_agent2_tile,tiles_array,(dtile.x,dtile.y),(cleaning_agent_tile.x,cleaning_agent_tile.y),1)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimax2(False,depth-1,cleaning_agent_tile,dirt_agent_tile,dirt_agent2_tile,1,tiles_array,(dirts_array),count,count2+1)[0]
                    # dirtAgentNextTile=dirt_agent2_tile
                    return eval,None,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if count2%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)

                        
                        eval=self.minimax2(False,depth-1,cleaning_agent_tile,dirt_agent_tile,dirtAgentNextTile,1,tiles_array,(dirts_array),count,count2+1)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                if eval>maxEval: 
                    maxEval=eval
                    dtile=dirtAgentNextTile
                else:
                    pass
                    return maxEval,None,None,dtile


    
 #   def minimaxmultimain(self,maximizing_player,depth,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index,tiles_array,dirts_array,counts,positions=[]):
        
        
    def minimaxmulti(self,maximizing_player,depth,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index,tiles_array,dirts_array,counts,positions=[]):
        # print("Dirts array: ",dirts_array)
        if(depth==0):
            # print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScoreMulti(cleaning_agents_tile,dirts_array),None,None   

        if(not maximizing_player):
            if (cleaning_agent_index<len(cleaning_agents_tile)-1):

                minEval= float('inf')
                tilee=cleaning_agents_tile[cleaning_agent_index]
            
                cleaning_agent_neighbours = self.getNeighboursWalls(tilee,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                for neighbour in cleaning_agent_neighbours:
                    popped=False
                    dirt_popped=(0,0)
                    cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if (neighbour.x,neighbour.y) in dirts_array:
                        index= dirts_array.index((neighbour.x,neighbour.y))
                        dirts_array.pop(index)
                        popped=True
                        dirt_popped=(neighbour.x,neighbour.y)
                    cleaning_agents_tile[cleaning_agent_index]=cleaningAgentNextTile
                    eval= self.minimaxmulti(False,depth-1,cleaning_agents_tile,cleaning_agent_index+1, dirt_agents_tile, dirt_agent_index,tiles_array,dirts_array,counts,positions)[0]
                    if popped:
                        dirts_array.append(dirt_popped)
                    if eval<minEval:
                        minEval=eval
                        tilee=cleaningAgentNextTile
                    else:
                        pass
                return minEval,tilee,None
                
            if(cleaning_agent_index==len(cleaning_agents_tile)-1):
                minEval= float('inf')
                tilee=cleaning_agents_tile[cleaning_agent_index]
            
                cleaning_agent_neighbours = self.getNeighboursWalls(tilee,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                for neighbour in cleaning_agent_neighbours:
                    popped=False
                    dirt_popped=(0,0)
                    cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if (neighbour.x,neighbour.y) in dirts_array:
                        index= dirts_array.index((neighbour.x,neighbour.y))
                        dirts_array.pop(index)
                        popped=True
                        dirt_popped=(neighbour.x,neighbour.y)
                    cleaning_agents_tile[cleaning_agent_index]=cleaningAgentNextTile
                    eval= self.minimaxmulti(True,depth-1,cleaning_agents_tile,0, dirt_agents_tile, 0,tiles_array,dirts_array,counts)[0]
                    if popped:
                        dirts_array.append(dirt_popped)
                    if eval<minEval:
                        minEval=eval
                        tilee=cleaningAgentNextTile
                    else:
                        pass

                return minEval,tilee,None
        if(maximizing_player):
            if(dirt_agent_index<len(dirt_agents_tile)-1):



                maxEval=-float('inf')
                dtile=dirt_agents_tile[dirt_agent_index]
                
                dirt_agent_neighbours = self.getNeighboursWalls(dtile,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimaxmulti(True,depth-1,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index+1,tiles_array,dirts_array,counts)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if counts[dirt_agent_index]%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)
                        dirt_agents_tile[dirt_agent_index]=dirtAgentNextTile 

                        
                        eval=eval=self.minimaxmulti(True,depth-1,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index+1,tiles_array,dirts_array,counts)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        else:
                            pass
                    return maxEval,None,dtile

            if(dirt_agent_index==len(dirt_agents_tile)-1):



                maxEval=-float('inf')
                dtile=dirt_agents_tile[dirt_agent_index]
                
                dirt_agent_neighbours = self.getNeighboursWalls(dtile,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimaxmulti(False,depth-1,cleaning_agents_tile,0,dirt_agents_tile,0,tiles_array,dirts_array,counts)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if counts[dirt_agent_index]%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)
                        dirt_agents_tile[dirt_agent_index]=dirtAgentNextTile

                        
                        eval=eval=self.minimaxmulti(False,depth-1,cleaning_agents_tile,0,dirt_agents_tile,0,tiles_array,dirts_array,counts)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        else:
                            pass
                    return maxEval,None,dtile
    def alphabetamulti(self,maximizing_player,alpha,beta,depth,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index,tiles_array,dirts_array,counts,positions=[]):
        # print("Dirts array: ",dirts_array)
        if(depth==0):
            # print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScoreMulti(cleaning_agents_tile,dirts_array),None,None   

        if(not maximizing_player):
            if (cleaning_agent_index<len(cleaning_agents_tile)-1):

                minEval= float('inf')
                tilee=cleaning_agents_tile[cleaning_agent_index]
            
                cleaning_agent_neighbours = self.getNeighboursWalls(tilee,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                for neighbour in cleaning_agent_neighbours:
                    popped=False
                    dirt_popped=(0,0)
                    cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if (neighbour.x,neighbour.y) in dirts_array:
                        index= dirts_array.index((neighbour.x,neighbour.y))
                        dirts_array.pop(index)
                        popped=True
                        dirt_popped=(neighbour.x,neighbour.y)
                    cleaning_agents_tile[cleaning_agent_index]=cleaningAgentNextTile
                    eval= self.alphabetamulti(False,alpha,beta,depth-1,cleaning_agents_tile,cleaning_agent_index+1, dirt_agents_tile, dirt_agent_index,tiles_array,dirts_array,counts,positions)[0]
                    if popped:
                        dirts_array.append(dirt_popped)
                    if eval<minEval:
                        minEval=eval
                        tilee=cleaningAgentNextTile
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return minEval,tilee,None
                
            if(cleaning_agent_index==len(cleaning_agents_tile)-1):
                minEval= float('inf')
                tilee=cleaning_agents_tile[cleaning_agent_index]
            
                cleaning_agent_neighbours = self.getNeighboursWalls(tilee,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                for neighbour in cleaning_agent_neighbours:
                    popped=False
                    dirt_popped=(0,0)
                    cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if (neighbour.x,neighbour.y) in dirts_array:
                        index= dirts_array.index((neighbour.x,neighbour.y))
                        dirts_array.pop(index)
                        popped=True
                        dirt_popped=(neighbour.x,neighbour.y)
                    cleaning_agents_tile[cleaning_agent_index]=cleaningAgentNextTile
                    eval= self.alphabetamulti(True,alpha,beta,depth-1,cleaning_agents_tile,0, dirt_agents_tile, 0,tiles_array,dirts_array,counts)[0]
                    if popped:
                        dirts_array.append(dirt_popped)
                    if eval<minEval:
                        minEval=eval
                        tilee=cleaningAgentNextTile
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break

                return minEval,tilee,None
        if(maximizing_player):
            if(dirt_agent_index<len(dirt_agents_tile)-1):



                maxEval=-float('inf')
                dtile=dirt_agents_tile[dirt_agent_index]
                
                dirt_agent_neighbours = self.getNeighboursWalls(dtile,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.alphabetamulti(True,alpha,beta,depth-1,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index+1,tiles_array,dirts_array,counts)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if counts[dirt_agent_index]%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)
                        dirt_agents_tile[dirt_agent_index]=dirtAgentNextTile 

                        
                        eval=eval=self.alphabetamulti(True,alpha,beta,depth-1,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index+1,tiles_array,dirts_array,counts)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                    return maxEval,None,dtile

            if(dirt_agent_index==len(dirt_agents_tile)-1):



                maxEval=-float('inf')
                dtile=dirt_agents_tile[dirt_agent_index]
                
                dirt_agent_neighbours = self.getNeighboursWalls(dtile,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.alphabetamulti(False,alpha,beta,depth-1,cleaning_agents_tile,0,dirt_agents_tile,0,tiles_array,dirts_array,counts)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if counts[dirt_agent_index]%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)
                        dirt_agents_tile[dirt_agent_index]=dirtAgentNextTile

                        
                        eval=eval=self.alphabetamulti(False,alpha,beta,depth-1,cleaning_agents_tile,0,dirt_agents_tile,0,tiles_array,dirts_array,counts)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                        if eval>maxEval: 
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
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

    def minimaxmultiwithbattery(self,maximizing_player,depth,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index,tiles_array,dirts_array,counts,dirt_agents_battery=[],cleaning_agents_battery=[]):
        # print("Dirts array: ",dirts_array)
        if(depth==0):
            # print("end: ",self.getScore(cleaning_agent_tile,dirts_array)[0],"  ",(cleaning_agent_tile.x,cleaning_agent_tile.y))
            return self.getScoreMulti(cleaning_agents_tile,dirts_array),None,None

        if(not maximizing_player):
            if (cleaning_agent_index<len(cleaning_agents_tile)-1):

                minEval= float('inf')
                tilee=cleaning_agents_tile[cleaning_agent_index]

                cleaning_agent_neighbours = self.getNeighboursWalls(tilee,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                for neighbour in cleaning_agent_neighbours:
                    popped=False
                    dirt_popped=(0,0)
                    cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if (neighbour.x,neighbour.y) in dirts_array and cleaning_agents_battery[cleaning_agent_index]>=10:
                        index= dirts_array.index((neighbour.x,neighbour.y))
                        dirts_array.pop(index)
                        popped=True
                        dirt_popped=(neighbour.x,neighbour.y)
                        cleaning_agents_battery[cleaning_agent_index]-=10
                    if cleaning_agents_battery[cleaning_agent_index]>=5:
                        cleaning_agents_tile[cleaning_agent_index]=cleaningAgentNextTile
                        cleaning_agents_battery[cleaning_agent_index]-=5
                    eval= self.minimaxmultiwithbattery(False,depth-1,cleaning_agents_tile,cleaning_agent_index+1, dirt_agents_tile, dirt_agent_index,tiles_array,dirts_array,counts,dirt_agents_battery,cleaning_agents_battery)[0]

                    if popped:
                        dirts_array.append(dirt_popped)
                        cleaning_agents_battery[cleaning_agent_index]+=10
                    if eval<minEval:
                        minEval=eval
                        tilee=cleaningAgentNextTile
                    else:
                        pass
                return minEval,tilee,None

            if(cleaning_agent_index==len(cleaning_agents_tile)-1):
                minEval= float('inf')
                tilee=cleaning_agents_tile[cleaning_agent_index]

                cleaning_agent_neighbours = self.getNeighboursWalls(tilee,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                for neighbour in cleaning_agent_neighbours:
                    popped=False
                    dirt_popped=(0,0)
                    cleaningAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                    if (neighbour.x,neighbour.y) in dirts_array and  cleaning_agents_battery[cleaning_agent_index]>=10:
                        index= dirts_array.index((neighbour.x,neighbour.y))
                        dirts_array.pop(index)
                        popped=True
                        cleaning_agents_battery[cleaning_agent_index]-=10
                        dirt_popped=(neighbour.x,neighbour.y)
                    if cleaning_agents_battery[cleaning_agent_index]>=5:
                        cleaning_agents_tile[cleaning_agent_index]=cleaningAgentNextTile
                        cleaning_agents_battery[cleaning_agent_index]-=5
                    eval= self.minimaxmultiwithbattery(True,depth-1,cleaning_agents_tile,0, dirt_agents_tile, 0,tiles_array,dirts_array,counts,dirt_agents_battery,cleaning_agents_battery)[0]
                    if popped:
                        dirts_array.append(dirt_popped)
                        cleaning_agents_battery[cleaning_agent_index]+=10
                    if eval<minEval:
                        minEval=eval
                        tilee=cleaningAgentNextTile
                    else:
                        pass

                return minEval,tilee,None
        if(maximizing_player):
            if(dirt_agent_index<len(dirt_agents_tile)-1):



                maxEval=-float('inf')
                dtile=dirt_agents_tile[dirt_agent_index]

                dirt_agent_neighbours = self.getNeighboursWalls(dtile,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                if(len(dirt_agent_neighbours)==0):

                    eval=self.minimaxmultiwithbattery(True,depth-1,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index+1,tiles_array,dirts_array,counts,dirt_agents_battery,cleaning_agents_battery)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if counts[dirt_agent_index]%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array and dirt_agents_battery[dirt_agent_index]>=10):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)
                            dirt_agents_battery[dirt_agent_index]-=10
                        if dirt_agents_battery[dirt_agent_index]>=5:
                            dirt_agents_tile[dirt_agent_index]=dirtAgentNextTile
                            dirt_agents_battery[dirt_agent_index]-=5


                        eval=eval=self.minimaxmultiwithbattery(True,depth-1,cleaning_agents_tile,cleaning_agent_index,dirt_agents_tile,dirt_agent_index+1,tiles_array,dirts_array,counts,dirt_agents_battery,cleaning_agents_battery)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                            dirt_agents_battery[dirt_agent_index]+=10
                        if eval>maxEval:
                            maxEval=eval
                            dtile=dirtAgentNextTile
                        else:
                            pass
                    return maxEval,None,dtile

            if(dirt_agent_index==len(dirt_agents_tile)-1):



                maxEval=-float('inf')
                dtile=dirt_agents_tile[dirt_agent_index]

                dirt_agent_neighbours = self.getNeighboursWalls(dtile,tiles_array,cleaning_agents_tile,dirt_agents_tile)
                if(len(dirt_agent_neighbours)==0):
                    eval=self.minimaxmultiwithbattery(False,depth-1,cleaning_agents_tile,0,dirt_agents_tile,0,tiles_array,dirts_array,counts,dirt_agents_battery,cleaning_agents_battery)[0]
                    # dirtAgentNextTile=dirt_agent_tile
                    return eval,None,dtile
                else:
                    for neighbour in dirt_agent_neighbours:
                        added=False
                        dirt_added=()
                        dirtAgentNextPos=(neighbour.x,neighbour.y)
                        dirtAgentNextTile=tiles_array[neighbour.x][neighbour.y]
                        if counts[dirt_agent_index]%self.dirts_freq==0 and ((dirtAgentNextTile.x,dirtAgentNextTile.y) not in dirts_array and dirt_agents_battery[dirt_agent_index]>=10):
                            d=(Dirt(dirtAgentNextTile.x,dirtAgentNextTile.y))
                            dirts_array.append((d.x,d.y))
                            tiles_array[dirtAgentNextTile.x][dirtAgentNextTile.y].isDirty=True
                            added=True
                            dirt_added=(d.x,d.y)
                            dirt_agents_battery[dirt_agent_index]-=10
                        if dirt_agents_battery[dirt_agent_index]>=5:
                            dirt_agents_tile[dirt_agent_index]=dirtAgentNextTile
                            dirt_agents_battery[dirt_agent_index]-=5


                        eval=eval=self.minimaxmultiwithbattery(False,depth-1,cleaning_agents_tile,0,dirt_agents_tile,0,tiles_array,dirts_array,counts,dirt_agents_battery,cleaning_agents_battery)[0]
                        if added:
                            index=dirts_array.index(dirt_added)
                            dirts_array.pop(index)
                            dirt_agents_battery[dirt_agent_index]+=10
                        if eval>maxEval:
                            maxEval=eval
                            dtile=dirtAgentNextTile

                        else:
                            pass
                    return maxEval,None,dtile
    def getResult(self):
        minScore,minIndex=self.getMin(self.scores)
        return minScore,minIndex




    
        






        
