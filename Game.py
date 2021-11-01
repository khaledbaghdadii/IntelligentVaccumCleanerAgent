import pygame
import random as rnd
from pygame import color
from pygame import font
from Checkbox import Checkbox
from InputText import InputBox
from VacuumCleaner import VacuumCleaner
from Wall import Walls
import constants
from Tiles import Tile, Tiles
from Dirt import Dirt, Dirts
from BFS import BFS
from time import sleep
from Button import Button

class Game:
    def __init__(self,n,m):
        self.n=n
        self.m=m
        self.init_pygame()
        self.Tiles=Tiles(n,m)
        self.Dirts=Dirts(n,m)
        self.Walls = Walls(n,m)
        self.VacuumCleaner= VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT)
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping=True
        self.dirt_checkbox= Checkbox(self.screen,50,520,1,caption="Dirt")
        self.wall_checkbox= Checkbox(self.screen,150,520,2,caption="Wall")
        self.agent_checkbox= Checkbox(self.screen,250,520,2,caption="Place Agent")
        self.reset_btn= Button("Reset",(50,600),font=20)
        self.rnd_dirts_btn= Button("Random Dirts",(150,600),font=20)
        self.grid_btn= Button("Generate Grid",(300,600),font=20)
        self.rnd_walls_btn=Button("Random Walls",(450,600),font=20)

        self.input_txt=InputBox(50,650,80,30)
        self.checkboxes=[self.dirt_checkbox,self.wall_checkbox,self.agent_checkbox]
        self.initialized=False
    def init_pygame(self):
        pygame.init()
        self.BG_COLOR = constants.BG_COLOR
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Enter {}".format(constants.TITLE))
        self.screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 40)
       
    def update_classes(self):
        for tile in self.Tiles:
            self.all_sprites.add(tile)
            # print(type(tile))
        for dirt in self.Dirts :
            self.all_sprites.add(dirt)
        
        for wall in self.Walls:
            self.all_sprites.add(wall)
                # print("dirt")
        self.VacuumCleaner.kill()
        self.all_sprites.add(self.VacuumCleaner)
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----

        
        self.dirt_checkbox.render_checkbox()
        self.wall_checkbox.render_checkbox()
        self.agent_checkbox.render_checkbox()
        self.screen.blit(self.reset_btn.surface, (self.reset_btn.x, self.reset_btn.y))
        self.screen.blit(self.rnd_dirts_btn.surface, (self.rnd_dirts_btn.x, self.rnd_dirts_btn.y))
        self.screen.blit(self.grid_btn.surface, (self.grid_btn.x, self.grid_btn.y))
        self.screen.blit(self.rnd_walls_btn.surface, (self.rnd_walls_btn.x, self.rnd_walls_btn.y))
        self.input_txt.draw(self.screen)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
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
                    
                    self.clean(0,0,self.Tiles.tiles)
                
            for box in self.checkboxes:
                    box.update_checkbox(event)
                    if box.checked is True:
                        for b in self.checkboxes:
                            if b != box:
                                b.checked = False
            self.input_txt.handle_event(event)
            # self.dirt_checkbox.update_checkbox(event)
            # self.wall_checkbox.update_checkbox(event)
            # self.agent_checkbox.update_checkbox(event)
            if event.type ==pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x=pygame.mouse.get_pos()[0]
                    y=pygame.mouse.get_pos()[1]
                    self.Dirts.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Tiles.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Walls.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
                    self.Tiles.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
                    self.VacuumCleaner.addAgent(x,y,check=self.agent_checkbox.checked,n=self.n,m=self.m)
                    if self.reset_btn.rect.collidepoint(x,y):
                        self.__init__(self.n,self.m)
                    if self.rnd_dirts_btn.rect.collidepoint(x,y):
                        self.randomDirts(self.Tiles.tiles)
                    if self.grid_btn.rect.collidepoint(x,y):
                        self.generateGrid()
                    if self.rnd_walls_btn.rect.collidepoint(x,y):
                        self.randomWalls()
                    # for dirt in self.Dirts:
                    #     for a in dirt:
                    #         print(type(a))
                    # print(self.Dirts)
                    self.draw()
                    # print(pygame.mouse.get_pos())
    def clean(self,x,y,tiles):
        bfs=BFS(tiles)
        bfs.clean(self.VacuumCleaner.x,self.VacuumCleaner.y)
        dirtsArray= bfs.getDirts()
        if (self.VacuumCleaner.x,self.VacuumCleaner.y) in dirtsArray:
            self.Dirts.dirts[self.VacuumCleaner.x][self.VacuumCleaner.y].kill()
            self.Dirts.dirts[self.VacuumCleaner.x][self.VacuumCleaner.y]=Dirt()

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
                        #call move vacuum cleaner method
                        self.VacuumCleaner.move(dx,dy)
                        
                        self.draw()
                        sleep(0.5)
                        previousTile=tile
    def randomDirts(self,tiles):
        self.Tiles=Tiles(self.n,self.m)
        self.Dirts=Dirts(self.n,self.m)
        self.VacuumCleaner=VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,self.VacuumCleaner.x,self.VacuumCleaner.y)
        for i in tiles:
            for j in i:
                random_dirt=rnd.getrandbits(3)
                if random_dirt==1:
                    j.isDirty=True
                    # print(j.x)
                    self.Dirts.addDirtXY(j.x,j.y,True)
                    self.Tiles.addDirtXY(j.x,j.y,True)
                else:
                    j.isDirty=False
    def generateGrid(self):
        try:
            size=self.input_txt.text.split(",")
            n=int(size[0])
            m=int(size[1])
            self.__init__(n,m)
        except:
            self.input_txt=InputBox(50,650,80,30)
            self.input_txt.draw(self.screen)
    def randomWalls(self):
        tiles=self.Tiles.tiles
        self.Tiles=Tiles(self.n,self.m)
        self.Walls=Walls(self.n,self.m)
        self.VacuumCleaner=VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT,self.VacuumCleaner.x,self.VacuumCleaner.y)
        for i in tiles:
            for j in i:
                
                random_dirt=rnd.getrandbits(3)
                if random_dirt==0:
                    j.has_walls_up=True
                    # print(j.x)
                    self.Walls.addWallXY(j.x,j.y,True,"up")
                    self.Tiles.addWallXY(j.x,j.y,True,"up")
                elif random_dirt==1:
                    j.has_walls_down=True
                    self.Walls.addWallXY(j.x,j.y,True,"down")
                    print(j.x,j.y)
                    self.Tiles.addWallXY(j.x,j.y,True,"down")
                elif random_dirt==2:
                    j.has_walls_right=True
                    self.Walls.addWallXY(j.x,j.y,True,"right")
                    self.Tiles.addWallXY(j.x,j.y,True,"right")
                elif random_dirt==3:
                    j.has_walls_left=True
                    self.Walls.addWallXY(j.x,j.y,True,"left")
                    self.Tiles.addWallXY(j.x,j.y,True,"left")
                


    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping :
                self.handle_events()
                self.draw()
