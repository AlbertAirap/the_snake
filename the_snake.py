from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self, body_color):
        super().__init__(self.randomize_position(), body_color)
        self.body_color = body_color

    def randomize_position(self):
        apple_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        apple_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (apple_x, apple_y)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    length = 1
    direction = RIGHT
    next_direction = None

    def __init__(self, position, body_color):
        super().__init__(position, body_color)
        self.positions = [(self.position)]
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        old_head = self.get_head_position()

        new_head_X = old_head[0] + self.direction[0] * GRID_SIZE
        if new_head_X >= SCREEN_WIDTH:
            new_head_X = 0
        elif new_head_X < 0:
            new_head_X = SCREEN_WIDTH - GRID_SIZE

        new_head_Y = old_head[1] + self.direction[1] * GRID_SIZE
        if new_head_Y >= SCREEN_HEIGHT:
            new_head_Y = 0
        elif new_head_Y < 0:
            new_head_Y = SCREEN_HEIGHT - GRID_SIZE

        if (new_head_X, new_head_Y) in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (new_head_X, new_head_Y))
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop()

    def draw(self):
        print(self.positions)
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Создание экземпляров классов.
    s_spawn_point = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
    snake = Snake(s_spawn_point, SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
