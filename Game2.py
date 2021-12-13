
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
from Algorithms.PartiallyObservable import PartiallyObservable
import math
import constants
class Game2:
    def __init__(self,n,m):
        self.n=n
        self.m=m
        self.init_pygame()
        self.Tiles=Tiles(n,m)
        self.Dirts=Dirts(n,m)
        self.Walls = Walls(n,m)
        self.VacuumCleaners= []
        self.DirtAgents=[]
        self.vacuum_cleaners_indices = []
        self.dirt_agents_indices = []
        self.current_vacuum_index=0
        self.current_dirt_agent_index=0
        self.selected_cleaner_index=0
        self.selected_dirt_agent_index= 0
        self.stepsAheadDirtAgent=5
        self.stepsAheadCleaner=5
        self.counts=[]
        self.cross_scores=[]
        self.added_agents_on_gui=[]
        self.DirtAgent= DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,0,1)
        self.DirtAgent2= DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,3,4)
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping=True

        # self.dirt_checkbox= Checkbox(self.screen,30,520,1,caption="Dirt")
        # self.wall_checkbox= Checkbox(self.screen,110,520,2,caption="Wall")
        # self.agent_checkbox= Checkbox(self.screen,210,520,2,caption="Place Agent")
        
        # self.rnd_dirts_btn= Button("Random Dirts",(10,560),font=25,bg=(200,150,50))
        # self.clear_dirts_btn= Button("Clear Dirts",(10,600),font=25,bg=(200,150,50))
        # self.rnd_walls_btn=Button("Random Walls",(200,560),font=25,bg=(200,150,50))
        # self.clear_walls_btn= Button("Clear Walls",(200,600),font=25,bg=(200,150,50))
        # self.dropdown=DropDown(530, 510, 150, 20,  "Select Speed", ["Very Slow", "Slow","Medium","Fast","Very Fast"])
        # self.algorithm_list=DropDown(350, 510, 150, 20,  "Select Algorithm", ["Modified BFS", "TSP+Best First Search","Djikstra","A*"])
        # self.random_dist_list=DropDown(350, 560, 180, 20,  "Select Random Distribution", ["Uniform: 50%", "Uniform: 12.5%"])
        # self.moves_label=TextLabel('No.  Moves: 0',600,560,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        # self.explored_label=TextLabel('No.  Explored:0 ',600,600,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        # self.input_txt=InputBox(200,650,80,30)
        # self.textlabel=TextLabel('Write in form "n,m"',100,665,font_background=(255,255,255))

        # self.grid_btn= Button("Generate Grid",(300,650),font=25,bg=(100, 80, 255),text_color="Black")
        # self.reset_btn= Button("  Reset  ",(500,650),font=25,bg=(255, 100, 100),text_color="Black")
        # self.start_btn= Button("  Start  ",(600,650),font=25,bg=(100, 140, 60),text_color="Black")
        # self.checkboxes=[self.dirt_checkbox,self.wall_checkbox,self.agent_checkbox]

        #GUI From Below
        self.controllers=TextLabel('Controllers',65,520,font_background=(255,255,255))
        self.geneartors=TextLabel('Generators',300,520,font_background=(255,255,255))
        self.restters=TextLabel('Resetters',450,520,font_background=(255,255,255))
        self.dirt_checkbox= Checkbox(self.screen,10,550,1,caption="Place Dirt")
        self.wall_checkbox= Checkbox(self.screen,10,590,2,caption="Place Wall")
        self.agent_checkbox= Checkbox(self.screen,10,630,2,caption="Place Cleaning Agent")
        self.dirt_agent_checkbox= Checkbox(self.screen,10,670,2,caption="Place Dirt Agent")
        self.random_dist_list=DropDown(250, 550, 120, 30,  "Randomness %", ["Uniform: 50%", "Uniform: 12.5%"])
        self.rnd_dirts_btn= Button("Random Dirts",(250, 600),font=25,bg=(200,150,50))
        self.rnd_walls_btn=Button("Random Walls",(250,650),font=25,bg=(200,150,50))
        self.clear_dirts_btn= Button("Clear Dirts",(400,550),font=25,bg=(200,150,50))
        self.clear_walls_btn= Button("Clear Walls",(400,600),font=25,bg=(200,150,50))
        self.recharge_btn= Button("Recharge All",(530,550),font=25,bg=(200,150,50))
        self.dropdown=DropDown(530, 510, 150, 30,  "Select Speed", ["Very Slow", "Slow","Medium","Fast","Very Fast"])



        #GUI From the right side
        self.textlabel=TextLabel('Write in form "n,m"',800,10,font_background=(255,255,255))
        self.input_txt=InputBox(710,30,80,30)
        self.grid_btn= Button("Generate Grid",(800,30),font=25,bg=(100, 80, 255),text_color="Black")
        self.obs=TextLabel('Observablity',770,90,font_background=(255,255,255))
        self.observablity=DropDown(710, 110, 180, 30,  "Select Agent's Observability", ["Fully Observable", "Partially Observable"])
        self.visibility=TextLabel('Visibility',970,90,font_background=(255,255,255))
        self.visibility_txt=InputBox(928,110,80,30)
        self.set_vis_btn= Button("Set Visiblity",(1020,110),font=25,bg=(255, 100, 100),text_color="Black")
        self.singleAgentLabel=TextLabel('For Single Agent:',800,170,font_background=(255,255,255))
        self.algorithm_list=DropDown(710, 200, 150, 30,  "Select Algorithm", ["Modified BFS", "TSP+Best First Search","Djikstra","A*"])
        self.vacuumCleanerLabel=TextLabel('For Vacuum Cleaner #1',820,270,font_background=(255,255,255))
        self.add_vacuum_checkbox= Checkbox(self.screen,710,290,1,caption="Add Vacuum Cleaner")
        self.stepAheadLabel=TextLabel('Steps Ahead:',770,340,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.steps_ahead_cleaner_input=InputBox(840,320,80,30)
        self.multialgo_dropdown=DropDown(880, 370, 150, 30, "Select Algorithm", ["Minimax", "Alpha-Beta", "Random", "Alpha Beta - Random", "Minimax - Random"])

        self.dirtAgentLabel=TextLabel('For Dirt Agent #0',1050,270,font_background=(255,255,255))
        self.add_dirt_agent_checkbox= Checkbox(self.screen,975,290,1,caption="Add Dirt Agent")
        self.stepAhead2Label=TextLabel('Steps Ahead:',1030,340,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.steps_ahead_dirtier_input=InputBox(1100,320,80,30)
        # self.dirt_dropdown=DropDown(980, 370, 150, 30,  "Select Algorithim", ["Minimax", "Alpha-Beta","Random"])

        self.performanceLabel=TextLabel('Cleaners Performance',820,430,font_background=(255,255,255))
        self.multiCleaners=DropDown(840, 450, 80, 30,  "1", self.vacuum_cleaners_indices)
        self.moves_label=TextLabel('Number of Moves: 0',800,500,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.explored_label=TextLabel('Number of Explored: 0 ',810,530,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        #self.moves_required_label=TextLabel('Number of Moves Required: 0 ',840,560,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.battery=TextLabel('Battery%: 0 ',770,560,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))


        self.performanceLabel2=TextLabel('Dirtiers Performance',1080,430,font_background=(255,255,255))
        self.multiDirtiers=DropDown(1100, 450, 80, 30,  "0", self.dirt_agents_indices)
        self.moves_label2=TextLabel('Number of Moves: 0',1070,500,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.explored_label2=TextLabel('Number of Explored: 0 ',1080,530,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.moves_required_label2=TextLabel('Number of Moves Required: 0 ',840,560,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.battery2=TextLabel('Battery%: 0 ',1040,560,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))

        self.scores=TextLabel('Scores',750,600,font_background=(255,255,255))
        self.winnerCleanerAgent=TextLabel('Winner Cleaner Agent:     ',820,625,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.WinnerDirtAgent=TextLabel('Winner Dirt Agent:    ',805,650,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))
        self.BothAgent=TextLabel('Overall Winner:                      ',835,675,font_background=(255,255,255),font=pygame.font.SysFont(None, 25))

        self.reset_btn= Button("  Reset  ",(1100,650),font=25,bg=(255, 100, 100),text_color="Black")
        self.start_btn= Button("  Start   ",(1100,600),font=25,bg=(100, 140, 60),text_color="Black")
        self.checkboxes=[self.dirt_checkbox,self.wall_checkbox,self.agent_checkbox,self.dirt_agent_checkbox,self.add_vacuum_checkbox,self.add_dirt_agent_checkbox]

        self.initialized=False
        self.WAIT_TIME=0.5
        self.ALGORITHM="Modified BFS"

        #start with 1 vacuum cleaner
        self.VacuumCleaners.append(VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,0,0))
        self.VacuumCleaners[len(self.VacuumCleaners)-1].addAgent(0,0,check=self.add_vacuum_checkbox.checked,n=self.n,m=self.m)
        self.current_vacuum_index+=1
        self.vacuum_cleaners_indices.append(str(self.current_vacuum_index))
        self.selected_cleaner_index=self.multiCleaners.options[self.multiCleaners.active_option]
        self.added_agents_on_gui.append((0,0))
        #start with 1 dirt agent that will be ignored upon calling minimax
        # self.DirtAgents.append(DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,0,0))
        # # self.VacuumCleaners[len(self.VacuumCleaners)-1].addAgent(0,0,check=self.add_vacuum_checkbox.checked,n=self.n,m=self.m)
        # self.current_dirt_agent_index+=1
        # # self.dirt_agents_indices.append(str(self.current_dirt_agent_index))
        # # self.selected_dirt_agent_index=self.multiDirtiers.options[self.multiDirtiers.active_option]


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
        self.VacuumCleaners[int(self.selected_cleaner_index)-1].kill()

    def killDirtAgent(self):
        self.DirtAgents[int(self.selected_dirt_agent_index)-1].kill()

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
        self.dirt_agent_checkbox.render_checkbox()
        self.add_vacuum_checkbox.render_checkbox()
        self.add_dirt_agent_checkbox.render_checkbox()

        self.screen.blit(self.reset_btn.surface, (self.reset_btn.x, self.reset_btn.y))
        self.screen.blit(self.recharge_btn.surface,(self.recharge_btn.x, self.recharge_btn.y))
        self.screen.blit(self.start_btn.surface, (self.start_btn.x, self.start_btn.y))
        self.screen.blit(self.rnd_dirts_btn.surface, (self.rnd_dirts_btn.x, self.rnd_dirts_btn.y))
        self.screen.blit(self.clear_dirts_btn.surface, (self.clear_dirts_btn.x, self.clear_dirts_btn.y))
        self.screen.blit(self.grid_btn.surface, (self.grid_btn.x, self.grid_btn.y))
        self.screen.blit(self.rnd_walls_btn.surface, (self.rnd_walls_btn.x, self.rnd_walls_btn.y))
        self.screen.blit(self.clear_walls_btn.surface, (self.clear_walls_btn.x, self.clear_walls_btn.y))
        self.screen.blit(self.set_vis_btn.surface, (self.set_vis_btn.x, self.set_vis_btn.y))
        self.input_txt.draw(self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        self.textlabel.draw(self.screen)
        self.controllers.draw(self.screen)
        self.geneartors.draw(self.screen)
        self.restters.draw(self.screen)
        self.obs.draw(self.screen)
        self.visibility.draw(self.screen)
        self.visibility_txt.draw(self.screen)
        self.singleAgentLabel.draw(self.screen)
        self.vacuumCleanerLabel.draw(self.screen)
        self.stepAheadLabel.draw(self.screen)
        self.steps_ahead_cleaner_input.draw(self.screen)
        self.dirtAgentLabel.draw(self.screen)
        self.steps_ahead_dirtier_input.draw(self.screen)
        self.stepAhead2Label.draw(self.screen)
        self.performanceLabel.draw(self.screen)
        #self.moves_required_label.draw(self.screen)
        self.battery.draw(self.screen)
        self.scores.draw(self.screen)
        self.performanceLabel2.draw(self.screen)
        self.moves_label2.draw(self.screen)
        self.explored_label2.draw(self.screen)
        self.battery2.draw(self.screen)
        self.winnerCleanerAgent.draw(self.screen)
        self.WinnerDirtAgent.draw(self.screen)
        self.BothAgent.draw(self.screen)


        self.multiCleaners.draw(self.screen)
        self.multiDirtiers.draw(self.screen)
        self.dropdown.draw(self.screen)
        self.observablity.draw(self.screen)
        self.algorithm_list.draw(self.screen)
        self.multialgo_dropdown.draw(self.screen)
        # self.dirt_dropdown.draw(self.screen)
        self.random_dist_list.draw(self.screen)

        pygame.display.flip()

    def cleanMultiAgents(self):
        if(self.multialgo_dropdown.main == "Minimax"):
            print("minimax")
        if(self.multialgo_dropdown.main == "Alpha-Beta"):
            print("Alpha-Beta")
        if(self.multialgo_dropdown.main == "Random"):
            print("Random")
        self.draw()

    def updateSelectedAgents(self):
        self.selected_cleaner_index = int(self.multiCleaners.main)
        print("HERE SELECTED CLEANER",self.selected_cleaner_index)
        self.selected_dirt_agent_index = int(self.multiDirtiers.main)
        self.vacuumCleanerLabel.setText("For Vacuum Cleaner #"+str(self.selected_cleaner_index))
        self.dirtAgentLabel.setText("For Dirt Agent #"+str(self.selected_dirt_agent_index))
        # if self.selected_dirt_agent_index>0:
        #     self.selected_dirt_agent_index = self.multiDirtiers.options[self.multiDirtiers.active_option]
        print("HERE SELECTED DIRT AGENT",self.selected_dirt_agent_index)
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
            self.steps_ahead_cleaner_input.handle_event(event)
            self.steps_ahead_dirtier_input.handle_event(event)
            if event.type ==pygame.MOUSEBUTTONDOWN :
                self.dropdown.update(event)
                self.observablity.update(event)
                self.algorithm_list.update(event)
                self.random_dist_list.update(event)
                self.multialgo_dropdown.update(event)
                # self.dirt_dropdown.update(event)
                self.multiCleaners.update(event)
                self.multiDirtiers.update(event)

                if pygame.mouse.get_pressed()[0]:
                    x=pygame.mouse.get_pos()[0]
                    y=pygame.mouse.get_pos()[1]
                    self.Dirts.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Tiles.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Walls.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
                    self.Tiles.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)

                    self.updateSelectedAgents()

                    x1=math.floor(x/self.Tiles.TILE_WIDTH)
                    y1=math.floor((y)/self.Tiles.TILE_HEIGHT)

                    #Add vacuum cleaner and update dropdown
                    if(self.add_vacuum_checkbox.checked and y1<=self.m-1 and x1<=self.n-1 and ((x1,y1) not in self.added_agents_on_gui)):
                        self.VacuumCleaners.append(VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,x,y))
                        self.VacuumCleaners[len(self.VacuumCleaners)-1].addAgent(x,y,check=self.add_vacuum_checkbox.checked,n=self.n,m=self.m)
                        self.added_agents_on_gui.append((x1,y1))
                        self.current_vacuum_index+=1
                        self.vacuum_cleaners_indices.append(str(self.current_vacuum_index))
                        if self.steps_ahead_cleaner_input.text=="":
                            print("no steps ahead for cleaner")
                            pass
                        else:
                            self.VacuumCleaners[len(self.VacuumCleaners)-1].stepsAhead=int(self.steps_ahead_cleaner_input.text)
                            print("steps ahead input is ",self.steps_ahead_cleaner_input.text)

                    else:
                        pass

                    #move the vacuum cleaner
                    if self.agent_checkbox.checked:
                        self.killVacuumCleaner()
                        self.VacuumCleaners[int(self.selected_cleaner_index)-1].addAgent(x,y,check=self.agent_checkbox.checked,n=self.n,m=self.m)

                    #add dirt agents and update dropdown
                    if(self.add_dirt_agent_checkbox.checked and y1<=self.m-1 and x1<=self.n-1 and ((x1,y1) not in self.added_agents_on_gui)):
                        self.DirtAgents.append(DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,x,y))
                        self.DirtAgents[len(self.DirtAgents)-1].addAgent(x,y,check=self.add_dirt_agent_checkbox.checked,n=self.n,m=self.m)
                        self.added_agents_on_gui.append((x1,y1))
                        self.current_dirt_agent_index+=1
                        self.dirt_agents_indices.append(str(self.current_dirt_agent_index))
                        self.counts.append(0)
                        if self.steps_ahead_dirtier_input.text=="":
                            print("no steps ahead for dirt agent")
                            pass
                        else:
                            self.DirtAgents[len(self.DirtAgents)-1].stepsAhead=int(self.steps_ahead_dirtier_input.text)
                            print("steps ahead input is ",self.steps_ahead_dirtier_input.text)
                    else:
                        pass

                    #move the dirt agent
                    if self.dirt_agent_checkbox.checked:
                        if self.selected_dirt_agent_index>0:
                            self.killDirtAgent()
                            self.DirtAgents[int(self.selected_dirt_agent_index)-1].addAgent(x,y,check=self.dirt_agent_checkbox.checked,n=self.n,m=self.m)

                    if self.reset_btn.rect.collidepoint(x,y):
                        self.resetGrid()
                    if self.start_btn.rect.collidepoint(x,y):
                        self.setSpeed()

                        if len(self.DirtAgents)==0:
                            #single of project 1
                            if len(self.VacuumCleaners)==1:
                                self.clean(0,0,self.Tiles.tiles,self.Tiles)
                        else:
                            if self.multialgo_dropdown.main=="Minimax":
                                pass
                                for i in range(30):
                                    #self.startAllAgentsMiniMax()
                                    self.startAllAgentsMiniMax()
                                    self.getEvaluationScores()
                            elif self.multialgo_dropdown.main=="Alpha-Beta":
                                for i in range(30):
                                    #self.startAllAgentsMiniMax()
                                    self.startAllAgentsAlphaBeta()
                                    self.getEvaluationScores()
                            elif self.multialgo_dropdown.main=="Random":
                                pass
                                # for i in range(30):
                                #     #self.startAllAgentsMiniMax()
                                #     self.startAllDirtAgentsRandom()
                                #     self.getEvaluationScores()
                            elif self.multialgo_dropdown.main=="Alpha Beta - Random" or self.multialgo_dropdown.main=="Minimax - Random":
                                for i in range(30):
                                    #self.startAllAgentsMiniMax()
                                    self.startAllDirtAgentsRandom()
                                    self.getEvaluationScores()
                            else:
                                for i in range(30):
                                    self.startAllAgentsMiniMax()
                                    self.getEvaluationScores()
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


    # def cleanMiniMax(self,i):
    #     MiniMaxS=MiniMax()
    #     cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[i].x][self.VacuumCleaners[i].y]
    #     dirtAgentTile= self.Tiles.tiles[self.DirtAgents[0].x][self.DirtAgents[0].y]
    #     dirtAgent2Tile= self.Tiles.tiles[self.DirtAgents[1].x][self.DirtAgents[1].y]
    #     if self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty:
    #         self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y].kill()
    #         self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y]=Dirt()
    #         self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty=False
    #         if ((cleaningAgentTile.x,cleaningAgentTile.y) in self.Dirts.dirts_array):
    #             index=self.Dirts.dirts_array.index((cleaningAgentTile.x,cleaningAgentTile.y))
    #             self.Dirts.dirts_array.pop(index)
    #     print("dirts array passed",self.Dirts.dirts_array)
    #     d_copy=deepcopy(self.Dirts.dirts_array)
    #     score,tile,tile1,til2=MiniMaxS.minimax2(False,6,cleaningAgentTile,dirtAgentTile,dirtAgent2Tile,1,self.Tiles.tiles,d_copy,self.DirtAgents[0].count,self.DirtAgents[1].count)
    #     #score,tile,tile1=MiniMaxS.minimax(False,5,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,self.Dirts.dirts_array,self.DirtAgent.count)
    #
    #
    #     return score,tile
        

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
            for i,V in enumerate(self.DirtAgents):
                self.DirtAgents[i]= DirtAgent(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT)
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
    # def startDirtAgentRandom(self,i):
    #     prevPos=[]
    #     for i in range(1):
    #         neighbours=self.getNeighbours(self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y],self.Tiles.tiles)
    #         neighbourAvailable=False
    #         for j in range(len(neighbours)):
    #             if not (neighbours[j].x,neighbours[j].y) in prevPos:
    #                 neighbourAvailable=True
    #                 break
    #         if(not neighbourAvailable):
    #             prevPos=[]
    #         if(len(neighbours)>=1):
    #             n=rnd.randint(0,len(neighbours)-1)
    #             nextPosX=neighbours[n].x
    #             nextPosY=neighbours[n].y
    #             # print(neighbours)
    #             # print("n: ",n)
    #             prevPosX=self.DirtAgents[i].x
    #             prevPosY=self.DirtAgents[i].y
    #             #added to the list of visited positions
    #             prevPos.append((prevPosX,prevPosY))
    #             #make sure the next position is not visted before
    #             while((nextPosX,nextPosY) in prevPos):
    #                 n=rnd.randint(0,len(neighbours)-1)
    #                 nextPosX=neighbours[n].x
    #                 nextPosY=neighbours[n].y
    #
    #             dx=nextPosX-prevPosX
    #             dy=nextPosY-prevPosY
    #             # print(dx," , ",dy)
    #             m=rnd.randint(0,1)
    #
    #             if( self.DirtAgents[i].count%3==0):
    #                     self.Dirts.addDirtXY(prevPosX,prevPosY,True)
    #                     self.Tiles.addDirtXY(prevPosX,prevPosY,True)
    #             else:
    #                     pass
    #             self.DirtAgents[i].move(dx,dy)
    #             self.DirtAgents[i].count+=1
    #
    #
    #
    #             self.draw()
    #             sleep(self.WAIT_TIME)
    # def startSmartDirtAgent(self,i):
    #     print("Before moving firts array is :",self.Dirts.dirts_array)
    #     MiniMaxS=MiniMax()
    #     cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[0].x][self.VacuumCleaners[0].y]
    #     dirtAgentTile= self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y]
    #     if ((dirtAgentTile.x,dirtAgentTile.y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
    #             self.Dirts.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
    #             self.Tiles.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
    #     print("After adding dirts: ,",self.Dirts.dirts_array)
    #     d_copy=  deepcopy(self.Dirts.dirts_array)
    #     score,tile,tile1=MiniMaxS.minimax(True,3,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,d_copy,self.DirtAgents[i].count)
    #     #score,tile,tile1=MiniMaxS.minimax(True,5,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,self.Dirts.dirts_array,self.DirtAgent.count)
    #     self.DirtAgents[i].move(tile1.x-self.DirtAgents[i].x,tile1.y-self.DirtAgents[i].y)
    #     print("After moving firts array is :",self.Dirts.dirts_array)
    #
    #
    #     self.DirtAgent.count+=1
    #
    #     return score,tile
    #
    # def startSmartDirtAgent1(self,i):
    #     print("Before moving firts array is :",self.Dirts.dirts_array)
    #     MiniMaxS=MiniMax()
    #     cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[0].x][self.VacuumCleaners[0].y]
    #     dirtAgentTiles= [self.Tiles.tiles[self.DirtAgents[0].x][self.DirtAgents[0].y], self.Tiles.tiles[self.DirtAgents[1].x][self.DirtAgents[1].y]]
    #     if ((dirtAgentTiles[i].x,dirtAgentTiles[i].y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
    #             self.Dirts.addDirtXY(dirtAgentTiles[i].x,dirtAgentTiles[i].y,True)
    #             self.Tiles.addDirtXY(dirtAgentTiles[i].x,dirtAgentTiles[i].y,True)
    #     print("After adding dirts: ,",self.Dirts.dirts_array)
    #     d_copy=  deepcopy(self.Dirts.dirts_array)
    #     score,tile,tile1,tile2=MiniMaxS.minimax2(True,4,cleaningAgentTile,dirtAgentTiles[0],dirtAgentTiles[1],i+1,self.Tiles.tiles,d_copy,self.DirtAgents[0].count,self.DirtAgents[1].count)
    #     if(i==0):
    #     #score,tile,tile1=MiniMaxS.minimax(True,5,cleaningAgentTile,dirtAgentTile,self.Tiles.tiles,self.Dirts.dirts_array,self.DirtAgent.count)
    #         self.DirtAgents[i].move(tile1.x-self.DirtAgents[i].x,tile1.y-self.DirtAgents[i].y)
    #     if(i==1):
    #         self.DirtAgents[i].move(tile2.x-self.DirtAgents[i].x,tile2.y-self.DirtAgents[i].y)
    #     print("After moving firts array is :",self.Dirts.dirts_array)
    #
    #
    #     self.DirtAgents[i].count+=1


    def startAllAgentsMiniMax(self):
        for i in range(len(self.DirtAgents)):
             minimax= MiniMax()
             dirtAgentTile= self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y]
             if ((dirtAgentTile.x,dirtAgentTile.y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
                self.Dirts.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
                self.Tiles.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
                self.DirtAgents[i].dirts_of_agent.append((dirtAgentTile.x,dirtAgentTile.y))
             d_copy=  deepcopy(self.Dirts.dirts_array)
             score,t,d_tile=minimax.minimaxmulti(True,self.DirtAgents[i].stepsAhead,self.getCleaningAgentsTiles(),0,self.getDirtAgentsTiles(),i,self.Tiles.tiles,d_copy,self.counts)
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
                    self.VacuumCleaners[i].dirts_cleaned.append((cleaningAgentTile.x,cleaningAgentTile.y))
             d_copy=deepcopy(self.Dirts.dirts_array)
             score,tile,d_tile=minimax.minimaxmulti(False,self.VacuumCleaners[i].stepsAhead,self.getCleaningAgentsTiles(),i,self.getDirtAgentsTiles(),0,self.Tiles.tiles,d_copy,self.counts)
             self.VacuumCleaners[i].move(tile.x-self.VacuumCleaners[i].x,tile.y-self.VacuumCleaners[i].y)
             self.draw()
             pygame.event.pump()

        pass
    def startAllAgentsAlphaBeta(self):
        alpha=-float('inf')
        beta=float('inf')
        for i in range(len(self.DirtAgents)):
             minimax= MiniMax()
             dirtAgentTile= self.Tiles.tiles[self.DirtAgents[i].x][self.DirtAgents[i].y]
             if ((dirtAgentTile.x,dirtAgentTile.y) not in self.Dirts.dirts_array and self.DirtAgents[i].count%3==0):
                self.Dirts.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
                self.Tiles.addDirtXY(dirtAgentTile.x,dirtAgentTile.y,True)
                self.DirtAgents[i].dirts_of_agent.append((dirtAgentTile.x,dirtAgentTile.y))
             d_copy=  deepcopy(self.Dirts.dirts_array)
             score,t,d_tile=minimax.alphabetamulti(True,-float('inf'),float('inf'),5,self.getCleaningAgentsTiles(),0,self.getDirtAgentsTiles(),i,self.Tiles.tiles,d_copy,self.counts)
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
                    self.VacuumCleaners[i].dirts_cleaned.append((cleaningAgentTile.x,cleaningAgentTile.y))
             d_copy=deepcopy(self.Dirts.dirts_array)
             score,tile,d_tile=minimax.alphabetamulti(False,-float('inf'),float('inf'),5,self.getCleaningAgentsTiles(),i,self.getDirtAgentsTiles(),0,self.Tiles.tiles,d_copy,self.counts)
             self.VacuumCleaners[i].move(tile.x-self.VacuumCleaners[i].x,tile.y-self.VacuumCleaners[i].y)
             self.draw()
             pygame.event.pump()

        pass

    def startAllDirtAgentsRandom(self):
        for i in range(len(self.DirtAgents)):
            self.startDirtAgentRandom(i)
        ##if vacuum cleaner minimax
        if self.multialgo_dropdown.main=="Minimax - Random":
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
                        self.VacuumCleaners[i].dirts_cleaned.append((cleaningAgentTile.x,cleaningAgentTile.y))
                d_copy=deepcopy(self.Dirts.dirts_array)
                score,tile,d_tile=minimax.minimaxmulti(False,5,self.getCleaningAgentsTiles(),i,self.getDirtAgentsTiles(),0,self.Tiles.tiles,d_copy,self.counts)
                self.VacuumCleaners[i].move(tile.x-self.VacuumCleaners[i].x,tile.y-self.VacuumCleaners[i].y)
                self.draw()
                pygame.event.pump()
        else:        
        ##if vacuum cleaner alphabeta
         minimax= MiniMax()
         cleaningAgentTile= self.Tiles.tiles[self.VacuumCleaners[i].x][self.VacuumCleaners[i].y]
         if self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty:
            self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y].kill()
            self.Dirts.dirts[cleaningAgentTile.x][cleaningAgentTile.y]=Dirt()
            self.Tiles.tiles[cleaningAgentTile.x][cleaningAgentTile.y].isDirty=False
            if ((cleaningAgentTile.x,cleaningAgentTile.y) in self.Dirts.dirts_array):
                index=self.Dirts.dirts_array.index((cleaningAgentTile.x,cleaningAgentTile.y))
                self.Dirts.dirts_array.pop(index)
                self.VacuumCleaners[i].dirts_cleaned.append((cleaningAgentTile.x,cleaningAgentTile.y))
         d_copy=deepcopy(self.Dirts.dirts_array)
         score,tile,d_tile=minimax.alphabetamulti(False,-float('inf'),float('inf'),5,self.getCleaningAgentsTiles(),i,self.getDirtAgentsTiles(),0,self.Tiles.tiles,d_copy,self.counts)
         self.VacuumCleaners[i].move(tile.x-self.VacuumCleaners[i].x,tile.y-self.VacuumCleaners[i].y)
         self.draw()
         pygame.event.pump()
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


    def getEvaluationScores(self):
        max_uncleaned=-float('inf')
        winner_among_dirt_agents_index=0
        max_cleaned=-float('inf')
        winner_among_cleaner_agents_index=0
        #evaluation measures
        for i in range(len(self.VacuumCleaners)):
            self.VacuumCleaners[i].total_num_cleaned=len(self.VacuumCleaners[i].dirts_cleaned)
        for i in range(len(self.DirtAgents)):
            self.DirtAgents[i].remaining_uncleaned= len(self.DirtAgents[i].dirts_of_agent)
        for i in range(len(self.VacuumCleaners)):
            for cleaned_tile in self.VacuumCleaners[i].dirts_cleaned:
                for j in range(len(self.DirtAgents)):
                    if cleaned_tile in self.DirtAgents[j].dirts_of_agent:
                        self.DirtAgents[j].remaining_uncleaned-=1


        #winner among dirt agents
        for i in range(len(self.DirtAgents)):
            temp = self.DirtAgents[i].remaining_uncleaned/len(self.DirtAgents[i].dirts_of_agent)
            if(temp>max_uncleaned):
                winner_among_dirt_agents_index=i
                max_uncleaned=temp
            print("Remaining uncleaned of dirt agent ",i+1,": ", self.DirtAgents[i].remaining_uncleaned," out of ",len(self.DirtAgents[i].dirts_of_agent))

        print("Winner among dirt agents is agent number ", winner_among_dirt_agents_index+1)
        self.WinnerDirtAgent.setText("Winner Dirt Agent:"+str(winner_among_dirt_agents_index+1)+str(" (")+str(self.DirtAgents[i].x)+str(",") +str(self.DirtAgents[i].y)+str(")"))
        #winner among cleaning agents
        for i in range(len(self.VacuumCleaners)):
            if(self.VacuumCleaners[i].total_num_cleaned>max_cleaned):
                winner_among_cleaner_agents_index=i
                max_cleaned=self.VacuumCleaners[i].total_num_cleaned
            print("Number of tiles cleaned by agent ",i+1,": ",self.VacuumCleaners[i].total_num_cleaned)
        print("Winner among cleaner agents is agent number ", winner_among_cleaner_agents_index+1)
        self.winnerCleanerAgent.setText("Winner Cleaner Agent:"+str(winner_among_cleaner_agents_index+1)+str(" (")+str(self.VacuumCleaners[i].x)+str(",") +str(self.VacuumCleaners[i].y)+str(")"))
        #cross scores
        for i in range(len(self.VacuumCleaners)):
            for j in range(len(self.DirtAgents)):
                cleaned_out_of_dirts=0
                for cleaned_tile in self.VacuumCleaners[i].dirts_cleaned:
                    if cleaned_tile in self.DirtAgents[j].dirts_of_agent:
                        cleaned_out_of_dirts+=1
                score_cleaner = cleaned_out_of_dirts/len(self.DirtAgents[j].dirts_of_agent)
                score_dirt_agent = self.DirtAgents[j].remaining_uncleaned/len(self.DirtAgents[j].dirts_of_agent)
                if score_cleaner>=score_dirt_agent:
                    self.cross_scores.append((0,score_cleaner, i)) #cleaner is 0, dirt agent is 1
                else:
                    self.cross_scores.append((1,score_dirt_agent,j))
        print(self.cross_scores)
        max_score=-float('inf')
        overall_winner_index = 0
        winner_type = 0
        for i in range(len(self.cross_scores)):
            if self.cross_scores[i][1]>max_score:
                max_score=self.cross_scores[i][1]
                overall_winner_index=self.cross_scores[i][2]
                winner_type= self.cross_scores[i][0]

        print("Overall winner is:  ")
        if winner_type == 0:
            print("Cleaner agent ",overall_winner_index)
            self.BothAgent.setText("Overall Winner - Cleaner: "+str(overall_winner_index+1)+str(" (")+str(self.VacuumCleaners[overall_winner_index].x)+str(",") +str(self.VacuumCleaners[overall_winner_index].y)+str(")"))

        else:
            self.BothAgent.setText("Overall Winner - Dirt Agent: "+str(overall_winner_index+1)+str(" (")+str(self.DirtAgents[overall_winner_index].x)+str(",") +str(self.DirtAgents[overall_winner_index].y)+str(")"))
            print("Dirt agent ",overall_winner_index)


#project one stuff
    def clean(self,x,y,tiles,tiles_object):
        if self.algorithm_list.main=="Modified BFS":
            self.ALGORITHM="Modified BFS"
            self.cleanBFSVariants(x,y,tiles)

        elif self.algorithm_list.main=="TSP+Best First Search":
            self.ALGORITHM="TSP+Best First Search"
            self.cleanTSP(tiles_object)

        elif self.algorithm_list.main=="Djikstra":
            self.ALGORITHM="Djikstra"
            self.cleanBFSVariants(x,y,tiles)

        elif self.algorithm_list.main=="A*":
            self.ALGORITHM="A*"
            self.cleanBFSVariants(x,y,tiles)

        else:
            self.cleanBFSVariants(x,y,tiles)
    def cleanBFSVariants(self,x,y,tiles):
        if self.observablity.main=="Partially Observable":
            bfs=PartiallyObservable(self.Tiles.tiles)
        else:
            if(self.ALGORITHM=="Modified BFS"):
                bfs=BFS(tiles)
            elif(self.ALGORITHM=="Djikstra"):
                bfs=Djikstra(tiles)
            elif(self.ALGORITHM=="A*"):
                bfs=Astar(tiles)
            else:
                bfs=BFS(tiles)

        bfs.clean(self.VacuumCleaners[0].x,self.VacuumCleaners[0].y)
        dirtsArray= bfs.getDirts()
        if (self.VacuumCleaners[0].x,self.VacuumCleaners[0].y) in dirtsArray:
            self.Dirts.dirts[self.VacuumCleaners[0].x][self.VacuumCleaners[0].y].kill()
            self.Dirts.dirts[self.VacuumCleaners[0].x][self.VacuumCleaners[0].y]=Dirt()
        for i in bfs.path:
            if(len(i)!=0):
                previousTile=i[0]
                if (previousTile.x,previousTile.y) in dirtsArray:
                    self.Dirts.dirts[previousTile.x][previousTile.y].kill()
                    self.Dirts.dirts[previousTile.x][previousTile.y]=Dirt()


                if(len(i)>1):
                    for tile in i[1:]:
                        dx=tile.x-previousTile.x
                        dy=tile.y-previousTile.y
                        currentTile=(tile.x,tile.y)
                        if(currentTile in dirtsArray):
                            self.Dirts.dirts[tile.x][tile.y].kill()
                            self.Dirts.dirts[tile.x][tile.y]=Dirt()
                        # call move vacuum cleaner method
                        self.VacuumCleaners[0].move(dx,dy)

                        self.draw()
                        sleep(self.WAIT_TIME)
                        pygame.event.pump()
                        previousTile=tile
        self.moves_label.setText("No.  Moves: "+str(bfs.moves-1))
        self.explored_label.setText("No. Explored: "+str(bfs.num_explored))
    def cleanTSP(self,tiles_object):
        paths,num_explored,moves=generatePathsList(tiles_object,self.VacuumCleaners[0])
        tiles=[]
        for path in paths:
            for tileXY in path:
                tileX=tileXY[0]
                tileY=tileXY[1]
                tile=self.Tiles.tiles[tileX][tileY]
                tiles.append(tile)
        vacuumX=self.VacuumCleaners[0].x
        vacuumY=self.VacuumCleaners[0].y
        if self.Tiles.tiles[vacuumX][vacuumY].isDirty:
            self.Dirts.dirts[vacuumX][vacuumY].kill()
            self.Dirts.dirts[vacuumX][vacuumY]=Dirt()
            self.Tiles.tiles[vacuumX][vacuumY].isDirty=False
        for i in range(len(tiles)-1):
            currentTile=tiles[i]
            nextTile=tiles[i+1]
            dx=nextTile.x-currentTile.x
            dy=nextTile.y-currentTile.y
            self.VacuumCleaners[0].move(dx,dy)
            if nextTile.isDirty:
                self.Dirts.dirts[nextTile.x][nextTile.y].kill()
                self.Dirts.dirts[nextTile.x][nextTile.y]=Dirt()
                self.Tiles.tiles[nextTile.x][nextTile.y].isDirty=False
            self.moves_label.setText("No.  Moves: "+str(moves))
            self.explored_label.setText("No.  Explored Nodes: "+str(num_explored))
            self.draw()
            pygame.event.pump()
            sleep(self.WAIT_TIME)
        pass


    def startDirtAgentRandom(self,i):
        dirt_agent=self.DirtAgents[i]
        dirt_agent_tile=self.Tiles.tiles[dirt_agent.x][dirt_agent.y]
        neighbours=self.getNeighbours(dirt_agent_tile,self.Tiles.tiles)


        nextX=dirt_agent.x
        nextY=dirt_agent.y
        n=rnd.randint(0,len(neighbours)-1)
        print("n: ",n)
        dirt_agent_next=neighbours[n]
        nextX=dirt_agent_next.x
        nextY=dirt_agent_next.y

        dx=nextX-dirt_agent.x
        dy=nextY-dirt_agent.y

        if(self.counts[i]%3==0 and (dirt_agent.x,dirt_agent.y) not in self.Dirts.dirts):
            self.Dirts.addDirtXY(dirt_agent.x,dirt_agent.y,True)
            self.Tiles.addDirtXY(dirt_agent.x,dirt_agent.y,True)
            self.DirtAgents[i].dirts_of_agent.append((dirt_agent.x,dirt_agent.y))
        self.counts[i]+=1
        self.DirtAgents[i].move(dx,dy)