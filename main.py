from src.testing_game import *
import time
from PIL import Image, ImageDraw, ImageFont
from digitalio import DigitalInOut, Direction, Pull

class Menu:
    def __init__(self, joystick):
        self.joystick = joystick
        self.width = joystick.width
        self.height = joystick.height
        self.clear_image = Image.new("RGB", (self.width, self.height))
        self.clear_draw = ImageDraw.Draw(self.clear_image)

    def show_title_screen(self):
        while True:
            self.clear_draw.rectangle((0, 0, self.width, self.height), fill=(255, 255, 255))
            font_size = 40
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            self.clear_draw.text((30, 100), "NARITA", font=font, fill=(0, 0, 0))
            self.joystick.disp.image(self.clear_image)

            # Wait for A button press
            if not self.joystick.button_A.value:
                break
            time.sleep(0.1)

    def show_help_screen(self):
        while True:
            self.clear_draw.rectangle((0, 0, self.width, self.height), fill=(255, 255, 255))
            font_size = 20
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            help_text = "Welcome to NARITA!\n\nYou can specify a \nIf you move your \ncharacter a set \nnumber of times and \nreach the goal, \nyou win!"
            self.clear_draw.text((5, 10), help_text, font=font, fill=(0, 0, 0))
            self.joystick.disp.image(self.clear_image)

            # Wait for B button press
            if not self.joystick.button_A.value:
                break
            time.sleep(0.1)

    def wait_for_button_press(self):
        while True:
            self.show_title_screen()
            self.show_help_screen()
            break

def game_starter():
    joystick = Joystick()
    menu = Menu(joystick)
    
    while True:
        menu.show_title_screen()
        menu.wait_for_button_press()
        stage1()

if __name__ == "__main__":
    game_starter()