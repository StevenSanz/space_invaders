import pygame
from pygame.sprite import Sprite

class Nave(Sprite):
    def __init__ (self, ai_config, pantalla):
        super(Nave, self).__init__()
        self.pantalla = pantalla
        self.ai_config = ai_config
        
        self.image = pygame.image.load("rocket-launch-clouds.png")
        self.image = pygame.transform.scale(self.image, (100, 85))  # Redimensiona a 100x85 píxeles
        self.rect = self.image.get_rect()
        self.pantalla_rect = pantalla.get_rect()
        
        self.rect.centerx = self.pantalla_rect.centerx
        self.rect.bottom = self.pantalla_rect.bottom

        # Almacenar un valor decimal para el centro de la nave
        self.center = float(self.rect.centerx)
        
        #Banderas de movimiento
        self.moving_right = False
        self.moving_left = False
    def update(self):
        # Actualiza la posicion de la nave segun las banderas de movimiento
        if self.moving_right and self.rect.right < self.pantalla_rect.right:
            self.center += self.ai_config.velocidad_nave
            
        if self.moving_left and self.rect.left > self.pantalla_rect.left:
            self.center -= self.ai_config.velocidad_nave
        self.rect.centerx = self.center

    def blitme(self):
        self.pantalla.blit(self.image, self.rect)

    def center_ship(self):
        # Centra la nave en la pantalla 
        self.center = self.pantalla_rect.centerx