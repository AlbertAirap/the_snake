"""Импорт методов choice и randint из random."""
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


class GameObject:
    """
    Родительский ласс GameObject для всех объектов.

    Класс GameObject является базовым классом для всех игровых объектов
    в игре. Он предоставляет общие атрибуты и методы,
    которые могут быть использованы и переопределены дочерними классами.

    Атрибуты:
        position (tuple): Текущая позиция объекта на игровом поле,
            по умолчанию устанавливается в центр экрана.
        body_color (str): Цвет тела объекта, задаваемый при инициализации.

    Методы:
        __init__(position, body_color): Конструктор класса, который
            инициализирует позицию и цвет тела объекта.
        draw(): Пустой метод, который должен быть переопределен
            в дочерних классах для отрисовки конкретных объектов на экране.
    """

    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Метод инициализации любого объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод пустой.

        Он будет переопределяться в дочерних классах Apple и Snake.
        """
        pass


# Описание класса яблока.
class Apple(GameObject):
    """
    Класс Apple представляет собой яблоко для змейки.

    Атрибуты:
        body_color (str): Цвет тела яблока, задаваемый при инициализации.
        position (tuple): Позиция яблока на игровом поле, задается
            случайным образом при создании объекта.

    Методы:
        __init__(body_color): Конструктор класса, который инициализирует
            цвет яблока и случайную позицию на игровом поле.
        randomize_position(): Находит случайную пустую координату для
            отрисовки яблока, возвращает координаты в формате (X, Y).
        draw(): Отрисовывает яблоко на экране в текущей позиции с заданным
            цветом.
    """

    def __init__(self, body_color=APPLE_COLOR):
        """Метод инициализации змеи."""
        super().__init__(self.randomize_position(), body_color)

    def randomize_position(self):
        """
        Метод нахождения позиции яблока.

        Метод используется для нахождения
        случайой пустой координаты для отрисовки яблока.
        Возвращает: (X, Y).
        """
        apple_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        apple_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (apple_x, apple_y)

    def draw(self):
        """Метод используется для отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


# Описание класса змеи.
class Snake(GameObject):
    """
    Класс Snake представляет собой змейку.

    Атрибуты:
        length: Длина змеи, инициализируется значением 1.
        direction (tuple): Направление движения змеи, по умолчанию RIGHT.
        next_direction (tuple): Следующее направление движения,
            которое будет применено в следующем обновлении.
        positions (list): Список, содержащий карьежи с текущими координатами
            сегментов змеи, включая голову.
        last (tuple): Координаты последнего сегмента змеи для стирания
            его на экране.
    Методы:
        __init__(position, body_color): Конструктор класса, который
            инициализирует позицию и цвет тела змеи.
        update_direction(): Обновляет текущее направление змеи на
            следующее, если оно задано.
        move(): Перемещает змею в указанном направлении, обрабатывает
            телепортацию через границы экрана и проверяет столкновения
            с собственным телом.
        draw(): Отрисовывает змею на экране, включая голову и последний
            сегмент для стирания.
        get_head_position(): Возвращает текущие координаты головы змеи.
        reset(): Сбрасывает состояние игры, очищает экран и задает
            начальные параметры для змеи, включая случайное направление.
    """

    length = 1
    direction = RIGHT
    next_direction = None

    # Присваивание входных атрибутов класса.
    def __init__(self, position=(0, 0), body_color=SNAKE_COLOR):
        """Метод инициализации змеи."""
        super().__init__(position, body_color)
        self.positions = [(self.position)]
        self.last = None

    def update_direction(self):
        """Метод используется для записи нового направления вместо текущего."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Передвижение змеи.

        Метод используется для передвижения змеи,
        переписи её координат, телепортации и для проверки на столкновение.
        """
        old_head = self.get_head_position()

        # Телепортация через границу.
        new_head_x = old_head[0] + self.direction[0] * GRID_SIZE
        if new_head_x >= SCREEN_WIDTH:
            new_head_x = 0
        elif new_head_x < 0:
            new_head_x = SCREEN_WIDTH - GRID_SIZE

        new_head_y = old_head[1] + self.direction[1] * GRID_SIZE
        if new_head_y >= SCREEN_HEIGHT:
            new_head_y = 0
        elif new_head_y < 0:
            new_head_y = SCREEN_HEIGHT - GRID_SIZE

        # Проверка на столкновение и изменение координат.
        if (new_head_x, new_head_y) in self.positions:
            self.reset()
        else:
            self.positions.insert(0, (new_head_x, new_head_y))
            if len(self.positions) > self.length:
                self.last = self.positions[-1]
                self.positions.pop()

    def draw(self):
        """
        Рисование змеи.

        Метод используется для отрисовки змеи, головы
        и для затирание последнего сегмента.
        """
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

    # Метод возврата координат головы.
    def get_head_position(self):
        """
        Метод для возврата координаты головы змеи.

        Возвращает: (X, Y).
        """
        return self.positions[0]

    def reset(self):
        """
        Метод для перезапуска игры.

        Он очищает экран, сбрасывает length и выбирает случайный direction
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """
    Функция для определения и записи направления движения змеи.

    Принимает параметр game_object и меняет его атрибут
    """
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
    """
    Главная функция с бескоекчным циклом.

    Функция для создания объектов классов Snake и Apple и вечный цикл
    работы программы, где вызываются методы классов update_direction(),
    move(), randomize_position(), apple.draw() и display.update()
    """
    pygame.init()
    s_spawn_point = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)
    snake = Snake(s_spawn_point, SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.position = apple.randomize_position()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
