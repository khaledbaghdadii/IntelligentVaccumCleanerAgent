import pygame
import constants
import math
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y,TILE_WIDTH,TILE_HEIGT):
        super().__init__()
        self.x = x
        self.y = y
        self.TILE_WIDTH= TILE_WIDTH
        self.TILE_HEIGHT= TILE_HEIGT
        self.has_walls_left=False
        self.has_walls_right=False
        self.has_walls_up=False
        self.has_walls_down=False
        self.has_walls=False
        self.isDirty=False
        self.isVisited = False #notion of memory
        self.possibleVisible=True
        self.filepath = "images/tile.png"
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (round(TILE_WIDTH), round(TILE_HEIGT)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * TILE_WIDTH, y * TILE_HEIGT)
    
    def setIsDirty(self,isDirty):
        self.isDirty=isDirty

    def hasWalls(self):
        return self.has_walls_left or self.has_walls_right or self.has_walls_down or self.has_walls_up
    def hasWallLeft(self):
        return self.has_walls_left
    def hasWallRight(self):
        return self.has_walls_right
    def hasWallUp(self):
        return self.has_walls_up
    def hasWallDown(self):
        return self.has_walls_down
    def clearWalls(self):
        self.has_walls_down=False
        self.has_walls_left=False
        self.has_walls_right=False
        self.has_walls_up=False
        self.has_walls=False
    
    



class Tiles:
    def __init__(self,n,m):
        self.n=n
        self.m=m
        self.TILE_WIDTH=(constants.SCREEN_WIDTH)/n
        self.TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m
        self.tiles=[[0 for x in range(m)] for y in range(n)]
        for i in range(n):
            for j in range(m):
                # TILE_WIDTH=(constants.SCREEN_WIDTH)/n
                # TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m
                tile = Tile(i,j,self.TILE_WIDTH,self.TILE_HEIGHT)
                #leftest border
                if(i==0):
                    tile.has_walls_left=True
                    if(j==0):
                        tile.has_walls_up=True
                    elif (j==m-1):
                        tile.has_walls_down=True
                #upper border
                if(j==0):
                    tile.has_walls_up=True
                    if (i==n-1):
                        tile.has_walls_right=True
                #right border
                if(i==n-1):
                    tile.has_walls_right=True
                    if (j==m-1):
                        tile.has_walls_down=True
                #bottom border
                if(j==m-1):
                    tile.has_walls_down=True
                self.tiles[i][j]=tile

    def __getitem__(self, item):
        return self.tiles[item]
    def getTiles(self):
        return self.tiles
    
    def addDirt(self,mouse_x,mouse_y,check):
        constants.SCREEN_WIDTH
        constants.SCREEN_HEIGHT
        x=math.floor(mouse_x/self.TILE_WIDTH)
        y=math.floor((mouse_y)/self.TILE_HEIGHT)
        if y<=self.m-1 and x<=self.n-1 and check:
            self.tiles[x][y].setIsDirty(True)
    def addDirtXY(self,x,y,check):
        if y<=self.m-1 and x<=self.n-1 and check:
            self.tiles[x][y].setIsDirty(True)
    def removeDirtXY(self,x,y):
        self.tiles[x][y].setIsDirty(False)
    def addWall(self,mouse_x,mouse_y,check):
        constants.SCREEN_WIDTH
        constants.SCREEN_HEIGHT
        x=math.floor(mouse_x/self.TILE_WIDTH)
        y=math.floor((mouse_y)/self.TILE_HEIGHT)

        if y<=self.m -1 and x<=self.n-1 and check:
            if mouse_x/self.TILE_WIDTH >= x+7/8 and mouse_x/self.TILE_WIDTH<=x+1 and x+1<len(self.tiles):
                self.tiles[x][y].has_walls_right=True
                self.tiles[x+1][y].has_walls_left=True
            elif mouse_x/self.TILE_WIDTH >= x and mouse_x/self.TILE_WIDTH<=x+1/8:
                self.tiles[x][y].has_walls_left=True
                self.tiles[x-1][y].has_walls_right=True
            elif mouse_y/self.TILE_HEIGHT >= y+ 7/8 and mouse_y/self.TILE_HEIGHT<=y+1 and y+1<len(self.tiles[x]):
                self.tiles[x][y].has_walls_down=True
                self.tiles[x][y+1].has_walls_up=True
            elif mouse_y/self.TILE_HEIGHT >= y and mouse_y/self.TILE_HEIGHT<=y+1/8:
                self.tiles[x][y].has_walls_up=True
                self.tiles[x][y-1].has_walls_down=True
        pass
    def addWallXY(self,x,y,check,direction):
        if y<=self.m-1 and check:
            if direction=="right" and x+1<len(self.tiles):
                self.tiles[x][y].has_walls_right=True
                self.tiles[x+1][y].has_walls_left=True
            elif direction=="left":
                self.tiles[x][y].has_walls_left=True
                self.tiles[x-1][y].has_walls_right=True
            elif direction=="down" and y+1<len(self.tiles[x]):
                self.tiles[x][y].has_walls_down=True
                self.tiles[x][y+1].has_walls_up=True
            elif direction=="up":
                self.tiles[x][y].has_walls_up=True
                self.tiles[x][y-1].has_walls_down=True
        pass
    def clearWalls(self):
        n=len(self.tiles)
        m=len(self.tiles[0])
        for i,tiles in enumerate(self.tiles):
            for j,tile in enumerate(tiles):
                tile.clearWalls()
                #leftest border
                if(tile.x==0):
                    tile.has_walls_left=True
                    if(tile.y==0):
                        tile.has_walls_up=True
                    elif (tile.y==m-1):
                        tile.has_walls_down=True
                #upper border
                if(tile.y==0):
                    tile.has_walls_up=True
                    if (tile.x==n-1):
                        tile.has_walls_right=True
                #right border
                if(tile.x==n-1):
                    tile.has_walls_right=True
                    if (tile.y==m-1):
                        tile.has_walls_down=True
                #bottom border
                if(tile.y==m-1):
                    tile.has_walls_down=True

    def clearDirts(self):
        for tiles in self.tiles:
            for tile in tiles:
                tile.isDirty=False
    

