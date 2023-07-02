from pyray import *
import random
import os

class Sapper:

    area = {}
    mine_rows = []
    mine_cols = []
    rec_width = None
    rec_height = None
    texture_bomb = None
    texture_flag = None
    end_game = False
    score = 0

    def __init__(self):
        self.rec_width = 50
        self.rec_height = 50
        path = os.path.dirname(os.path.abspath(__file__))
        self.texture_bomb = load_texture(os.path.join(path, 'resources') + "/bomb.png")
        self.texture_flag = load_texture(os.path.join(path, 'resources') + "/flag.png")
        self.end_game = False

    def randomizer(self):
        while len(self.mine_rows) <= 30:
            self.mine_rows.append(random.randint(0, 9))
            self.mine_cols.append(random.randint(0, 9))
        for row, col in zip(self.mine_rows, self.mine_cols):
            self.area[row][col][1] = True

    def createArea(self):
        for i in range(0, 10):
            self.area[i] = {}
            for j in range(0, 10):
                x = j * self.rec_width
                y = i * self.rec_height
                rec = Rectangle(x, y, self.rec_width, self.rec_height)
                self.area[i][j] = [rec, False, False, 0, False] #rec, is_mine, is_open, number_of_mines_around, flag

    def drawArea(self):
        for i in range(0, 10):
            for j in range(0, 10):
                x = j * self.rec_width
                y = i * self.rec_height
                if self.area[i][j][2]:
                    draw_rectangle_rec(self.area[i][j][0], LIGHTGRAY)
                    if self.area[i][j][1]:
                        draw_texture(self.texture_bomb, x, y, WHITE)
                        self.end_game = True
                    else:
                        draw_text(f"{self.area[i][j][3]}", x + 20, y + 15, 20, BLACK)
                else:
                    draw_rectangle_rec(self.area[i][j][0], DARKBLUE)
                    if self.area[i][j][4]:
                        draw_texture(self.texture_flag, x, y, WHITE)
                draw_rectangle_lines(x, y, self.rec_width, self.rec_height, BLACK)

    def aroundChecker(self, x, y, open = False) -> int:
        count = 0
        for i in range(max(x-1, 0), min(x+2, len(self.area))):
            for j in range(max(y-1, 0), min(y+2, len(self.area[0]))):
                if self.area[i][j][1]:
                    count += 1
                if not self.area[i][j][1] and open:
                    self.area[i][j][3] = self.aroundChecker(i, j)
                    self.area[i][j][2] = True
        return count

    def clicked(self):
        mouse = get_mouse_position()
        for i in range(0, 10):
            for j in range(0, 10):
                x = j * self.rec_width
                y = i * self.rec_height
                if mouse.x > x and mouse.x < x + self.rec_width and \
                mouse.y > y and mouse.y < y + self.rec_height:
                    self.area[i][j][2] = True
                    self.area[i][j][3] = self.aroundChecker(i, j, True)
                    if not self.area[i][j][1]:
                        self.score += 1

    def flag(self):
        mouse = get_mouse_position()
        for i in range(0, 10):
            for j in range(0, 10):
                x = j * self.rec_width
                y = i * self.rec_height
                if mouse.x > x and mouse.x < x + self.rec_width and \
                mouse.y > y and mouse.y < y + self.rec_height and not self.area[i][j][2]:
                    self.area[i][j][4] = not self.area[i][j][4]

    def checkEndGame(self):
        succes = True
        for i in range(0, 10):
            for j in range(0, 10):
                if self.area[i][j][1] and not self.area[i][j][4]:
                    succes = False
                if not self.area[i][j][1] and not self.area[i][j][2]:
                    succes = False
        return succes


    def show(self):
        set_target_fps(30)
        self.createArea()
        self.randomizer()
        while not window_should_close():
            begin_drawing()
            clear_background(PURPLE)
            if is_mouse_button_pressed(MOUSE_LEFT_BUTTON) and not self.end_game:
                self.clicked()
            if is_mouse_button_pressed(MOUSE_RIGHT_BUTTON) and not self.end_game:
                self.flag()
            draw_text(f"Score: {self.score}", 530, 40, 20, BLACK)
            self.drawArea()
            if self.end_game or self.checkEndGame():
                color = Color(0, 0, 0, 168)
                rec = Rectangle(0, 0, 650, 500)
                draw_rectangle_rec(rec, color)
                if self.checkEndGame():
                    draw_text(f"Victory!", 250, 180, 30, WHITE)
                draw_text(f"Score: {self.score}", 250, 220, 30, WHITE)
            end_drawing()

init_window(650, 500, "BarleyBreak")
set_config_flags(ConfigFlags.FLAG_VSYNC_HINT)
test = Sapper()
test.show()