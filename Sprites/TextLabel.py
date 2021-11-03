import pygame
class TextLabel:
    def __init__(self,text,x,y,font_background=(0,0,0),font_color=(0,0,0),font=pygame.font.SysFont(None, 30)):
        #create text label
        self.font=font
        self.x=x
        self.y=y
        self.font_color = font_color
        self.font_background = font_background
        self.t = font.render(text, True, font_color, font_background)
        self.t_rect = self.t.get_rect()
        self.t_rect.centerx, self.t_rect.centery = x, y
    def draw(self,screen):
        #draw text to screen
        screen.blit(self.t, self.t_rect)
    def setText(self,text):
        self.t = self.font.render(text, True, self.font_color, self.font_background)
        self.t_rect = self.t.get_rect()
        self.t_rect.centerx, self.t_rect.centery = self.x, self.y