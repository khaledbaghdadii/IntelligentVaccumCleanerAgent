import pygame
import constants

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y,TILE_WIDTH,TILE_HEIGT):
        super().__init__()
        self.x = x
        self.y = y
        self.TILE_WIDTH= TILE_WIDTH
        self.TILE_HEIGHT= TILE_HEIGT
        self.hasWallLeft=False
        self.hasWallRight=False
        self.hasWallUp=False
        self.hasWallsDown=False
        self.isDirty=False
        self.filepath = "images/tile.png"
        try:
            self.image = pygame.image.load(self.filepath).convert_alpha()
        except:
            s = "Couldn't open: {}".format(self.filepath)
            raise ValueError(s)
        self.image = pygame.transform.scale(self.image, (round(TILE_WIDTH), round(TILE_HEIGT)))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x * TILE_WIDTH, y * TILE_HEIGT)


class Tiles:
    def __init__(self,n,m):
        self.TILE_WIDTH=(constants.SCREEN_WIDTH)/n
        self.TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m
        self.tiles=[[0 for x in range(m)] for y in range(n)]
        for i in range(n):
            for j in range(m):
                # TILE_WIDTH=(constants.SCREEN_WIDTH)/n
                # TILE_HEIGHT=(constants.SCREEN_HEIGHT-200)/m
                tile = Tile(i,j,self.TILE_WIDTH,self.TILE_HEIGHT)
                self.tiles[i][j]=tile

    def __getitem__(self, item):
        return self.tiles[item]


