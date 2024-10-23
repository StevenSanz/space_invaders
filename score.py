import pygame.font
from pygame.sprite import Group

from nave import Nave

class Score():
    # Almacena la puntuacion y la muestra al jugador
    def __init__(self, ai_config, pantalla, stats): 
        # Inicializa los atributos del puntaje
        self.pantalla = pantalla
        self.pantalla_rect = pantalla.get_rect()
        self.ai_config = ai_config
        self.stats = stats

        # Ajustes de fuente para la puntuación
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepara la imagen inicial
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        # Convierte el marcador en una imagen renderizada
        rounded_score = int(round(self.stats.points, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_config.bg_color)

        # Muestra el puntaje en la esquina superior derecha de la pantalla 
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.pantalla_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        # Convierte la puntuación mas alta en una imagen renderizada
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_config.bg_color)

        # Muestra el puntaje mas alto en la parte superior de la pantalla
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.pantalla_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        # Convierte el nivel en una imagen renderizada
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_config.bg_color)

        # Posiciona el nivel debajo del puntaje
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.pantalla_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        # Muesta las naves restantes del jugador
        self.naves = Group()
        for numero_nave in range(self.stats.ships_left):
            nave = Nave(self.ai_config, self.pantalla)
            nave.rect.x = 10 + numero_nave * nave.rect.width
            nave.rect.y = 10
            self.naves.add(nave)

    def show_score(self):
        # Dibuja la puntuación en la pantalla 
        self.pantalla.blit(self.score_image, self.score_rect)
        self.pantalla.blit(self.high_score_image, self.high_score_rect)
        self.pantalla.blit(self.level_image, self.level_rect)

        # Dibuja las naves 
        self.naves.draw(self.pantalla)