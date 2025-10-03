import pygame
import sys

SCREEN_DIM = (1200,600)
ground_y = SCREEN_DIM[1]*0.78
GRAVITY = 0.5
screen = pygame.display.set_mode(SCREEN_DIM,pygame.RESIZABLE)

class Button():
    def __init__(self,pos,image,text,font_style,font_size,font_color):
        self.image = image
        self.pos = pos
        text_font = pygame.font.SysFont(font_style,font_size)
        self.rect = self.image.get_rect(center=self.pos)
        self.text_content = text
        self.text = text_font.render(self.text_content,True,font_color)
        self.text_rect = self.text.get_rect(center=(self.pos[0],self.pos[1]+40))
    
    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image,self.rect)
        if self.text is not None:
            screen.blit(self.text,self.text_rect)
    
    def clicked(self,position):
        if position[0] in range(self.rect.left,self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            clicked = True
            return clicked