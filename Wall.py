import pygame
import constants
import math
class Wall(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0,position="up",TILE_WIDTH=0,TILE_HEIGT=0):
        super().__init__()
        self.x = x
        self.y = y

        self.position=position
        
        
        self.filepath = "images/"+position+"_wall.png"
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (round(TILE_WIDTH), round(TILE_HEIGT)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * TILE_WIDTH, y * TILE_HEIGT)

class Walls():
    def __init__(self,n,m):
        self.walls=[]
        self.n=n
        self.m=m
        self.TILE_WIDTH=(constants.SCREEN_WIDTH)/n
        self.TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m

    def __getitem__(self, item):
        return self.walls[item]

    def addWall(self,mouse_x,mouse_y,check):
        constants.SCREEN_WIDTH
        constants.SCREEN_HEIGHT
        x=math.floor(mouse_x/self.TILE_WIDTH)
        y=math.floor((mouse_y)/self.TILE_HEIGHT)
        # print(mouse_x/self.TILE_WIDTH)
        # print(mouse_y/self.TILE_HEIGHT)
        # if mouse_x/self.TILE_HEIGHT > x+ self.TILE_HEIGHT*7/8:
        #     wall=Wall(x,y,"right",self.TILE_WIDTH,self.TILE_HEIGHT)

        if y<=self.m -1 and check:
            if mouse_x/self.TILE_WIDTH >= x+7/8 and mouse_x/self.TILE_WIDTH<=x+1:
                wall=Wall(x,y,"right",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x+1,y,"left",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
            elif mouse_x/self.TILE_WIDTH >= x and mouse_x/self.TILE_WIDTH<=x+1/8:
                wall=Wall(x,y,"left",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x-1,y,"right",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
            elif mouse_y/self.TILE_HEIGHT >= y+ 7/8 and mouse_y/self.TILE_HEIGHT<=y+1:
                wall=Wall(x,y,"down",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x,y+1,"up",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
            elif mouse_y/self.TILE_HEIGHT >= y and mouse_y/self.TILE_HEIGHT<=y+1/8:
                wall=Wall(x,y,"up",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x,y-1,"down",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
    def addWallXY(self,x,y,check,direction):
        if y<=self.m -1 and check:
            if direction=="right":
                wall=Wall(x,y,"right",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x+1,y,"left",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
            elif direction=="left":
                wall=Wall(x,y,"left",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x-1,y,"right",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
            elif direction=="down":
                wall=Wall(x,y,"down",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x,y+1,"up",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)
            elif direction=="up":
                wall=Wall(x,y,"up",self.TILE_WIDTH,self.TILE_HEIGHT)
                wall1=Wall(x,y-1,"down",self.TILE_WIDTH,self.TILE_HEIGHT)
                self.walls.append(wall)
                self.walls.append(wall1)

            # dirt = Wall(x,y,position,self.TILE_WIDTH,self.TILE_HEIGHT)
            # self.dirts[x][y]=dirt
            # print(x)
            # print(y)

