from micropython import const
from picovision import PicoVision, PEN_RGB555
from pimoroni import Button
from math import radians, cos, sin
import gc


SCREEN_WIDTH = const(320)
SCREEN_HEIGHT = const(240)


class Information:

    FONT_SCALE = const(1)

    def __init__(self, screen):
        """
        information constructor
        :param screen: displayed screen
        """
        self._display = screen
        self.level = 1
        self.lives = 3
        self.score = 0

    def draw_information(self) -> None:
        """
        draw information on the display
        :return: None
        """
        self._display.set_pen(INFORMATION)
        self._display.text(f'Level: {self.level}', 10, 10, scale=self.FONT_SCALE)
        self._display.text(f'Lives: {self.lives}', 120, 10, scale=self.FONT_SCALE)
        self._display.text(f'Score: {self.score}', 230, 10, scale=self.FONT_SCALE)


class Building:

    ROOF = const(5)
    FOUNDATION = const(10)
    WINDOW = const(10)

    def __init__(self, screen, x: int, y: int, w: int, h: int, r: bool = False, s: bool = False, f: bool = False):
        """
        building constructor
        :param screen: displayed screen
        :param x: x position of the building as integer
        :param y: y position of the building as integer
        :param w: width of the building as integer (minimum 30px, maximum 80px)
        :param h: height of the building as integer (minimum 60px, maximum 100px)
        :param r: boolean to indicate roof for building (default: False)
        :param s: boolean to indicate line or single windows (default: False)
        :param f: boolean to indicate building foundation (default: False)
        """
        self._display = screen
        self._pos_x = int(x)
        self._pos_y = int(y)

        if 30 < int(w) > 80:
            self._width = 50
        else:
            self._width = int(w)

        if 60 < int(h) > 100:
            self._height = 80
        else:
            self._height = int(h)

        self._roof = bool(r)
        self._single = bool(s)
        self._foundation = bool(f)

    def _add_roof(self) -> None:
        """
        draw building roof on display
        :return: None
        """
        roof_pos_x = self._pos_x + (self.ROOF * 2)
        roof_pos_y = self._pos_y - self.ROOF
        roof_width = self._width - (self.ROOF * 4)
        self._display.rectangle(roof_pos_x, roof_pos_y, roof_width, self.ROOF)

    def _add_foundation(self) -> None:
        """
        draw building foundation on display
        :return: None
        """
        foundation_pos_x = self._pos_x - (self.FOUNDATION // 2)
        foundation_pos_y = self._pos_y + self._height - self.FOUNDATION
        foundation_width = self._width + self.FOUNDATION
        self._display.rectangle(foundation_pos_x, foundation_pos_y, foundation_width, self.FOUNDATION)

    def _add_windows(self) -> None:
        """
        draw building windows on display
        :return: None
        """
        self._display.set_pen(WINDOWS)
        x = self._pos_x + (self.WINDOW // 2)
        y = self._pos_y + self.WINDOW
        w = self._width - self.WINDOW
        h = self.WINDOW

        for _ in range(6):
            self._display.rectangle(x, y, w, h)
            y += 15

            if y > self._pos_y + self._height - self.WINDOW:
                break

        if self._single:
            self._display.set_pen(BUILDING)
            x1 = x2 = self._pos_x + (self.WINDOW // 2) + 4
            y1 = self._pos_y
            y2 = self._pos_y + self._height

            for _ in range(13):
                self._display.line(x1, y1, x2, y2, 1)
                x1 += 5
                x2 = x1

                if x1 > self._pos_x + self._width - 5:
                    break

    def draw_building(self) -> None:
        """
        draw building on screen
        :return: None
        """
        self._display.set_pen(BUILDING)
        self._display.rectangle(self._pos_x, self._pos_y, self._width, self._height)

        if self._roof:
            self._add_roof()

        if self._foundation:
            self._add_foundation()

        self._add_windows()


class Tank:

    GUN_ROTATION_SPEED = const(2)
    GUN_LENGTH = const(15)
    BULLET_SPEED = const(5)

    def __init__(self, screen, center_x: int, center_y: int):
        """
        tank constructor
        :param screen: displayed screen
        :param center_x: tank center x position in pixel
        :param center_y: tank center y position in pixel
        """
        self._display = screen
        self._tank_center_x = int(center_x)
        self._tank_center_y = int(center_y - 6)
        self._gun_angle = -45
        self._bullet_state = "ready"
        self._bullet_angle = None

        self.bullet_x = self._tank_center_x
        self.bullet_y = self._tank_center_y

    def _calculate_gun_angle(self) -> tuple:
        """
        calculate the gun angle for line
        :return: tuple with x, y integer coordinates
        """
        angle = radians(self._gun_angle)
        x = int(self._tank_center_x + self.GUN_LENGTH * cos(angle))
        y = int(self._tank_center_y + self.GUN_LENGTH * sin(angle))

        return x, y

    def _draw_tank(self) -> None:
        """
        draw tank and gun on the on display
        :return: None
        """
        x, y = self._calculate_gun_angle()

        self._display.set_pen(GUN)
        self._display.line(self._tank_center_x, self._tank_center_y, x, y, 3)

        self._display.set_pen(TANK)
        self._display.circle(self._tank_center_x, self._tank_center_y, 5)
        self._display.rectangle(self._tank_center_x - 10, self._tank_center_y, 20, 6)

    def _calculate_bullet_position(self) -> None:
        """
        calculate new bullet x, y position as rounded integer
        :return: None
        """
        if self._bullet_angle is not None:
            self.bullet_x += round(self.BULLET_SPEED * cos(self._bullet_angle))
            self.bullet_y += round(self.BULLET_SPEED * sin(self._bullet_angle))

    def _draw_bullet(self) -> None:
        """
        draw bullet on display or reset bullet state (if bullet position is outside display bounds)
        :return: None
        """
        if self._bullet_state == "fire":
            self._calculate_bullet_position()

            self._display.set_pen(BULLET)
            self._display.pixel(self.bullet_x, self.bullet_y)

            if self.bullet_x < 0 or self.bullet_x > SCREEN_WIDTH or self.bullet_y < 0 or self.bullet_y > SCREEN_HEIGHT:
                self._bullet_state = "ready"
                self._bullet_angle = None

    def handle_player_input(self) -> None:
        """
        handle player input by buttons to move gun and to shoot the bullet (incl rotation restriction)
        :return: None
        """
        button_up = self._display.is_button_a_pressed
        button_down = self._display.is_button_x_pressed
        button_select = Button(9, invert=True).read

        if button_up() and self._gun_angle > -180:
            self._gun_angle -= self.GUN_ROTATION_SPEED

        if button_down() and self._gun_angle < 0:
            self._gun_angle += self.GUN_ROTATION_SPEED

        if button_select() and self._bullet_state == "ready":
            self._bullet_state = "fire"
            self._bullet_angle = radians(self._gun_angle)
            self.bullet_x = self._tank_center_x
            self.bullet_y = self._tank_center_y

        self._draw_bullet()
        self._draw_tank()


# initialize display
display = PicoVision(PEN_RGB555, SCREEN_WIDTH, SCREEN_HEIGHT)
display.set_font("bitmap8")

# define colors
SKY = display.create_pen(165, 182, 209)
GROUND = display.create_pen(9, 84, 5)
INFORMATION = display.create_pen(50, 50, 50)
BUILDING = display.create_pen(45, 45, 45)
WINDOWS = display.create_pen(50, 250, 25)
TANK = display.create_pen(150, 150, 150)
GUN = display.create_pen(100, 100, 100)
BULLET = display.create_pen(0, 0, 0)

# define important variables and create objects
ground = [0, int(SCREEN_HEIGHT // 1.05), SCREEN_WIDTH, SCREEN_HEIGHT]

game_info = Information(screen=display)

building_a = Building(screen=display, x=35, y=138, w=50, h=90, r=True, s=True)
building_b = Building(screen=display, x=140, y=128, w=40, h=100, f=True)
building_c = Building(screen=display, x=200, y=148, w=40, h=80, s=True)

tank = Tank(screen=display, center_x=100, center_y=ground[1])

# game loop
while True:
    display.set_pen(SKY)
    display.clear()

    display.set_pen(GROUND)
    display.rectangle(ground[0], ground[1], ground[2], ground[3])

    game_info.draw_information()

    building_a.draw_building()
    building_b.draw_building()
    building_c.draw_building()

    tank.handle_player_input()

    display.update()
    gc.collect()
