import pygame

''' component 1 : resuable Rect that stores its coordinates in the lable  attribute
    extending from the class pygame.Rect
'''
class LabeledRect(pygame.Rect):
    
    def __init__(self, position, size, label):
        super().__init__(position, size)
        self.rect = pygame.Rect(position, size)
        self.label = label
    def write(self,surface,font,fontsize,color):
        font = pygame.font.Font(None, fontsize)
        text_surface =font.render(self.label,True,color)
        text_rect=text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface,text_rect)
        