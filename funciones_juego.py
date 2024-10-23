import sys

from time import sleep

import pygame

from bala import Bala

from alien import Alien
 
def  validacion_eventos_keydown(event, ai_config, pantalla, nave, balas):
    if event.key == pygame.K_RIGHT:
            nave.moving_right = True
    elif event.key == pygame.K_LEFT:
            nave.moving_left = True
    elif event.key == pygame.K_SPACE:
            # Crea una nueva bala y la agrega el grupo de balas
            disparo_bala(ai_config, pantalla, nave, balas)
    elif event.key == pygame.K_q: 
         sys.exit()
            
def validacion_eventos_keyup(event, nave):
    if event.key == pygame.K_RIGHT:
        nave.moving_right = False
    elif event.key == pygame.K_LEFT:
        nave.moving_left = False  


def validacion_eventos(ai_config, pantalla, stats, score, play_button, nave, aliens, balas):
    # Responde a pulsaciones del teclado y eventos del ratón
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            validacion_eventos_keydown(event, ai_config, pantalla, nave, balas)
        elif event.type == pygame.KEYUP:
            validacion_eventos_keyup(event, nave)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_config, pantalla, stats, score, play_button, nave, aliens, balas, mouse_x, mouse_y)

def check_play_button(ai_config, pantalla, stats, score, play_button, nave, aliens, balas, mouse_x, mouse_y):
    # Comienza un nuevo juego cuando el jugador hace click en play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Restablece la configuración del juego
        ai_config.dinamic_config_init()
        # Oculta el mouse
        pygame.mouse.set_visible(False)
        # Restablece las estadisticas del juego
        stats.reset_stats()
        stats.game_active = True

        # Restablece las imagenes de marcador
        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ships()

        # Vacia la lista de aliens y balas
        aliens.empty()
        balas.empty()

        # Crea una nueva flota y centra la nave
        crear_flota(ai_config, pantalla, aliens, nave)
        nave.center_ship()


def actualizar_pantalla (ai_config, pantalla, stats, score, nave, aliens, balas, play_button):
    
    # Carga fondo y nave
    pantalla.fill(ai_config.bg_color)
    # Vuelve a dibujar todas las balas detras de la nave y de los invaders
    for bala in balas.sprites():
        bala.draw_bala()
    nave.blitme()
    aliens.draw(pantalla)

    # Dibuja la información de la puntuación
    score.show_score()

    # Dibuja el botón de play si el juego esta inactivo
    if not stats.game_active:
        play_button.draw_button()


    pygame.display.flip()   

def update_balas (ai_config, pantalla, stats, score, nave, aliens, balas):
     # Actualiza la posicion de las balas 
    balas.update()
    # Elimina las balas desaparecidas
    for bala in balas.copy():
        if bala.rect.bottom <= 0:
            balas.remove(bala)

    # Comprueba si hay balas que hayan alcanzado a los aliens 
    # Si son alcanzados, desaparecen la bala y el alien
    check_bala_alien_collisions(ai_config, pantalla, stats, score, nave, aliens, balas)

def check_bala_alien_collisions(ai_config, pantalla, stats, score, nave, aliens, balas):
    # Responde a las colisiones entre balas y aliens
    # Elimina las balas y los aliens que hayan chocado
    colisions = pygame.sprite.groupcollide(balas, aliens, True, True)

    if colisions:
        for aliens in colisions.values():
            stats.points += ai_config.alien_points * len(aliens)
            score.prep_score()
        check_high_score(stats, score)

    if len(aliens) == 0:
        # Si se destruye toda la flota comienza un nuevo nivel
        balas.empty()
        ai_config.increase_speed()

        # Incrementa el nivel
        stats.level += 1
        score.prep_level()

        crear_flota(ai_config, pantalla, aliens, nave)

def check_high_score(stats, score):
    # Verifica si se ha alcanzado la puntuación mas alta
    if stats.points > stats.high_score:
        stats.high_score = stats.points
        score.prep_high_score()


def disparo_bala(ai_config, pantalla, nave, balas):
    # Dispara una bala si aun el limite no se ha sobrepasado
    if len(balas) < ai_config.balas_allowed:
        nueva_bala = Bala(ai_config, pantalla, nave)
        balas.add(nueva_bala)

def get_number_aliens_x(ai_config, alien_width):
    # Determina el numero de aliens que caben en una fila
    avaliable_space_x = ai_config.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_config, nave_height, alien_height):
    # Determina el numero de filas de aliens que se ajusta a la pantalla
    avaliable_space_y = (ai_config.screen_height - 
                         (3 * alien_height) - nave_height) 
    number_rows = int(avaliable_space_y / (2 * alien_height))
    return number_rows
    

def create_alien(ai_config, pantalla, aliens, alien_number, row_number):
    # Crea un alien y lo coloca en la fila 
    alien = Alien(ai_config, pantalla)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def crear_flota(ai_config, pantalla, aliens, nave):
    # Crea una flota de aliens
    # Crea un alien y encuentra el numero de aliens seguidos
    # El espacio entre cada alien es igual a un ancho del alien 

    alien = Alien(ai_config, pantalla)
    number_aliens_x = get_number_aliens_x(ai_config, alien.rect.width)
    number_rows = get_number_rows(ai_config, nave.rect.height, alien.rect.height)


    # Crea la primera flota de aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_config, pantalla, aliens, alien_number, row_number)

def check_fleet_edges(ai_config, aliens):
    # Detecta si algun alien ha llegado a uno de los bordes de la pantalla 
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_config, aliens)
            break
    
# Cambia la dirección y baja los aliens cuando toquen el borde
def change_fleet_direction(ai_config, aliens):
    # Desciende la flota
    for alien in aliens.sprites():
        alien.rect.y += ai_config.fleet_drop_speed
    # Cambia la dirección multiplicando por -1
    ai_config.fleet_direction *= -1

def on_ship_hit(ai_config, stats, pantalla, score, nave, aliens, balas):
    # Responde al impacto de un alien con la nave

    if stats.ships_left > 0:
        # Disminuye las naves restantes 
        stats.ships_left -= 1

        # Actualiza el marcador de naves restantes
        score.prep_ships()

        # Vacia la lista de aliens y balas
        aliens.empty()
        balas.empty()

        # Crea una nueva flota y centra la nave
        crear_flota(ai_config, pantalla, aliens, nave)
        nave.center_ship()

        # Pausa de 0.5 segundos
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True) # Vuelve visible el mouse


def check_aliens_bottom(ai_config, stats, pantalla, score, nave, aliens, balas):
    # Comprueba si algun alien ha llegado al final de la pantalla 
    pantalla_rect = pantalla.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= pantalla_rect.bottom:
            # Responde igual que si la nave fuera golpeada 
            on_ship_hit(ai_config, stats, pantalla, score, nave, aliens, balas)
            break

def update_aliens(ai_config, stats, pantalla, score, nave, aliens, balas):
    # Comprueba si la flota esta al borde y luego actualiza las posiciones de todos los aliens de la flota
    check_fleet_edges(ai_config, aliens)
    aliens.update()
    
    # Busca colisiones entre la nave y los aliens
    if pygame.sprite.spritecollideany(nave, aliens):
        on_ship_hit(ai_config, stats, pantalla, score, nave, aliens, balas)

    # Busca aliens que golpean la parte inferior de la pantalla 
    check_aliens_bottom(ai_config, stats, pantalla, score, nave, aliens, balas)
