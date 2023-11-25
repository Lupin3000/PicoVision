from picovision import PicoVision, PEN_RGB555


display = PicoVision(PEN_RGB555, 640, 480)
WHITE = display.create_pen(255, 255, 255)

display.set_pen(WHITE)
display.text('Hello world', 0, 0, 640, 4)
display.update()
