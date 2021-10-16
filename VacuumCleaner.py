import pygame

class VacuumCleaner(pygame.sprite.Sprite):
    def __init__(self,TILE_WIDTH,TILE_HEIGHT):
        super().__init__()
        self.x=0
        self.y=0
        self.TILE_WIDTH= TILE_WIDTH
        self.TILE_HEIGHT= TILE_HEIGHT
        self.filepath = "images/vacuum.png"
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
    
