import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import numpy as np
global colli
colli = 0
class Joystick:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    height=240,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # Input pins:
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT

        # Turn on the Backlight
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for color.
        self.width = self.disp.width
        self.height = self.disp.height

class Character:
    global colli
    def __init__(self, spawn_position):
        self.appearance = 'rectangle'
        self.state = None           #왼쪽                   위쪽                      오른쪽                        아래쪽
        self.position = np.array([spawn_position[0] - 10, spawn_position[1] - 10, spawn_position[0] + 10, spawn_position[1] + 10])
        self.outline = "#FFFFFF"
    def fail(self, spawn_position):
        self.position = np.array([spawn_position[0] - 10, spawn_position[1] - 10, spawn_position[0] + 10, spawn_position[1] + 10])
    def move(self, command=None):
        if command is None or not command['move']:
            self.state = None
            self.outline = "#FFFFFF"  # 검정색상 코드!
        else:
            self.state = 'move'
            self.outline = "#FF0000"  # 빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5

            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5

    def collision_check(self, objects, direc):
        global colli
        for obj in objects:
            collision = self.overlap(self.position, obj.position, direc)
            if collision:
                colli = 1

    def goal_check(self, goal,direc):
        collision = self.overlap(self.position, goal.position, direc)
        return collision
    
    def overlap(self, ego_position, other_position, direction):
        if direction == 'U': 
            return not (ego_position[2]  < other_position[0] or
                    ego_position[0]  > other_position[2] or
                    ego_position[3]  < other_position[1] or
                    ego_position[1] - 5 > other_position[3])
        if direction == 'D':
            return not (ego_position[2] < other_position[0] or
                    ego_position[0] > other_position[2] or
                    ego_position[3] + 5 < other_position[1] or
                    ego_position[1] > other_position[3])
        if direction == 'L':
            return not (ego_position[2] < other_position[0] or
                    ego_position[0] - 5 > other_position[2] or
                    ego_position[3] < other_position[1] or
                    ego_position[1] > other_position[3])
        if direction == 'R':
            return not (ego_position[2] + 5 < other_position[0] or
                    ego_position[0] > other_position[2] or
                    ego_position[3] < other_position[1] or
                    ego_position[1] > other_position[3])
        if direction == 'G':
            return not (ego_position[2]  < other_position[0] or
                    ego_position[0]  > other_position[2] or
                    ego_position[3]  < other_position[1] or
                    ego_position[1]  > other_position[3])
            
    
class Objects:
    def __init__(self, spawn_position):
        self.appearance = 'rectangle'
        self.state = 'UP'
        self.position = np.array([spawn_position[0] - 15, spawn_position[1] - 15, spawn_position[0] + 15, spawn_position[1] + 15])
        self.outline = "#00FF00" 

class Goal:
    def __init__(self, spawn_position):
        self.appearance = 'rectangle'
        self.state = 'UP'
        self.position = np.array([spawn_position[0] - 15, spawn_position[1] - 15, spawn_position[0] + 15, spawn_position[1] + 15])
        self.outline = "#00FF00"
def game_over_screen(joystick):
    clear_image = Image.new("RGB", (joystick.width, joystick.height))
    clear_draw = ImageDraw.Draw(clear_image)
    clear_draw.text((50, 100), "CLEAR!!!", font=None, fill=(255, 255, 255))
    joystick.disp.image(clear_image)
    time.sleep(2)

def stage1():
    global colli
    colli = 0
    joystick = Joystick()
    my_image = Image.new("RGB", (joystick.width, joystick.height))
    my_draw = ImageDraw.Draw(my_image)
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 0, 0, 100))
    joystick.disp.image(my_image)
    posi = 15
    # 잔상이 남지 않는 코드 & 대각선 이동 가능
    my_circle = Character((posi*5,posi*15))

    goal = Goal((posi*3,posi))

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
    object_1 = Objects((posi,posi))
    #object_2 = Objects((posi*3,posi))
    object_3 = Objects((posi*5,posi))
    object_4 = Objects((posi*7,posi))
    object_5 = Objects((posi*9,posi))
    object_11 = Objects((posi*11,posi))
    object_15 = Objects((posi*13,posi))
    object_14 = Objects((posi*15,posi))

    object_6 = Objects((posi,posi*3))
    object_7 = Objects((posi,posi*5))
    object_8 = Objects((posi,posi*7))
    object_9 = Objects((posi,posi*9))
    object_10 = Objects((posi,posi*11))
    object_12 = Objects((posi,posi*13))
    object_13 = Objects((posi,posi*15))

    object_16 = Objects((posi*3,posi*15))
    #object_17 = Objects((posi*5,posi*15))
    object_18 = Objects((posi*7,posi*15))
    object_19 = Objects((posi*9,posi*15))
    object_20 = Objects((posi*11,posi*15))
    object_21 = Objects((posi*13,posi*15))
    object_22 = Objects((posi*15,posi*15))

    object_23 = Objects((posi*15,posi*3))
    object_24 = Objects((posi*15,posi*5))
    object_25 = Objects((posi*15,posi*7))
    object_26 = Objects((posi*15,posi*9))
    object_27 = Objects((posi*15,posi*11))
    object_28 = Objects((posi*15,posi*13))

    objects_list = [object_1,  object_3, object_4, object_5, object_6, object_7,object_8,object_9,object_10, object_11, object_12
                    , object_13, object_14, object_15, object_16,  object_18, object_19, object_20, object_21
                    ,object_22, object_23, object_24, object_25, object_26, object_27, object_28]
    direction_1 = 'A'
    direction_2 = 'A'
    direction_3 = 'A'
    direction_4 = 'A'
    direction_count = 0
    direction_list = [direction_1, direction_2, direction_3, direction_4]
    while True:
        while direction_count < 4:
            #command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
        
            if not joystick.button_U.value:  # up pressed
                direction_list[direction_count] = 'U'
                print(direction_count)
                direction_count += 1
                time.sleep(0.2)

            if not joystick.button_D.value:  # down pressed
                direction_list[direction_count] = 'D'
                print(direction_count)
                direction_count += 1
                time.sleep(0.2)

            if not joystick.button_L.value:  # left pressed
                direction_list[direction_count] = 'L'
                print(direction_count)
                direction_count += 1
                time.sleep(0.2)

            if not joystick.button_R.value:  # right pressed
                direction_list[direction_count] = 'R'
                print(direction_count)
                direction_count += 1
                time.sleep(0.2)

            if not joystick.button_A.value: # A pressed
                direction_count = 0
                print(direction_count)
                time.sleep(0.2)

            my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
            my_draw.rectangle(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
            my_draw.rectangle(tuple(goal.position), outline = goal.outline)
            for object in objects_list:
                my_draw.rectangle(tuple(object.position), outline = object.outline, fill = (255, 0, 0))
            
            #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
            joystick.disp.image(my_image)
        print(direction_list)
        for i in range(4):
            go = 0
            colli = 0
            while colli == 0:
                command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
                if direction_list[i] == 'U':
                    command['up_pressed'] = True
                    command['move'] = True
                if direction_list[i] == 'D':
                    command['down_pressed'] = True
                    command['move'] = True
                if direction_list[i] == 'L':
                    command['left_pressed'] = True
                    command['move'] = True
                if direction_list[i] == 'R':
                    command['right_pressed'] = True
                    command['move'] = True
                
                my_circle.move(command)

                my_circle.collision_check(objects_list, direction_list[i])

                if  my_circle.goal_check(goal, 'G'):
                    go = 1
                    clear = 1  
                    break

                #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
                my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
                my_draw.rectangle(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
                my_draw.rectangle(tuple(goal.position), outline = goal.outline)
                for object in objects_list:
                    my_draw.rectangle(tuple(object.position), outline = object.outline, fill = (255, 0, 0))
            
                #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
                joystick.disp.image(my_image)
            
            my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
            my_draw.rectangle(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
            my_draw.rectangle(tuple(goal.position), outline = goal.outline )
            for object in objects_list:
                my_draw.rectangle(tuple(object.position), outline = object.outline, fill = (255, 0, 0))
            
            joystick.disp.image(my_image)
        if go == 0:
            print('Fail...')
            direction_count = 0
            my_circle.fail((posi*5,posi*15))
        elif clear == 1 :
            game_over_screen(joystick)
            break