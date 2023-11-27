from picovision import PicoVision, PEN_RGB555
from urandom import randrange


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
PADDLE_SPEED = 5


class Paddle:
    def __init__(self):
        self.width = 5
        self.height = 20
        self.pos_x = 1
        self.pos_y = SCREEN_HEIGHT // 2

    def handle_input(self, interface) -> None:
        button_up = display.is_button_a_pressed
        button_down = display.is_button_x_pressed

        if button_up() and self.pos_y > 0:
            self.pos_y -= PADDLE_SPEED

        if button_down() and self.pos_y < (SCREEN_HEIGHT - self.height):
            self.pos_y += PADDLE_SPEED

        interface.rectangle(self.pos_x, self.pos_y, self.width, self.height)


class Ball:
    def __init__(self):
        self.radius = 5

        self.pos_x = SCREEN_WIDTH // 2
        self.pos_y = SCREEN_HEIGHT // 2

        self.speed_x = -1 if randrange(2) else 1
        self.speed_y = -1 if randrange(2) else 1

    def draw(self, interface) -> None:
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        interface.circle(self.pos_x, self.pos_y, self.radius)


display = PicoVision(PEN_RGB555, SCREEN_WIDTH, SCREEN_HEIGHT)
display.set_font("bitmap8")

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)

ball = Ball()
paddle = Paddle()

left_limit = top_limit = ball.radius
right_limit = SCREEN_WIDTH - ball.radius
bottom_limit = SCREEN_HEIGHT - ball.radius

while True:
    display.set_pen(BLACK)
    display.rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    if not (left_limit <= ball.pos_x <= right_limit):
        ball.speed_x *= -1

    if not (top_limit <= ball.pos_y <= bottom_limit):
        ball.speed_y *= -1

    display.set_pen(WHITE)
    ball.draw(display)

    paddle.handle_input(display)

    display.update()
