
import pygame
import random as rnd
from pygame import color
from pygame import font
from pygame.event import get
from Sprites.Checkbox import Checkbox
from Sprites.DropDown import DropDown
from Sprites.InputText import InputBox
from Sprites.TextLabel import TextLabel
from Sprites.VacuumCleaner import VacuumCleaner
from Sprites.DirtAgent import DirtAgent
from Sprites.Wall import Wall, Walls
import constants
from Sprites.Tiles import Tile, Tiles
from Sprites.Dirt import Dirt, Dirts
from Algorithms.BFS import BFS
from time import sleep
from Sprites.Button import Button
from Algorithms.Djikstra import Djikstra
from Algorithms.Astar import Astar
from Algorithms.TSP import generatePathsList
from Algorithms.MiniMax.minimax import MiniMax
from copy import deepcopy

class Game2:
    def __init__(self,n,m):
        self.n=n
        self.m=m
        self.init_pygame()
        self.Tiles=Tiles(n,m)
        self.Dirts=Dirts(n,m)
        self.Walls = Walls(n,m)
        self.VacuumCleaners= [VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT),VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,4,3),VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,2,2)]
        self.DirtAgents=[DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,3,4),DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,5,5)]
        self.counts=[0,0,0]

        self.DirtAgent= DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,0,1)
        self.DirtAgent2= DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,3,4)
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping=True
        self.dirt_checkbox= Checkbox(self.screen,30,520,1,caption="Dirt")
        self.wall_checkbox= Checkbox(self.screen,110,520,2,caption="Wall")
        self.agent_checkbox= Checkbox(self.screen,210,520,2,caption="Place Agent")
        
        self.rnd_dirts_btn= Button("Random Dirts",(10,560),font=25,bg=(200,150,50))
        self.clear_dirts_btn= Button("Clear Dirts",(10,600),font=25,bg=(200,150,50))
        self.rnd_walls_btn=Button("Random Walls",(200,560),font=25,bg=(200,150,50))
        self.clear_walls_btn= Button("Clear Walls",(200,600),font=25,bg=(200,150,50))
        self.dropdown=DropDown(530, 510, 150, 20,  "Select Speed", ["Very Slow", "Slow","Medium","Fast","Very Fast"])
        self.algorithm_list=DropDown(350, 510, 150, 20,  "Select Algorithm", ["Modified BFS", "TSP+Best First Search","Djikstra","A*"])
        self.random_dist_list=DropDown(350, 560, 180, 20,  "Select Random Distribution", ["Uniform: 50%", "Uniform: 12.5%"])
        self.moves_label=TextLabel('No.  Moves: 0',600,560,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.explored_label=TextLabel('No.  Explored:0 ',600,600,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.input_txt=InputBox(200,650,80,30)
        self.textlabel=TextLabel('Write in form "n,m"',100,665,font_background=(255,255,255))

        self.grid_btn= Button("Generate Grid",(300,650),font=25,bg=(100, 80, 255),text_color="Black")
        self.reset_btn= Button("  Reset  ",(500,650),font=25,bg=(255, 100, 100),text_color="Black")
        self.start_btn= Button("  Start  ",(600,650),font=25,bg=(100, 140, 60),text_color="Black")
        self.checkboxes=[self.dirt_checkbox,self.wall_checkbox,self.agent_checkbox]
        self.initialized=False
        self.WAIT_TIME=0.5
        self.ALGORITHM="Modified BFS"
    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("{}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((1200, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
       
    def update_classes(self):
        for tile in self.Tiles.tiles:
            self.all_sprites.add(tile)
        for dirt in self.Dirts.dirts :
            self.all_sprites.add(dirt)
        
        for wall in self.Walls.walls:
            self.all_sprites.add(wall)
        for VacuumCleaner in self.VacuumCleaners:
            VacuumCleaner.kill()
            self.all_sprites.add(VacuumCleaner)
        for DirtAgent in self.DirtAgents:
            DirtAgent.kill()
            self.all_sprites.add(DirtAgent)
    def killWalls(self):
        for wall in self.Walls.walls:
            wall.kill()
    def killDirts(self):
        for dirtss in self.Dirts.dirts:
            for dirt in dirtss:
                dirt.kill()
    def killVacuumCleaner(self):
        for VacuumCleaner in self.VacuumCleaners:

            VacuumCleaner.kill()
    
    def killTiles(self):
        for tiles in self.Tiles.tiles:
            for tile in tiles:
                tile.kill()
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        self.moves_label.draw(self.screen)
        self.explored_label.draw(self.screen)
        self.random_dist_list.draw(self.screen)
        self.dirt_checkbox.render_checkbox()
        self.wall_checkbox.render_checkbox()
        self.agent_checkbox.render_checkbox()
        self.screen.blit(self.reset_btn.surface, (self.reset_btn.x, self.reset_btn.y))
        self.screen.blit(self.start_btn.surface, (self.start_btn.x, self.start_btn.y))
        self.screen.blit(self.rnd_dirts_btn.surface, (self.rnd_dirts_btn.x, self.rnd_dirts_btn.y))
        self.screen.blit(self.clear_dirts_btn.surface, (self.clear_dirts_btn.x, self.clear_dirts_btn.y))
        self.screen.blit(self.grid_btn.surface, (self.grid_btn.x, self.grid_btn.y))
        self.screen.blit(self.rnd_walls_btn.surface, (self.rnd_walls_btn.x, self.rnd_walls_btn.y))
        self.screen.blit(self.clear_walls_btn.surface, (self.clear_walls_btn.x, self.clear_walls_btn.y))
        self.input_txt.draw(self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.dropdown.draw(self.screen)
        self.algorithm_list.draw(self.screen)
        self.textlabel.draw(self.screen)

        pygame.display.flip()


    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.keep_looping = False
                elif event.key ==pygame.K_SPACE:
                    self.killVacuumCleaner()
                    self.setSpeed()
                    self.clean(0,0,self.Tiles.tiles,self.Tiles)
                
            for box in self.checkboxes:
                    box.update_checkbox(event)
                    if box.checked is True:
                        for b in self.checkboxes:
                            if b != box:
                                b.checked = False
            self.input_txt.handle_event(event)
            if event.type ==pygame.MOUSEBUTTONDOWN :
                self.dropdown.update(event)
                self.algorithm_list.update(event)
                self.random_dist_list.update(event)
                if pygame.mouse.get_pressed()[0]:
                    x=pygame.mouse.get_pos()[0]
                    y=pygame.mouse.get_pos()[1]
                    self.Dirts.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Tiles.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Walls.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
                    self.Tiles.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
                    print(self.Dirts.dirts_array)
                    if(self.agent_checkbox):
                        self.killVacuumCleaner()
                        self.VacuumCleaners[0].addAgent(x,y,check=self.agent_checkbox.checked,n=self.n,m=self.m)
                    if self.reset_btn.rect.collidepoint(x,y):
                        self.resetGrid()
                    if self.start_btn.rect.collidepoint(x,y):
                        self.setSpeed()
                        for i in range(30):
                            self.startAllAgents()
                        # for i in range(30):
                        #     for i in range(len(self.DirtAgents)):
                        #         self.startSmartDirtAgent1(i)
                            
                        #     for i in range(len(self.VacuumCleaners)):
                        #         score,tile=self.cleanMiniMax(i)
                        #         self.VacuumCleaners[i].move(tile.x-self.VacuumCleaners[i].x,tile.y-self.VacuumCleaners[i].y)
                        #         pygame.event.pump()
                        #         self.draw()

                        # self.setSpeed()
                        # # self.clean(0,0,self.Tiles.tiles,self.Tiles)
                        # self.startDirtAgentRandom()
                    if self.rnd_dirts_btn.rect.collidepoint(x,y):
                        self.killVacuumCleaner()
                        self.randomDirts(self.Tiles.tiles)
                    if self.clear_dirts_btn.rect.collidepoint(x,y):
                        self.clearDirts()
                    if self.clear_walls_btn.rect.collidepoint(x,y):
                        self.clearWalls()
                    if self.grid_btn.rect.collidepoint(x,y):
                        self.generateGrid()
                    if self.rnd_walls_btn.rect.collidepoint(x,y):
                        self.killVacuumCleaner()
                        self.randomWalls()
                    self.draw()


    def cleanMiniMax(self,i):
        MiniMaxS=MiniMax()
        cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[i].x][self.VacuumCleaners[i].y]
        dirtAgentTile= self.Tiles.tiles[self.DirtAgents[0].x][self.DirtAgents[0].y]
        dirtAgent2Tile= self.Tiles.tiles[self.DirtAgents[1].x][self.DirtAgents[1].y]
        if self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty:
            self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y].kill()
            self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y]=Dirt()
            self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty=False
            if ((cleaningAgentTile.x,cleaningAgentTile.y) in self.Dirts.dirts_array):
                index=self.Dirts.dirts_array.index((cleaningAgentTile.x,cleaningAgentTile.y))
                self.Dirts.dirts_array.pop(index)
        print("dirts array passed",self.Dirts.dirts_array)
        d_copy=deepcopy(self.Dirts.dirts_array)
        score,tile,tile1,til2=MiniMaxS.minimax2(False,6,cleaningAgentTile,dirtAgentTile,dirtAgent2Tile,1,self.Tiles.tiles,d_copy,self.DirtAgents[0].count,self.DirtAgents[1].count)
        #score,tile,tile1=MiniMaxS.minimax(False,5,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,self.Dirts.dirts_array,self.DirtAgent.count)
        
                
        return score,tile
        

    def randomDirts(self,tiles):
        self.clearDirts()
        for i in tiles:
            for j in i:
                if self.random_dist_list.main=="Uniform: 50%":

                    random_dirt=int(rnd.uniform(0,2))
                else:
                    random_dirt=rnd.getrandbits(3)

                
                if random_dirt==1:
                    j.isDirty=True
                    self.Dirts.addDirtXY(j.x,j.y,True)
                    self.Tiles.addDirtXY(j.x,j.y,True)
                else:
                    j.isDirty=False
        self.draw()
    def generateGrid(self):
        try:
            size=self.input_txt.text.split(",")
            n=int(size[0])
            m=int(size[1])
            if n==0 or m==0 or (n>=90 and m>=90):
                raise Exception('Invalid Number')
            self.n=n
            self.m=m
            self.clearDirts()
            self.clearWalls()

            self.Tiles=Tiles(n,m)
            self.Dirts=Dirts(n,m)
            self.Walls=Walls(n,m)
            for i,V in enumerate(self.VacuumCleaners):

                self.VacuumCleaners[i]= VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT)
            self.draw()
        except:
            self.input_txt=InputBox(200,650,80,30)
            self.input_txt.draw(self.screen)
    def resetGrid(self):
            self.Tiles=Tiles(self.n,self.m)
            self.Dirts=Dirts(self.n,self.m)
            self.Walls=Walls(self.n,self.m)
            self.moves_label.setText("No.  Moves: 0")
            self.explored_label.setText("No.  Explored Nodes: 0")
            for i in range(len(self.VacuumCleaners)):
                self.VacuumCleaner[i]= VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT)

            self.draw()
    def randomWalls(self):
        tiles=self.Tiles.tiles
        self.clearWalls()
        for i in tiles:
            for j in i:
                
                random_dirt=rnd.getrandbits(3)
                if random_dirt==0:
                    j.has_walls_up=True
                    self.Walls.addWallXY(j.x,j.y,True,"up")
                    self.Tiles.addWallXY(j.x,j.y,True,"up")
                elif random_dirt==1:
                    j.has_walls_down=True
                    self.Walls.addWallXY(j.x,j.y,True,"down")
                    self.Tiles.addWallXY(j.x,j.y,True,"down")
                elif random_dirt==2:
                    j.has_walls_right=True
                    self.Walls.addWallXY(j.x,j.y,True,"right")
                    self.Tiles.addWallXY(j.x,j.y,True,"right")
                elif random_dirt==3:
                    j.has_walls_left=True
                    self.Walls.addWallXY(j.x,j.y,True,"left")
                    self.Tiles.addWallXY(j.x,j.y,True,"left")
        self.draw()
                
    def setSpeed(self):
        if self.dropdown.main=="Very Slow":
            self.WAIT_TIME=0.5
        elif self.dropdown.main=="Slow":
            self.WAIT_TIME=0.2
        elif self.dropdown.main=="Medium":
            self.WAIT_TIME=0.05
        elif self.dropdown.main=="Fast":
            self.WAIT_TIME=0.001
        elif self.dropdown.main=="Very Fast":
            self.WAIT_TIME=0.0001
    def clearDirts(self):
        self.killDirts()
        self.killVacuumCleaner()
        self.Tiles.clearDirts()
        self.Dirts.clearDirts()
        for i in range(len(self.VacuumCleaners)):
            self.VacuumCleaners[i]=VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,self.VacuumCleaners[i].x,self.VacuumCleaners[i].y)
        self.draw()
    def clearWalls(self):
        self.killWalls()
        self.killVacuumCleaner()
        self.Tiles.clearWalls()
        self.Walls.clearWalls()
        for i in range(len(self.VacuumCleaners)):
            self.VacuumCleaners[i]=VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,self.VacuumCleaners[i].x,self.VacuumCleaners[i].y)


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
    def startDirtAgentRandom(self,i):
        prevPos=[]
        for i in range(1):
            neighbours=self.getNeighbours(self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y],self.Tiles.tiles)
            neighbourAvailable=False
            for j in range(len(neighbours)):
                if not (neighbours[j].x,neighbours[j].y) in prevPos:
                    neighbourAvailable=True
                    break
            if(not neighbourAvailable):
                prevPos=[]
            if(len(neighbours)>=1):
                n=rnd.randint(0,len(neighbours)-1)
                nextPosX=neighbours[n].x
                nextPosY=neighbours[n].y
                # print(neighbours)
                # print("n: ",n)
                prevPosX=self.DirtAgents[i].x
                prevPosY=self.DirtAgents[i].y
                #added to the list of visited positions
                prevPos.append((prevPosX,prevPosY))
                #make sure the next position is not visted before
                while((nextPosX,nextPosY) in prevPos):
                    n=rnd.randint(0,len(neighbours)-1)
                    nextPosX=neighbours[n].x
                    nextPosY=neighbours[n].y

                dx=nextPosX-prevPosX
                dy=nextPosY-prevPosY
                # print(dx," , ",dy)
                m=rnd.randint(0,1)
                
                if( self.DirtAgents[i].count%3==0):
                        self.Dirts.addDirtXY(prevPosX,prevPosY,True)
                        self.Tiles.addDirtXY(prevPosX,prevPosY,True)
                else:
                        pass
                self.DirtAgents[i].move(dx,dy)
                self.DirtAgents[i].count+=1
                
                

                self.draw()
                sleep(self.WAIT_TIME)
    def startSmartDirtAgent(self,i):
        print("Before moving firts array is :",self.Dirts.dirts_array)
        MiniMaxS=MiniMax()
        cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[0].x][self.VacuumCleaners[0].y]
        dirtAgentTile= self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y]
        if ((dirtAgentTile.x,dirtAgentTile.y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
                self.Dirts.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
                self.Tiles.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
        print("After adding dirts: ,",self.Dirts.dirts_array)
        d_copy=  deepcopy(self.Dirts.dirts_array)
        score,tile,tile1=MiniMaxS.minimax(True,3,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,d_copy,self.DirtAgents[i].count)
        #score,tile,tile1=MiniMaxS.minimax(True,5,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,self.Dirts.dirts_array,self.DirtAgent.count)
        self.DirtAgents[i].move(tile1.x-self.DirtAgents[i].x,tile1.y-self.DirtAgents[i].y)
        print("After moving firts array is :",self.Dirts.dirts_array)
        

        self.DirtAgent.count+=1
                
        return score,tile

    def startSmartDirtAgent1(self,i):
        print("Before moving firts array is :",self.Dirts.dirts_array)
        MiniMaxS=MiniMax()
        cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[0].x][self.VacuumCleaners[0].y]
        dirtAgentTiles= [self.Tiles.tiles[self.DirtAgents[0].x][self.DirtAgents[0].y], self.Tiles.tiles[self.DirtAgents[1].x][self.DirtAgents[1].y]]
        if ((dirtAgentTiles[i].x,dirtAgentTiles[i].y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
                self.Dirts.addDirtXY(dirtAgentTiles[i].x,dirtAgentTiles[i].y,True)
                self.Tiles.addDirtXY(dirtAgentTiles[i].x,dirtAgentTiles[i].y,True)
        print("After adding dirts: ,",self.Dirts.dirts_array)
        d_copy=  deepcopy(self.Dirts.dirts_array)
        score,tile,tile1,tile2=MiniMaxS.minimax2(True,4,cleaningAgentTile,dirtAgentTiles[0],dirtAgentTiles[1],i+1,self.Tiles.tiles,d_copy,self.DirtAgents[0].count,self.DirtAgents[1].count)
        if(i==0):
        #score,tile,tile1=MiniMaxS.minimax(True,5,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,self.Dirts.dirts_array,self.DirtAgent.count)
            self.DirtAgents[i].move(tile1.x-self.DirtAgents[i].x,tile1.y-self.DirtAgents[i].y)
        if(i==1):
            self.DirtAgents[i].move(tile2.x-self.DirtAgents[i].x,tile2.y-self.DirtAgents[i].y)
        print("After moving firts array is :",self.Dirts.dirts_array)
        

        self.DirtAgents[i].count+=1


    def startAllAgents(self):
        for i in range(len(self.DirtAgents)):
             minimax= MiniMax()
             dirtAgentTile= self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y]
             if ((dirtAgentTile.x,dirtAgentTile.y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
                self.Dirts.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
                self.Tiles.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
             d_copy=  deepcopy(self.Dirts.dirts_array)
             score,t,d_tile=minimax.minimaxmulti(True,3,self.getCleaningAgentsTiles(),0,self.getDirtAgentsTiles(),i,self.Tiles.tiles,d_copy,self.counts)
             self.DirtAgents[i].move(d_tile.x-self.DirtAgents[i].x,d_tile.y-self.DirtAgents[i].y)
             self.DirtAgents[i].count+=1
             self.counts[i]+=1
             self.draw()
             pygame.event.pump()
        for i in range(len(self.VacuumCleaners)):
             minimax= MiniMax()
             cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[i].x][self.VacuumCleaners[i].y]
             if self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty:
                self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y].kill()
                self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y]=Dirt()
                self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty=False
                if ((cleaningAgentTile.x,cleaningAgentTile.y) in self.Dirts.dirts_array):
                    index=self.Dirts.dirts_array.index((cleaningAgentTile.x,cleaningAgentTile.y))
                    self.Dirts.dirts_array.pop(index)
             d_copy=deepcopy(self.Dirts.dirts_array)
             score,tile,d_tile=minimax.minimaxmulti(False,3,self.getCleaningAgentsTiles(),i,self.getDirtAgentsTiles(),0,self.Tiles.tiles,d_copy,self.counts)
             self.VacuumCleaners[i].move(tile.x-self.VacuumCleaners[i].x,tile.y-self.VacuumCleaners[i].y)
             self.draw()
             pygame.event.pump()



        


        pass
    def getCleaningAgentsTiles(self):
        cleaning_agents_tiles=[]
        for VacuumCleaner in self.VacuumCleaners:
            cleaning_agent_tile=self.Tiles.tiles[VacuumCleaner.x][VacuumCleaner.y]
            cleaning_agents_tiles.append(cleaning_agent_tile)
        return cleaning_agents_tiles
    def getDirtAgentsTiles(self):
        dirt_agents_tiles=[]
        for DirtAgent in self.DirtAgents:
            dirt_agent_tile=self.Tiles.tiles[DirtAgent.x][DirtAgent.y]
            dirt_agents_tiles.append(dirt_agent_tile)
        return dirt_agents_tiles


    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping :
                self.handle_events()
                self.draw()