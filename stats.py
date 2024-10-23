class Stats():
    # Seguimiento de las estadisticas del juego
    def __init__(self, ai_config):
        # Inicializa las estadisticas
        self.ai_config = ai_config
        self.reset_stats()

        # Inicia space_invaders en un estado activo
        self.game_active = False

        # Puntuacion mas alta
        self.high_score = 0

    
    def reset_stats(self):
        # Inicializa estadisticas que pueden variar durante el juego
        self.ships_left = self.ai_config.ships_left
        self.points = 0
        self.level = 1
     