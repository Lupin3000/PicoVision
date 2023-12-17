from micropython import const
from picovision import PicoVision, PEN_RGB555
from pimoroni import Button
from math import radians, cos, sin
import gc


SCREEN_WIDTH = const(320)
SCREEN_HEIGHT = const(240)


class Tank:

    GUN_ROTATION_SPEED = const(2)
    GUN_LENGTH = const(15)
    BULLET_SPEED = const(5)

    def __init__(self, screen, center_x: int, center_y: int):
        """
        tank constructor
        :param screen: display
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
        handle player input by buttons to move gun and to shoot the bullet
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


display = PicoVision(PEN_RGB555, SCREEN_WIDTH, SCREEN_HEIGHT)
display.set_font("bitmap8")

SKY = display.create_pen(165, 182, 209)
GROUND = display.create_pen(9, 84, 5)
TANK = display.create_pen(150, 150, 150)
GUN = display.create_pen(100, 100, 100)
BULLET = display.create_pen(0, 0, 0)

ground = [0, int(SCREEN_HEIGHT // 1.05), SCREEN_WIDTH, SCREEN_HEIGHT]
tank = Tank(screen=display, center_x=50, center_y=ground[1])

while True:
    display.set_pen(SKY)
    display.clear()

    display.set_pen(GROUND)
    display.rectangle(ground[0], ground[1], ground[2], ground[3])

    tank.handle_player_input()

    display.update()
    gc.collect()
