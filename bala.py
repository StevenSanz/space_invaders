import pygame
from pygame.sprite import Sprite

class Bala(Sprite):

    def __init__(self, ai_config, pantalla, nave):
        # Inicialización de Sprite
        super().__init__()
        self.pantalla = pantalla

        # Crear un rectángulo para la bala y establecer la posición correcta
        self.rect = pygame.Rect(0, 0, ai_config.bala_width, ai_config.bala_height)
        self.rect.centerx = nave.rect.centerx + 3 
        self.rect.top = nave.rect.top

        # Almacenar la posición de la bala como un valor decimal
        self.y = float(self.rect.y)
        self.color = ai_config.bala_color
        self.velocidad = ai_config.velocidad_bala

    def update(self):
        # Movimiento ascendente de la bala
        self.y -= self.velocidad
        self.rect.y = self.y

    def draw_bala(self):
        # Dibujar la bala en la pantalla
        pygame.draw.rect(self.pantalla, self.color, self.rect)


