import pygame
import constants
import math
class Dirt(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0,TILE_WIDTH=0,TILE_HEIGHT=0):
        super().__init__()
        self.x=x
        self.y=y
        self.TILE_WIDTH= TILE_WIDTH
        self.TILE_HEIGHT= TILE_HEIGHT
        self.filepath = "images/dirt.gif"
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        vacuumsize= self.TILE_WIDTH if (self.TILE_HEIGHT>self.TILE_WIDTH) else self.TILE_HEIGHT
        self.image = pygame.transform.scale(self.image, (round(vacuumsize*1), round(vacuumsize*1)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.TILE_WIDTH, self.y * self.TILE_HEIGHT)

    def move(self, dx=0, dy=0, walls=None):
        if not self._collide_with_walls(dx, dy, walls):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * self.TILE_WIDTH, dy * self.TILE_HEIGHT)

class Dirts:
    def __init__(self,n,m):
        self.n=n
        self.m=m 
        self.TILE_WIDTH=(constants.SCREEN_WIDTH)/n
        self.TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m
        self.dirts=[[Dirt() for x in range(m)] for y in range(n)]
        # for i in range(n):
        #     for j in range(m):
        #         # TILE_WIDTH=(constants.SCREEN_WIDTH)/n
        #         # TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m
        #         tile = Dirt(i,j,self.TILE_WIDTH,self.TILE_HEIGHT)
        #         self.dirts[i][j]=tile

    def __getitem__(self, item):
        return self.dirts[item]

    def addDirt(self,mouse_x,mouse_y,check):
        constants.SCREEN_WIDTH
        constants.SCREEN_HEIGHT
        x=math.floor(mouse_x/self.TILE_WIDTH)
        y=math.floor((mouse_y)/self.TILE_HEIGHT)
        if y<=self.m -1 and check and self.dirts[x][y].TILE_HEIGHT==0:
            dirt = Dirt(x,y,self.TILE_WIDTH,self.TILE_HEIGHT)
            self.dirts[x][y]=dirt
            # print(x)
            # print(y)
    def addDirtXY(self,x,y,check):
        if y<=self.m -1 and check and self.dirts[x][y].TILE_HEIGHT==0:
            dirt = Dirt(x,y,self.TILE_WIDTH,self.TILE_HEIGHT)
            self.dirts[x][y]=dirt
    def clearDirts(self):
        self.dirts=[[Dirt() for x in range(self.m)] for y in range(self.n)]



        


        

