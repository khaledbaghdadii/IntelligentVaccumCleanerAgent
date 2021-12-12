import pygame
import constants
import math
class DirtAgent(pygame.sprite.Sprite):
    def __init__(self,TILE_WIDTH,TILE_HEIGHT,x=0,y=0):
        super().__init__()
        self.x=x
        self.y=y
        self.TILE_WIDTH= TILE_WIDTH
        self.TILE_HEIGHT= TILE_HEIGHT
        self.count=0
        self.filepath = "images/dog1.png"
        self.dirts_of_agent=[]
        self.remaining_uncleaned=0
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        vacuumsize= self.TILE_WIDTH if (self.TILE_HEIGHT>self.TILE_WIDTH) else self.TILE_HEIGHT
        self.image = pygame.transform.scale(self.image, (round(vacuumsize*1), round(vacuumsize*1)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x * self.TILE_WIDTH, self.y * self.TILE_HEIGHT)

    def move(self, dx=0, dy=0):
            self.x += dx
            self.y += dy
            self.rect = self.rect.move(dx * self.TILE_WIDTH, dy * self.TILE_HEIGHT)
    
    
    def addAgent(self,mouse_x,mouse_y,check,n,m):
        constants.SCREEN_WIDTH
        constants.SCREEN_HEIGHT
        x=math.floor(mouse_x/self.TILE_WIDTH)
        y=math.floor((mouse_y)/self.TILE_HEIGHT)
        if y<=m -1 and check :
            self.__init__(self.TILE_WIDTH,self.TILE_HEIGHT,x,y)
            

