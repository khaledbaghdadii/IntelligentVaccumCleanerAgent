import pygame
from pygame import color
from Checkbox import Checkbox
from VacuumCleaner import VacuumCleaner
from Wall import Walls
import constants
from Tiles import Tiles
from Dirt import Dirt, Dirts
from BFS import BFS
from time import sleep
class Game:
    def __init__(self,n,m):
        self.init_pygame()
        self.Tiles=Tiles(n,m)
        self.Dirts=Dirts(n,m)
        self.Walls = Walls(n,m)
        self.VacuumCleaner= VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT)
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping=True
        self.dirt_checkbox= Checkbox(self.screen,50,520,1,caption="Dirt")
        self.wall_checkbox= Checkbox(self.screen,150,520,2,caption="Wall")
        
    
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
        self.VacuumCleaner.kill()
        for wall in self.Walls:
            self.all_sprites.add(wall)
                # print("dirt")
        self.all_sprites.add(self.VacuumCleaner)
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        
        self.dirt_checkbox.render_checkbox()
        self.wall_checkbox.render_checkbox()
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
                elif event.key ==pygame.K_RETURN:
                    self.clean(0,0,self.Tiles.tiles)

            self.dirt_checkbox.update_checkbox(event)
            self.wall_checkbox.update_checkbox(event)
            if event.type ==pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.Dirts.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Tiles.addDirt(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.dirt_checkbox.checked)
                    self.Walls.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
                    self.Tiles.addWall(mouse_x=pygame.mouse.get_pos()[0],mouse_y=pygame.mouse.get_pos()[1],check=self.wall_checkbox.checked)
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


    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
