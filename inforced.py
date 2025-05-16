import pygame
import random
import sys

# Inicializar o pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monster Farm Adventure")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonte
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 72)

# Classe para o Jogador
class Player:
    def __init__(self, name):
        self.name = name
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.width = 30
        self.height = 30
        self.direction = "down"  # Direção inicial

    def move(self, keys):
        if keys[pygame.K_UP]:
            self.y -= self.speed
            self.direction = "up"
        if keys[pygame.K_DOWN]:
            self.y += self.speed
            self.direction = "down"
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = "right"

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Classe para Criaturas
class Creature:
    def __init__(self, name, type, friendliness):
        self.name = name
        self.type = type
        self.friendliness = friendliness
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 50)
        self.width = 20
        self.height = 20
        self.speed = random.randint(1, 3)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        if self.x <= 0:
            self.x = 0
            self.direction = "right"
        elif self.x + self.width >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.direction = "left"
        if self.y <= 0:
            self.y = 0
            self.direction = "down"
        elif self.y + self.height >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
            self.direction = "up"

    def draw(self, screen):
        color = (0, 255, 0) if self.friendliness > 5 else (255, 0, 0)
        pygame.draw.circle(screen, color, (self.x, self.y), 20)
        text = font.render(self.name, True, BLACK)
        screen.blit(text, (self.x - 20, self.y - 40))

# Classe para Bolas
class Ball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.speed = 10
        self.direction = direction
        self.radius = 5

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.radius)

    def is_off_screen(self):
        return self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT

# Função para explorar o mundo
def explore_world():
    creatures = [
        Creature("Draco", "Dragon", random.randint(1, 10)),
        Creature("Luna", "Wolf", random.randint(1, 10)),
        Creature("Fang", "Monster", random.randint(1, 10)),
        Creature("Blaze", "Phoenix", random.randint(1, 10)),
    ]
    return creatures

# Função para exibir o menu inicial
def show_menu():
    while True:
        screen.fill(WHITE)
        title = menu_font.render("Monster Farm Adventure", True, BLACK)
        start_button = font.render("Start", True, BLACK)
        quit_button = font.render("Quit", True, BLACK)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        screen.blit(start_button, (SCREEN_WIDTH // 2 - start_button.get_width() // 2, 250))
        screen.blit(quit_button, (SCREEN_WIDTH // 2 - quit_button.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if SCREEN_WIDTH // 2 - start_button.get_width() // 2 <= mouse_x <= SCREEN_WIDTH // 2 + start_button.get_width() // 2:
                    if 250 <= mouse_y <= 250 + start_button.get_height():
                        return "start"
                elif SCREEN_WIDTH // 2 - quit_button.get_width() // 2 <= mouse_x <= SCREEN_WIDTH // 2 + quit_button.get_width() // 2:
                    if 350 <= mouse_y <= 350 + quit_button.get_height():
                        return "quit"

# Função para exibir a tela de Game Over
def show_game_over():
    while True:
        screen.fill(BLACK)
        game_over_text = menu_font.render("GAME OVER", True, WHITE)
        restart_text = font.render("Pressione R para reiniciar ou Q para sair", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Função principal
def main():
    clock = pygame.time.Clock()
    player_name = "Player"
    player = Player(player_name)
    creatures = explore_world()
    balls = []

    menu_choice = show_menu()
    if menu_choice == "quit":
        pygame.quit()
        sys.exit()

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    balls.append(Ball(player.x + player.width // 2, player.y + player.height // 2, player.direction))

        keys = pygame.key.get_pressed()
        player.move(keys)

        for creature in creatures:
            creature.move()

        for ball in balls:
            ball.move()

        for ball in balls[:]:
            for creature in creatures[:]:
                if abs(ball.x - creature.x) < 20 and abs(ball.y - creature.y) < 20:
                    creatures.remove(creature)
                    balls.remove(ball)
                    break
            if ball.is_off_screen():
                balls.remove(ball)

        for creature in creatures:
            if abs(player.x - creature.x) < 20 and abs(player.y - creature.y) < 20:
                result = show_game_over()
                if result == "restart":
                    main()
                running = False

        player.draw(screen)
        for creature in creatures:
            creature.draw(screen)
        for ball in balls:
            ball.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
