import pygame, sys
from button import Button
import time
import random

# initializing
pygame.init()
pygame.mixer.init()

# music
pygame.mixer.music.load("start.ogg")
pygame.mixer.music.set_volume(0.3)

# some important variables
screen_width = 798
screen_height = 1338
game_width, game_height = 800, 800
clock = pygame.time.Clock()
surface = pygame.display.set_mode((screen_width, screen_height))

# color
white = (255, 255, 255)
skin_color = (245, 223, 152)
green = (0, 128, 0)
purple = (128, 0, 128)
b = (9, 89, 30)

# --- Create separate surfaces ---
gs_bg = pygame.Surface((game_width, game_width))
game_surface = pygame.Surface((game_width - 50, game_width - 50))
SCOREBOARD_SURFACE = pygame.Surface((800, 100))
control_surface = pygame.Surface((800, 440))

# loading all the images
start_screen_bg = pygame.image.load('start_bg.png').convert_alpha()
start_screen_bg = pygame.transform.scale(start_screen_bg, (screen_width, screen_height))
start_button_img = pygame.image.load('start.png').convert_alpha()
start_button_img = pygame.transform.scale(start_button_img,(400,400))
up_img = pygame.image.load('up.png').convert_alpha()
up_img = pygame.transform.scale(up_img,(150,150))
down_img = pygame.transform.rotate(up_img, 180)
right_img = pygame.transform.rotate(up_img, 270)
left_img = pygame.transform.rotate(up_img, 90)
snake = pygame.image.load('snake.png').convert_alpha()
snake = pygame.transform.scale(snake, (80, 80))
food = pygame.image.load('apple.png').convert_alpha()
food = pygame.transform.scale(food, (80, 80))
skull =pygame.image.load('skull.png').convert_alpha()
skull = pygame.transform.scale(skull, (150, 150))
# creating all the buttons
start_button = Button(start_button_img, 200, 500)
up_button = Button(up_img, 320, 10, )
down_button = Button(down_img, 310, 280)
left_button = Button(left_img, 198, 140)
right_button = Button(right_img, 440, 150)


# display_text_function
def display_text(text, x, y, surface, size, color):
    font = pygame.font.SysFont("Arial", size)
    text = font.render(text, True, color)
    surface.blit(text, (x, y))


def start_screen():
    pygame.mixer.music.play(loops=-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button.is_clicked(x, y):
                    pygame.mixer.music.pause()
                    main_loop()

        surface.blit(start_screen_bg, (0, 0))
        start_button.draw(surface)
        pygame.display.flip()
        clock.tick(60)


def place_food(snake_body):
    while True:
        food_x = random.randint(50, 650)
        food_y = random.randint(150,700)
        if (food_x, food_y) not in snake_body:
            return food_x, food_y


def game_over():
    pygame.mixer.music.load("die.ogg")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = ev.pos
                if 10 < x < 800 and 200 < y < 900:
                    pygame.mixer.music.pause()
                    main_loop()
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_surface.fill(green)
        game_surface.blit(skull,(0,50))
        game_surface.blit(skull,(610,50))
        display_text("Game over", 135, 50, game_surface, 100, white)
        display_text(f'hiscore: - {hiscore}', 100, 300, game_surface, 54, white)
        display_text(f'score :- {score}', 100, 400, game_surface, 54, white)
        display_text("tap to restart ", 100, 600, game_surface, 100, purple)
        surface.blit(game_surface, (25, 125))
        pygame.display.flip()


def main_loop():
    snake_length = 1
    snake_body = []
    now = "left"
    pygame.mixer.music.load("main.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    global snake_x, snake_y
    snake_x = 8
    snake_y = 8
    global velocity_x, velocity_y
    velocity_x = 80
    velocity_y = 0
    global score, hiscore
    score = 0

    gs_bg.fill(b)
    control_surface.fill(skin_color)

    food_x, food_y = place_food(snake_body)

    while True:
        game_surface.fill(green)
        SCOREBOARD_SURFACE.fill(purple)
        with open("hiscore.txt", "r") as file:
            hiscore = file.read().strip()

        display_text(f'hiscore:- {hiscore}', 20, 20, SCOREBOARD_SURFACE, 54, skin_color)
        display_text(f'score :- {score}', 500, 20, SCOREBOARD_SURFACE, 54, skin_color)

        if not hiscore.isdigit():
            hiscore = "0"
        if score > int(hiscore):
            hiscore = str(score)
            with open("hiscore.txt", "w") as file:
                file.write(hiscore)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y > 900:
                    if up_button.is_clicked(x, y - 900):
                        velocity_y -= 75
                        velocity_x = 0
                        now = "up"
                    if down_button.is_clicked(x, y - 900):
                        velocity_y += 75
                        velocity_x = 0
                        now = "down"
                    if right_button.is_clicked(x, y - 900):
                        velocity_x += 75
                        velocity_y = 0
                        now = "right"
                    if left_button.is_clicked(x, y - 900):
                        velocity_x -= 75
                        velocity_y = 0
                        now = "left"

            if velocity_x == 0 and velocity_y == 0:
                if now == "up":
                    velocity_y -= 75
                if now == "down":
                    velocity_y += 75
                if now == "right":
                    velocity_x += 75
                if now == "left":
                    velocity_x -= 75

        # add constant velocity and move snake
        snake_x = snake_x + velocity_x
        snake_y = snake_y + velocity_y

        up_button.draw(control_surface)
        down_button.draw(control_surface)
        left_button.draw(control_surface)
        right_button.draw(control_surface)

        snake_rect = pygame.Rect(snake_x, snake_y, 45, 45)
        food_rect = pygame.Rect(food_x, food_y, 45, 45)

        # checking collision with food
        if snake_rect.colliderect(food_rect):
            main_music_pos = pygame.mixer.music.get_pos() / 1000.0
            pygame.mixer.music.load("score.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()
            time.sleep(0.7)
            pygame.mixer.music.load("main.ogg")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1, start=main_music_pos)
            food_x, food_y = place_food(snake_body)
            score += 1
            snake_length += 1

        if len(snake_body) != len(set(tuple(i) for i in snake_body)):
        	time.sleep(0.5)
        	game_over()

        # checking boundaries
        if -10 > snake_x or snake_x > 720 or snake_y < 0 or snake_y > 700:
            pygame.mixer.music.pause()
            snake_length = 1
            time.sleep(0.5)
            game_over()

        head = [snake_x, snake_y]
        snake_body.append(head)
        if len(snake_body) > snake_length:
            del snake_body[0]

        for x, y in snake_body:
        	game_surface.blit(snake, (x, y))
        if(head in snake_body[:-1]):
        	game_over()
        game_surface.blit(food, (food_x, food_y))
        surface.blit(SCOREBOARD_SURFACE, (0, 0))
        surface.blit(gs_bg, (0, 100))
        surface.blit(game_surface, (25, 125))
        surface.blit(control_surface, (0, 900))
        time.sleep(0.1)
        pygame.display.flip()
        clock.tick(20)


if __name__ == "__main__":
    start_screen()
   