import pygame
from pygame.sprite import Group
from configuracion import Config
from stats import Stats 
from button import Button
from score import Score
from nave import Nave
import funciones_juego as fj # Creación de pseudonimo

def run_game():
    # Inicializamos el juego, el objeto pantalla y las configuraciones. 
    pygame.init()
    ai_config = Config() 
    pantalla = pygame.display.set_mode((ai_config.screen_width, ai_config.screen_height), )
    pygame.display.set_caption("Stif's Invaders")

    # Crea el botón Play
    play_button = Button(ai_config, pantalla, "Play")

    # Crea una estancia para almacenar las stats del juego Y crea el marcador
    stats = Stats(ai_config)
    score = Score(ai_config, pantalla, stats)

    # Creamos la nave, un grupo de balas y un grupo de aliens
    nave = Nave(ai_config, pantalla)
    balas = Group()
    aliens = Group()

    # Crea la flota de aliens
    fj.crear_flota(ai_config, pantalla, aliens, nave)

    # Inicia el bucle principal del juego
    while True:
        
        fj.validacion_eventos(ai_config, pantalla, stats, score, play_button, nave, aliens, balas)
        if stats.game_active:
            nave.update()
            fj.update_balas(ai_config, pantalla, stats, score, nave, aliens, balas)
            fj.update_aliens(ai_config, stats, pantalla, score, nave, aliens, balas)
        
        fj.actualizar_pantalla(ai_config, pantalla, stats, score, nave, aliens, balas, play_button)
        
run_game()
