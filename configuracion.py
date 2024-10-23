class Config ():
    # Almacenar las configuraciones del juego.
    def __init__ (self):
        self.screen_width = 990
        self.screen_height = 690
        self.bg_color = (135, 206, 250)

        # Nave Config
        
        self.ships_left = 3
        # Configuracion balas
        
        self.bala_width = 3
        self.bala_height = 15
        self.bala_color = 60, 60, 60
        self.balas_allowed = 3
        
        # Configuracion aliens
        
        self.fleet_drop_speed = 10

        # Velocidad aceleración del juego
        self.aceleration = 1.1

        # Factor aumento puntuación
        self.score_streak = 1.5

        self.dinamic_config_init()
        
    def dinamic_config_init(self):
        # Inicializa la configuracion dinamica del juego
        self.velocidad_nave = 1.5
        self.velocidad_bala = 1 
        self.alien_speed_factor = 1

        # fleet_direction, cuando es 1 representa a la derecha y cuando es -1 a la izquierda
        self.fleet_direction = 1 

        # Puntuación
        self.alien_points = 50

    def increase_speed(self):
        # Aumenta la configuracuión de velocidad y los valores de puntos por alien
        self.velocidad_nave *= self.aceleration
        self.velocidad_bala *= self.aceleration
        self.alien_speed_factor *= self.aceleration
        self.alien_points = int(self.alien_points * self.score_streak)
        