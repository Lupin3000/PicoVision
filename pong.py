from micropython import const
from picovision import PicoVision, PEN_RGB555
from urandom import randrange


SCREEN_WIDTH = const(320)
SCREEN_HEIGHT = const(240)
PADDLE_SPEED = const(5)
COLLISION_TOLERANCE = 5


class Field:
    def __init__(self, screen):
        self._display = screen

    def draw(self, fails: int = 0) -> None:
        self._display.set_pen(WHITE)
        self._display.text(f'Fails {fails}', 25, 15, scale=1)
        self._display.line(25, 25, SCREEN_WIDTH - 25, 25)
        self._display.line(25, 25, 25, SCREEN_HEIGHT - 25)
        self._display.line(SCREEN_WIDTH - 25, 25, SCREEN_WIDTH - 25, SCREEN_HEIGHT - 25)
        self._display.line(25, SCREEN_HEIGHT - 25, SCREEN_WIDTH - 25, SCREEN_HEIGHT - 25)


class Paddle:
    def __init__(self, screen):
        self._display = screen
        self.width = 5
        self.height = 20
        self.pos_x = 28
        self.pos_y = SCREEN_HEIGHT // 2

    def handle_input(self) -> None:
        button_up = self._display.is_button_a_pressed
        button_down = self._display.is_button_x_pressed

        if button_up() and self.pos_y > 30:
            self.pos_y -= PADDLE_SPEED

        if button_down() and self.pos_y < (SCREEN_HEIGHT - self.height - 30):
            self.pos_y += PADDLE_SPEED

        self._display.set_pen(RED)
        self._display.rectangle(self.pos_x, self.pos_y, self.width, self.height)


class Ball:
    def __init__(self, screen):
        self._display = screen
        self.radius = 5
        self.pos_x = SCREEN_WIDTH // 2
        self.pos_y = SCREEN_HEIGHT // 2
        self.speed_x = -1 if randrange(2) else 1
        self.speed_y = -1 if randrange(2) else 1

    def draw(self) -> None:
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        self._display.set_pen(BLUE)
        self._display.circle(self.pos_x, self.pos_y, self.radius)


def check_collision(circle: list, rectangle: list):
    circle_radius, circle_x, circle_y = circle
    rect_x, rect_y, rect_width, rect_height = rectangle

    closest_x = max(rect_x, min(circle_x, rect_x + rect_width))
    closest_y = max(rect_y, min(circle_y, rect_y + rect_height))

    distance = ((circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2) ** 0.5
    return distance <= (circle_radius + COLLISION_TOLERANCE)


display = PicoVision(PEN_RGB555, SCREEN_WIDTH, SCREEN_HEIGHT)
display.set_font("bitmap8")

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(0, 0, 255)

ball_lost = 0
field = Field(screen=display)
paddle = Paddle(screen=display)
ball = Ball(screen=display)

while True:
    display.set_pen(BLACK)
    display.clear()

    field.draw(fails=ball_lost)
    paddle.handle_input()

    if not (25 + ball.radius <= ball.pos_y <= SCREEN_HEIGHT - 25 - ball.radius):
        ball.speed_y *= -1

    if not (25 + ball.radius <= ball.pos_x <= SCREEN_WIDTH - 25 - ball.radius):
        ball.speed_x *= -1

    if ball.pos_x <= 35:
        if check_collision(circle=[ball.radius, ball.pos_x, ball.pos_y],
                           rectangle=[paddle.pos_x, paddle.pos_y, paddle.width, paddle.height]):
            ball.speed_x *= -1

    if ball.pos_x - ball.radius < 25:
        ball_lost += 1

    ball.draw()

    display.update()
