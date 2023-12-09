from micropython import const
from picovision import PicoVision, PEN_RGB555
from pimoroni import Button


SCREEN_WIDTH = const(320)
SCREEN_HEIGHT = const(240)


class Interface:
    def __init__(self, screen, icon: list):
        """
        interface constructor
        :param screen: display
        :param icon: gun icon as list
        """
        self._display = screen
        self.score = 0
        self.lives = 3
        self._icon = list(icon)

    def draw(self) -> None:
        """
        draw interface with score and lives on display
        :return: None
        """
        self._display.set_pen(WHITE)

        self._display.text(f'Score {self.score}', 5, 5, scale=1)
        self._display.text('Lives', 230, 5, scale=1)

        self._display.set_pen(YELLOW)

        score_icon_pos_x = 260
        score_icon_pos_y = 6
        for _ in range(self.lives):
            for y, row in enumerate(self._icon):
                for x, c in enumerate(row):
                    if c == 1:
                        self._display.pixel(x + score_icon_pos_x, y + score_icon_pos_y)
            score_icon_pos_x += 15


class Enemy:

    ENEMY_SPEED = const(2)

    def __init__(self, screen, x: int, y: int):
        """
        enemy constructor
        :param screen: display
        :param x: x position
        :param y: y position
        """
        self._display = screen
        self._icon = [
            [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0]
        ]

        self.enemy_pos_x = int(x)
        self.enemy_pos_y = int(y)

    def draw(self) -> None:
        """
        draw enemy on display
        :return: None
        """
        self._display.set_pen(WHITE)

        for y, row in enumerate(self._icon):
            for x, c in enumerate(row):
                if c == 1:
                    self._display.pixel(x + self.enemy_pos_x, y + self.enemy_pos_y)


class Gun:

    GUN_SPEED = const(5)
    BULLET_SPEED = const(8)

    def __init__(self, screen, icon: list, x: int, y: int):
        """
        gun constructor
        :param screen: display
        :param icon: icon image as list with bin values
        :param x: x position
        :param y: y position
        """
        self._display = screen
        self._icon = list(icon)

        self.gun_pos_x = int(x)
        self.gun_pos_y = int(y)

        self.bullet_state = "ready"
        self.bullet_pos_x = None
        self.bullet_pos_y = None

    def handle_input(self) -> None:
        """
        handle player input for gun and bullet incl. draw on display
        :return: None
        """
        button_up = self._display.is_button_a_pressed
        button_down = self._display.is_button_x_pressed
        button_select = Button(9, invert=True).read

        if button_select() and self.bullet_state == "ready":
            self.bullet_state = "fire"
            self.bullet_pos_x = self.gun_pos_x + 6
            self.bullet_pos_y = self.gun_pos_y

        if button_up() and self.gun_pos_x > 5:
            self.gun_pos_x -= self.GUN_SPEED

        if button_down() and self.gun_pos_x < SCREEN_WIDTH - 15:
            self.gun_pos_x += self.GUN_SPEED

        if self.bullet_state == "fire":
            self._display.set_pen(BLUE)
            self.bullet_pos_y -= self.BULLET_SPEED
            self._display.pixel(self.bullet_pos_x, self.bullet_pos_y)

        if self.bullet_state == "fire" and self.bullet_pos_y < 15:
            self.bullet_state = "ready"

        self._display.set_pen(YELLOW)

        for y, row in enumerate(self._icon):
            for x, c in enumerate(row):
                if c == 1:
                    self._display.pixel(x + self.gun_pos_x, y + self.gun_pos_y)


def collision_check(point: list, rectangle: list) -> bool:
    """
    check whether a point is inside a rectangular
    :param point: list of x,y position coordinates
    :param rectangle: list of x,y position coordinates
    :return: bool
    """
    point_x, point_y = point
    rect_x1, rect_y1 = rectangle
    rect_x2 = rect_x1 + 10
    rect_y2 = rect_y1 + 8

    if rect_x1 < point_x < rect_x2:
        if rect_y1 < point_y < rect_y2:
            return True

    return False


display = PicoVision(PEN_RGB555, SCREEN_WIDTH, SCREEN_HEIGHT)
display.set_font("bitmap8")

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
BLUE = display.create_pen(0, 0, 255)
YELLOW = display.create_pen(255, 255, 0)

gun_icon = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

interface = Interface(screen=display, icon=gun_icon)

enemies = []
enemy_add = 15
enemy_start = 100
for _ in range(8):
    enemy = Enemy(screen=display, x=enemy_start, y=20)
    enemies.append(enemy)
    enemy_start += enemy_add

gun = Gun(screen=display, icon=gun_icon, x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT - 10)

while True:
    display.set_pen(BLACK)
    display.clear()

    interface.draw()

    # @ToDo: move enemies

    for enemy in enemies:
        enemy.draw()

        if gun.bullet_state == "fire":
            if collision_check(point=[gun.bullet_pos_x, gun.bullet_pos_y],
                               rectangle=[enemy.enemy_pos_x, enemy.enemy_pos_y]):
                interface.score += 1
                enemies.remove(enemy)
                gun.bullet_state = "ready"

    # @ToDo: enemy shoot

    # @ToDo: buildings

    gun.handle_input()

    display.update()
