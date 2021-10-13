import pygame
from VacuumCleaner import VacuumCleaner
import constants
from Tiles import Tiles
class Game:
    def __init__(self,n,m):
        self.init_pygame()
        self.Tiles=Tiles(n,m)
        self.VacuumCleaner= VacuumCleaner(self.Tiles.TILE_WIDTH,self.Tiles.TILE_HEIGHT)
        self.all_sprites = pygame.sprite.Group()
        self.keep_looping=True
    
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
        self.all_sprites.add(self.VacuumCleaner)
    def draw(self):
        self.screen.fill(self.BG_COLOR)
        self.update_classes()
        # ----
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        # ----
        pygame.display.flip()
    def handle_events(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.keep_looping = False
                return True
            

    def main(self):
        self.clock.tick(constants.FRAME_RATE)
        while self.keep_looping:
            self.handle_events()
            self.draw()
