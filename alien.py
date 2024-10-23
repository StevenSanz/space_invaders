import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_config, pantalla):
        # inicializa el alien y establece su posicion original
        super(Alien, self).__init__()

        self.pantalla = pantalla
        self.ai_config = ai_config

        self.image = pygame.image.load("imagenes/aliens.png")
        self.image = pygame.transform.scale(self.image, (58, 45))  # Redimensiona a 58x45 píxeles
        self.rect = self.image.get_rect()

        # Inicializa cada nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Almacena la posición actual del alien
        self.x = float(self.rect.x)

    def blitme(self):
          # Dibuja el alien en su posicion actual
          self.pantalla.blit(self.image, self.rect)

    def check_edges(self):
        # Devuelve verdarero si el alien esta al borde de la pantalla 
        screen_rect = self.pantalla.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        # Mueve el alien a la derecha 
        self.x += (self.ai_config.alien_speed_factor *
                        self.ai_config.fleet_direction)
        self.rect.x = self.x 