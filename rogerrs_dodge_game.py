import pygame
from pygame.locals import *
import random


SCREEN_WIDTH = SCREEN_W = 800
SCREEN_HEIGHT = SCREEN_H = 600
SCREEN_RESOLUTION = (SCREEN_W, SCREEN_H)

COLOR_GREEN = (0, 191, 0)
COLOR_BLUE = (0, 0, 191)
COLOR_RED = (191, 0, 0)

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

SQUARE_WIDTH = SQUARE_W = 100
SQUARE_HEIGT = SQUARE_H = 100
SQUARE_SIZE = (SQUARE_W, SQUARE_H)
SQUARE_SPEED_MIN = 1
SQUARE_SPEED_MAX = 6
SQUARES_AMOUNT = 2

CAR_START_X = SCREEN_WIDTH / 2 - 1
CAR_START_Y = SCREEN_HEIGHT * 0.8
CAR_START_COORDS = [CAR_START_X, CAR_START_Y]
CAR_WIDTH = CAR_W = 50
CAR_HEIGHT = CAR_H = 50
CAR_SIZE = (CAR_W, CAR_H)
CAR_SPEED = 10

SCORE_CAPTION = "Dodges: "
SCORE_COORDS = [10, 10]

GAMEOVER_CAPTION = "YOU DIED!"

class Game:
    def __init__(self):
        self.squares = []
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_RESOLUTION)

        self.score = 0

        self.square_manager = SquareManager(self)
        self.init_squares()
        self.car = Car(CAR_START_COORDS, CAR_SIZE, CAR_SPEED, self)
        self.score_informer = ScoreInformer(SCORE_COORDS, self)

    def init_squares(self):
        for i in range(SQUARES_AMOUNT):
            square = Square([random.randint(0, SCREEN_W - SQUARE_W), -SQUARE_H],
                            SQUARE_SIZE,
                            random.randint(SQUARE_SPEED_MIN, SQUARE_SPEED_MAX),
                            COLOR_BLUE)
            self.square_manager.squares.append(square)

    def collision_detect(self):
        car_rect = pygame.Rect(self.car.coords, self.car.size)
        return self.square_manager.checkForCollision(car_rect)

    def run(self):
        isContinue = True
        isWaitAfterGameOver = True

        clock = pygame.time.Clock()
        car_events = []

        while isContinue:
            for event in pygame.event.get():
                if event.type == QUIT:
                    isContinue = False
                if event.type in (KEYDOWN, KEYUP):
                    if event.key in (K_LEFT, K_RIGHT):
                        car_events.append(event)
    
            self.car.handle_events(car_events)

            self.screen.fill(COLOR_GREEN)
            time_passed = clock.tick(60)

            self.square_manager.process(time_passed)
            self.car.process(time_passed)
        
            if self.collision_detect():
                isContinue = False

            self.square_manager.render()
            self.car.render(self.screen)
            self.score_informer.render(self.screen)

            car_events = []
            pygame.display.update()

        gameoverInformer = GameoverInformer(self, COLOR_BLACK)
        print(GAMEOVER_CAPTION)
        print(SCORE_CAPTION + str(self.score))
        while isWaitAfterGameOver:
            for event in pygame.event.get():
                if event.type == QUIT:
                    isWaitAfterGameOver = False

            clock.tick(60)

            self.screen.fill(COLOR_RED)
            gameoverInformer.render(self.screen)

            pygame.display.update()

            
class GameoverInformer:
    def __init__(self, game, color = COLOR_WHITE, font_name = "comicsansms", font_size = 40):
        self.color = color
        self.game = game
        self.font_name = font_name
        self.font_size = font_size

        self.load_font()

    def load_font(self):
        self.font = pygame.font.SysFont(self.font_name, self.font_size)    

    def render(self, surface):
        caption = GAMEOVER_CAPTION + " " + SCORE_CAPTION + str(self.game.score)
        caption_surface = self.font.render(caption, True, self.color)
        caption_coords = [(SCREEN_W - caption_surface.get_width()) / 2,
                          (SCREEN_H - caption_surface.get_height()) / 2]
        surface.blit(caption_surface, caption_coords)


class ScoreInformer:
    def __init__(self, coords, game, color = COLOR_WHITE, font_name = "comicsansms", font_size = 80):
        self.coords = coords
        self.color = color
        self.game = game
        self.font_name = font_name
        self.font_size = font_size

        self.load_font()

    def load_font(self):
        self.font = pygame.font.SysFont(self.font_name, self.font_size)    

    def render(self, surface):
        caption_surface = self.font.render(SCORE_CAPTION + str(self.game.score), True, self.color)
        surface.blit(caption_surface, self.coords)

class SquareManager:
    def __init__(self, game):
        self.game = game
        self.squares = []

    def render(self):
        for square in self.squares:
            square.render(self.game.screen)

    def process(self, time_passed):
        for square in self.squares:
            square.process(time_passed)
        self.checkForUnderScreen()

    def checkForUnderScreen(self):
        for square in self.squares:
            if square.coords[1] > self.game.screen.get_height():
                square.coords = [random.randint(0, SCREEN_W - SQUARE_W), -SQUARE_H]
                square.speed = random.randint(SQUARE_SPEED_MIN, SQUARE_SPEED_MAX)

                self.game.score += 1

    def checkForCollision(self, rect):
        for square in self.squares:
            square_rect = pygame.Rect(square.coords, square.size)
            if square_rect.x <= rect.x <= square_rect.x + square_rect.w and \
               square_rect.y <= rect.y <= square_rect.y + square_rect.h:
                return True
            if square_rect.x <= rect.x + rect.w <= square_rect.x + square_rect.w and \
               square_rect.y <= rect.y <= square_rect.y + square_rect.h:
                return True
            if square_rect.x <= rect.x <= square_rect.x + square_rect.w and \
               square_rect.y <= rect.y + rect.h <= square_rect.y + square_rect.h:
                return True
            if square_rect.x <= rect.x + rect.w <= square_rect.x + square_rect.w and \
               square_rect.y <= rect.y + rect.h <= square_rect.y + square_rect.h:
                return True

        return False
                

class Square:
    def __init__(self, coords, size, speed, color):
        self.coords = coords
        self.size = size
        self.speed = speed
        self.color = color

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.coords[0], self.coords[1], self.size[0], self.size[1]))

    def process(self, time_passed):
        self.coords[1] += self.speed

class Car:
    def __init__(self, coords, size, speed, game, bgcolor = COLOR_BLACK, image_path = None):
        self.coords = coords
        self.size = size
        self.speed = speed
        self.game = game
        self.bgcolor = bgcolor
        self.image_path = image_path
        self.direction = [0, 0]

    def render(self, surface):
        car_surface = pygame.Surface(self.size)
        car_surface.fill(self.bgcolor)
        if self.image_path is not None:
            image_surface = pygame.image.load(self.image_path)
            car_surface.blit(image_surface, (0, 0))
        surface.blit(car_surface, self.coords)

    def handle_events(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.direction = [-1, 0]
                elif event.key == K_RIGHT:
                    self.direction = [1, 0]
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT):
                    self.direction = [0, 0]

    def process(self, time_passed):
        if self.direction[0] != 0:
            self.tryMove()
        
    def tryMove(self):
        newX = self.direction[0] * self.speed + self.coords[0]
        if newX <= 0:
            newX = 0
        if newX >= SCREEN_W - self.size[1]:
            newX = SCREEN_W - self.size[1]

        self.coords[0] = newX

def run():
    game = Game()
    game.run()

if __name__ == '__main__':
    run()