import pygame
import sys
from pygame.sprite import Sprite
from pygame import ftfont
import random
import time


class MyRectangle(Sprite):
    def __init__(self, screen, x, y, color, width=40, height=40):
        super(MyRectangle, self).__init__()
        self.screen = screen
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.y = y
        self.rect.x = x
        self.color = color

    def blit_me(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update_me(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Board:
    def __init__(self, screen, size, color):
        self.screen = screen
        self.size = size
        self.color = color
        self.x_start = 0
        self.y_start = 0
        self.x_end = random.randint(19, 19)
        self.y_end = random.randint(19, 19)
        self.board = []
        self.rectanglesxy = []
        self.prepare_board()

    def __choice(self):
        number = random.choice([0, 1, 2, 3, 4])
        if number % 2 == 0:
            number = 1
        else:
            number = random.choice([0, 1, 2, 3, 4])
            if number != 1:
                number = 0
        return number

    def show_board(self):
        for x in self.board:
            for y in x:
                print(str(y) + " ", end="")
            print("")

    def prepare_board(self):
        for x in range(self.size):
            self.board.append([])

        for x in range(self.size):
            for y in range(self.size):
                number = self.__choice()
                self.board[x].append(number)
                if number == 0:
                    if (x == 0 and y == 0) or (x == 0 and y == 1) or \
                            (self.x_end == x and self.y_end == y) or \
                            (x == 0 and y == 2) or (x == 0 and y == 3) or \
                            (x == 18 and y == 19) or (x == 17 and y == 19) or\
                            (x == 16 and y == 19) or (x == 15 and y == 19):
                        pass
                    else:
                        rec = MyRectangle(self.screen, 40 * x, 40 * y, self.color)
                        self.rectanglesxy.append(rec)

        self.board[0][0] = 1
        self.board[0][1] = 1
        self.board[0][2] = 1
        self.board[0][3] = 1
        self.board[self.x_end][self.y_end] = 1
        self.board[self.x_end - 1][self.y_end] = 1
        self.board[self.x_end - 2][self.y_end] = 1
        self.board[self.x_end - 3][self.y_end] = 1
        self.board[self.x_end - 4][self.y_end] = 1

    def display_board(self):
        for rec in self.rectanglesxy:
            rec.blit_me()


class Solve:
    def __init__(self, board):
        self.board = board
        self.solution = []
        self.x_start = board.x_start
        self.y_start = board.y_start
        self.x_end = board.x_end
        self.y_end = board.y_end
        self.xy_solutions = []
        self.solv_memory = []
        self.path = []

    def prepare_board_for_solution(self):
        s = len(self.board.board)
        for x in range(s):
            self.solution.append([])
            self.solv_memory.append([])
        for x in range(s):
            for y in range(s):
                self.solution[x].append(0)
                self.solv_memory[x].append(0)

    def print_solve(self):
        for x in self.solution:
            for y in x:
                print(str(y) + " ", end="")
            print("")

    def solve(self):
        self.prepare_board_for_solution()
        # self.print_solve()
        flag = self.my_solve(self.x_start, self.y_start, "right")
        print("")
        self.print_solve()
        if flag:
            return True
        return False

    def check(self, x, y):
        if x in range(0, 20) and y in range(0, 20) and self.board.board[x][y] == 1\
                and self.solution[x][y] == 0 and self.solv_memory[x][y] != 1:
            return True
        return False

    def my_solve(self, x, y, direction):
        if (x == self.x_end and y == self.y_end):
            self.solution[x][y] = 1
            return True
        if self.check(x, y):
            x_y = [x, y]
            self.xy_solutions.append(x_y)
            self.solution[x][y] = 1
            self.path.append(x_y)
            self.solv_memory[x][y] = 1
            if direction != "up" and self.my_solve(x, y + 1, "down"):
                return True
            if direction != "left" and self.my_solve(x + 1, y, "right"):
                return True
            if direction != "right" and self.my_solve(x - 1, y, "left"):
                return True
            if direction != "down" and self.my_solve(x, y - 1, "up"):
                return True
            self.path.pop()
            self.solution[x][y] = 0
            return False
        return False


class ShowSteps:
    def __init__(self, points, screen, path, end):
        self.points = points
        self.screen = screen
        self.rectangle = MyRectangle(screen, 0, 0, (255, 0, 0))
        self.dst = MyRectangle(screen, end[0] * 40, end[1] * 40, (255, 255, 0))
        self.path = path
        self.rectangle_for_path = MyRectangle(screen, 0, 0, (255, 255, 0))
        self.start_point = MyRectangle(screen, 0, 0, (0, 255, 0))
        self.counter = 0

    def show(self):
        if self.counter < len(self.points):
            x = self.points[self.counter][0]
            y = self.points[self.counter][1]
            self.rectangle.update_me(x*40, y*40)
            self.rectangle.blit_me()
            self.dst.blit_me()
            self.start_point.blit_me()
            self.counter += 1
            return True
        return False

    def show_path(self):
        for x in self.path:
            self.rectangle_for_path.update_me(x[0]*40, x[1]*40)
            self.rectangle_for_path.blit_me()
            self.dst.blit_me()
            self.start_point.blit_me()

    def show_solution(self):
        for x in self.points:
            self.rectangle.update_me(x[0]*40, x[1]*40)
            self.rectangle.blit_me()
            self.dst.blit_me()
            self.start_point.blit_me()


class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (150, 150, 250)
        self.solution_time = ""
        self.activate = False
        self.restart = False
        self.solved = True
        self.start = False
        self.right_panel = MyRectangle(self.screen, 800, 0, (102, 255, 204), 400, 800)
        self.mouse = Button(screen, "MOUSE", (255, 0, 0), 800, 0, 400, 50)
        self.cheese = Button(screen, "CHEESE", (255, 255, 0), 800, 100, 400, 50)
        self.start_point = Button(screen, "START POINT", (0, 255, 0), 800, 200, 400, 50)
        self.start_button = Button(screen, "PRESS s TO START",
                                   (255, 75, 0), 800, 300, 400, 50)
        self.all_steps = Button(screen, "ALL STEPS", (255, 0, 0), 800, 0, 400, 50)
        self.path = Button(screen, "PATH", (255, 255, 0), 800, 100, 400, 50)
        self.restart_button = Button(screen, "PRESS r TO RESTART",
                                   (255, 75, 0), 800, 500, 400, 50)
        self.time_button = Button(screen, "TIME ",
                                  (125, 125, 125), 800, 300, 400, 50)
        self.success_button = Button(screen, "SUCCESS",
                                  (180, 125, 42), 800, 400, 400, 50)

    def solve(self):
        t1 = time.time()
        self.solved = solve.solve()
        t2 = time.time()
        self.solution_time = t2 - t1
        self.solution_time = str(self.solution_time)
        self.solution_time = self.solution_time[0:5]
        self.time_button.update("TIME USED: " + self.solution_time)
        if self.solved:
            self.success_button.update("SUCCESS")
        else:
            self.success_button.update("DEFEAT")
        print(self.solution_time)

    def show_right_panel(self, panel_number=1):
        self.right_panel.blit_me()
        if panel_number == 0:
            self.start_button.draw_button()
        elif panel_number == 1:
            self.mouse.draw_button()
            self.cheese.draw_button()
            self.start_point.draw_button()
            self.restart_button.draw_button()
            self.time_button.draw_button()
            self.success_button.draw_button()
            # self.start_button.draw_button()
        elif panel_number == 2:
            self.restart_button.draw_button()
            self.path.draw_button()
            self.all_steps.draw_button()
            self.start_point.draw_button()
            self.time_button.draw_button()
            self.success_button.draw_button()


class Button:
    text_color = (255, 255, 255)

    def __init__(self, screen, message, color, x=0, y=0, width=10, height=10):
        self.font = pygame.ftfont.SysFont(None, 48)
        self.screen = screen
        self.button_color = color
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.screen_rect = screen.get_rect()
        self.rect = self.make_button()
        self.prepare_message(message)

    def update(self, message):
        self.prepare_message(message)

    def make_button(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def prepare_message(self, message):
        self.message_image = self.font.render(message, True, self.text_color,
                                              self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)


def check_events(settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                settings.activate = True
            if event.key == pygame.K_r:
                settings.restart = True


def show(settings, steps):
    time.sleep(0.1)
    if not settings.activate:
        settings.show_right_panel(0)
    elif settings.activate and steps.show():
        settings.show_right_panel()
    elif settings.activate:
        settings.show_right_panel(2)
        steps.show_solution()
        steps.show_path()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Rat in maze")
    settings = Settings(screen)
    board = Board(screen, 20, (0, 0, 255))
    solve = Solve(board)
    settings.solve()
    points = solve.xy_solutions
    path = solve.path
    steps = ShowSteps(points, screen, path, [board.x_end, board.y_end])

    while True:
        screen.fill(settings.bg_color)
        board.display_board()
        show(settings, steps)
        check_events(settings)
        if settings.restart:
            board = Board(screen, 20, (0, 0, 255))
            solve = Solve(board)
            settings.solve()
            points = solve.xy_solutions
            path = solve.path
            steps = ShowSteps(points, screen, path, [board.x_end, board.y_end])
            settings.restart = False
        # time.sleep(0.01)
        pygame.display.flip()
