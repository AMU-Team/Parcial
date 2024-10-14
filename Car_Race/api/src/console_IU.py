import os
import random
import time

# Dimensiones de la pista
WIDTH = 7  # Número de columnas de la pista
HEIGHT = 10  # Número de filas de la pista

# Caracteres de la pista
PLAYER = 'A'  # Representa el coche del jugador
OBSTACLE = 'X'  # Representa los obstáculos en la pista
EMPTY = ' '  # Representa los espacios vacíos

# Velocidad inicial del coche
INITIAL_SPEED = 0.5

class RaceGame:
    def __init__(self):
        self.track = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.player_pos = WIDTH // 2  # Posición inicial del jugador
        self.track[-1][self.player_pos] = PLAYER  # Coloca el jugador en la pista desde el inicio
        self.speed = INITIAL_SPEED
        self.lap = 1
        self.max_laps = 3
        self.is_running = True
        self.last_obstacle_col = -1  # Para evitar que los obstáculos se generen en la misma columna consecutivamente

    # Método para mostrar la pista en la consola
    def display_track(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Lap: {self.lap}/{self.max_laps}")
        print(f"Speed: {int(1000 * self.speed)} km/h")
        print("-" * (WIDTH + 2))
        for row in self.track:
            print(f"|{''.join(row)}|")
        print("-" * (WIDTH + 2))

    # Método para mover el coche del jugador
    def move_player(self, direction):
        # Borra la posición actual del coche antes de moverlo
        self.track[-1][self.player_pos] = EMPTY
        
        # Mueve el coche a la izquierda si es posible
        if direction == 'L':
            if self.player_pos > 0:
                self.player_pos -= 1
            else:
                self.is_running = False
                print("¡Has chocado contra la pared! Game Over.")
                return
        # Mueve el coche a la derecha si es posible
        elif direction == 'R':
            if self.player_pos < WIDTH - 1:
                self.player_pos += 1
            else:
                self.is_running = False
                print("¡Has chocado contra la pared! Game Over.")
                return

    # Método modificado para generar un solo obstáculo por fila y evitar que se generen consecutivamente en la misma columna
    def generate_obstacles(self):
        # Genera una fila vacía
        new_row = [EMPTY for _ in range(WIDTH)]
        # Elige una columna aleatoria para colocar el obstáculo, diferente a la última columna de obstáculo
        obstacle_col = random.choice([i for i in range(WIDTH) if i != self.last_obstacle_col])
        new_row[obstacle_col] = OBSTACLE
        self.last_obstacle_col = obstacle_col
        self.track.insert(0, new_row)
        self.track.pop()

    # Método para verificar si el coche del jugador ha chocado con un obstáculo
    def check_collision(self):
        if self.track[-1][self.player_pos] == OBSTACLE:
            self.is_running = False
            print("¡Has chocado con un obstáculo! Game Over.")

    # Método principal que ejecuta el juego
    def run_game(self):
        while self.is_running:
            self.display_track()

            # Input del jugador
            direction = input("Mover (L=Izquierda, R=Derecha): ").upper()

            # Si la entrada es válida, el coche se mueve y la pista avanza
            if direction in ['L', 'R']:
                self.move_player(direction)
                self.generate_obstacles()  # Solo generamos nuevos obstáculos si la entrada es válida
                self.check_collision()
            else:
                print("Entrada inválida. Use L o R para moverse.")
                time.sleep(1)  # Pausa breve para dar tiempo a leer el mensaje de entrada inválida
            
            # Asegura que el coche siempre se dibuje después de que se actualice la pista
            self.track[-1][self.player_pos] = PLAYER  

            time.sleep(self.speed)

        print("Gracias por jugar.")

if __name__ == "__main__":
    game = RaceGame()
    game.run_game()
