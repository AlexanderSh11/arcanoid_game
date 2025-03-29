import sys

import pygame
from random import randrange as rnd

#screen
width, height = 1200, 700
fps = 60
#creating the screen
pygame.init()
sc = pygame.display.set_mode((width, height)) 
clock = pygame.time.Clock()
#import records
records = []
with open("records_default.txt") as f:
    for line in f:
        records.append([int(x) for x in line.split()])
#fonts
font_score = pygame.font.SysFont('Comic Sans MS', 26)
#paddle
paddle_w = 200
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(width // 2 - paddle_w // 2, height - paddle_h - 10, paddle_w, paddle_h)
#ball (as rectangle)
ball_r = 20
ball_speed = 8
ball_rect = int(ball_r * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
dx, dy = 1, -1 #for direction and its change
#blocks (position: X = 30 + 120i, Y = 10 + 70j)
blocks, colors, bricks= [], [], []
#background
Img = pygame.image.load("Background.jpg").convert()
#global
score = 0
level_n = 0
def level_start(file1, file2):
    global blocks, colors, bricks
    blocks = []
    colors = []
    bricks = []
    with open(file1) as f:
        for line in f:
            coordinates = [float(x) for x in line.split()]
            blocks.append(pygame.Rect(coordinates[0], coordinates[1], 100, 50))
            colors.append((rnd(50, 256), rnd(50, 256), rnd(50, 256)))
    if file2 != '-':
        with open(file2) as f:
            for line in f:
                coordinates = [float(x) for x in line.split()]
                bricks.append(pygame.Rect(coordinates[0], coordinates[1], coordinates[2], coordinates[3]))
def restart():
    global score, dx, dy
    score = 0
    dx, dy = 1, -1
    # drawing objects
    ball.x = rnd(ball_rect, width - ball_rect)
    ball.y = height // 2
#levels
levels =    [(120, 80, 'Главное меню', 'white', 'red', 0),
            (120, 180, 'Уровень 1', 'white', 'red', 1),
            (120, 280, 'Уровень 2', 'white', 'red', 2),
            (120, 380, 'Уровень 3', 'white', 'red', 3),
            (120, 480, 'Уровень 4', 'white', 'red', 4),
            (120, 580, 'Уровень 5', 'white', 'red', 5),]
class Level_Menu:
    global running
    def __init__(self, levels):
        self.levels = levels
    def render(self, screen, font, level_n):
        for i in self.levels:
            if level_n == i[5]:
                screen.blit(font.render(i[2], 1, pygame.Color(i[4])), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, pygame.Color(i[3])), (i[0], i[1]))
    def menu(self):
        global level_n
        done = True
        running = False
        font_menu = pygame.font.SysFont('Comic Sans MS', 50)
        level = 0
        while done:
            sc.blit(Img, (0, 0))
            self.render(sc, font_menu, level)
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_SPACE:
                        if level == 0:
                            done = False
                            game.menu()
                        if level == 1:
                            done = False
                            level_n = 1
                            level_start("level1.txt", '-')
                            restart()
                            running = True
                        if level == 2:
                            done = False
                            level_n = 2
                            level_start("level2.txt", "level2_b.txt")
                            restart()
                            running = True
                        if level == 3:
                            done = False
                            level_n = 3
                            level_start("level3.txt", "level3_b.txt")
                            restart()
                            running = True
                        if level == 4:
                            done = False
                            level_n = 4
                            level_start("level4.txt", "level4_b.txt")
                            restart()
                            running = True
                        if level == 5:
                            done = False
                            level_n = 5
                            level_start("level5.txt", "level5_b.txt")
                            restart()
                            running = True
                    if event.key == pygame.K_UP:
                        if level > 0:
                            level -= 1
                    if event.key == pygame.K_DOWN:
                        if level < len(self.levels) - 1:
                            level += 1
            pygame.display.flip()
#records table
class Record_Menu:
    global running
    def __init__(self, records):
        self.records = records
    def render(self, screen, font):
        k = 0
        screen.blit(pygame.font.SysFont('Comic Sans MS', 50).render('Главное меню', 1, pygame.Color('red')), (120, 80))
        screen.blit(font.render('Счёт', 1, pygame.Color('white')), (120, 170))
        screen.blit(font.render('Уровень', 1, pygame.Color('white')), (320, 170))
        for i in self.records:
            screen.blit(font.render(str(i[0]), 1, pygame.Color('white')), (120, 200 + 30 * k))
            screen.blit(font.render(str(i[1]), 1, pygame.Color('white')), (320, 200 + 30 * k))
            k += 1
    def menu(self):
        done = True
        running = False
        font_menu = pygame.font.SysFont('Comic Sans MS', 26)
        level = 0
        while done:
            sc.blit(Img, (0, 0))
            self.render(sc, font_menu)
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_SPACE:
                        done = False
                        game.menu()
            pygame.display.flip()
#menu
class Menu:
    global running, level_menu
    def __init__(self, options):
        self.options = options
    def render(self, screen, font, option_n):
        for i in self.options:
            if option_n == i[5]:
                screen.blit(font.render(i[2], 1, pygame.Color(i[4])), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], 1, pygame.Color(i[3])), (i[0], i[1]))
    def menu(self):
        done = True
        running = False
        font_menu = pygame.font.SysFont('Comic Sans MS', 50)
        option = 0

        while done:
            sc.blit(Img, (0, 0))
            self.render(sc, font_menu, option)
            render_tips = [[font_score.render('Управление - при помощи клавиш со стрелками.', 1, pygame.Color('black')), (120, 400)],
                           [font_score.render('Пробел - клавиша подтверждения.', 1, pygame.Color('black')), (120, 430)],
                           [font_score.render('Цель игры - разбить все цветные блоки.', 1, pygame.Color('black')), (120, 460)],
                           [font_score.render('Чёрные блоки - стены, их разбить нельзя.', 1, pygame.Color('black')), (120, 490)]]
            for i in range(len(render_tips)):
                sc.blit(render_tips[i][0], render_tips[i][1])
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                        if option == 0:
                            done = False
                            level_menu.menu()
                        if option == 1:
                            done = False
                            record_menu.menu()
                        if option == 2:
                            sys.exit()
                    if event.key == pygame.K_UP:
                        if option > 0:
                            option -= 1
                    if event.key == pygame.K_DOWN:
                        if option < len(self.options) - 1:
                            option += 1
            pygame.display.flip()
#start the level_menu and record_menu
record_menu = Record_Menu(records)
level_menu = Level_Menu(levels)
#start the menu
options = [(120, 80, 'Уровни', 'white', 'red', 0),
           (120, 180, 'Рекорды', 'white', 'red', 1),
           (120, 280, 'Выход', 'white', 'red', 2)]
game = Menu(options)
game.menu()
def ball_block_collision(dx, dy, ball, block):
    if dx>0:
        delta_x = ball.right - block.left
    else:
        delta_x = block.right - ball.left
    if dy>0:
        delta_y = ball.bottom - block.top
    else:
        delta_y= block.bottom - ball.top
    if abs(delta_x-delta_y) < 5:
        dx = -dx
        dy = -dy
    elif delta_x>delta_y:
        dy = -dy
    elif delta_y>delta_x:
        dx = -dx
    return dx, dy
def level_record(level_n, records):
    result = 0
    for i in records:
        if level_n == i[1] and result < i[0]:
            result = i[0]
    return result
def level_min(level_n, records):
    result = 100000
    for i in records:
        if level_n == i[1] and result > i[0]:
            result = i[0]
    return result
def custom_key(records):
    return records[0]
def start():
    global score, dx, dy, bricks, colors, blocks, level_n, records, running
    score, dx, dy = 0, 1, -1
    restart()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.menu()
        current_record = level_record(level_n, records)
        current_min_record = level_min(level_n, records)
        # ball movement
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy
        # ball-border collision
        if ball.centerx < ball_r or ball.centerx > width - ball_r:
            dx = -dx
        if ball.centery < ball_r:
            dy = -dy
        # ball-paddle collision
        if ball.colliderect(paddle) and dy > 0:  # the ball's heading to the paddle
            dx, dy = ball_block_collision(dx, dy, ball, paddle)
        # ball-brick collision
        for brick in bricks:
            if ball.colliderect(brick):
                dx, dy = ball_block_collision(dx, dy, ball, brick)
        # ball-block collision
        h = ball.collidelist(blocks)
        if h != -1:
            hit_block = blocks.pop(h)
            hit_color = colors.pop(h)
            dx, dy = ball_block_collision(dx, dy, ball, hit_block)
            score += 10
        # control
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < width:
            paddle.right += paddle_speed
        # drawing objects
        sc.blit(Img, (0, 0))
        render_score = font_score.render(f'ОЧКИ: {score}', 1, pygame.Color('white'))
        render_record = font_score.render(f'РЕКОРД: {current_record}', 1, pygame.Color('white'))
        sc.blit(render_score, (width - 200, height - 130))
        sc.blit(render_record, (width - 200, height - 80))
        pygame.draw.rect(sc, pygame.Color('#ffff00'), paddle)
        pygame.draw.circle(sc, pygame.Color('#ffffff'), ball.center, ball_r)
        for color, block in enumerate(blocks):
            pygame.draw.rect(sc, colors[color], block)
        for color_b, brick in enumerate(bricks):
            pygame.draw.rect(sc, pygame.Color('#000000'), brick)
        # winning and losing
        if ball.bottom > height + 100 or len(blocks) <= 0:
            if len(blocks) <= 0:
                sc.blit(font_score.render(f'Победа! Ваш результат: {score}', 1, pygame.Color('red')), (width // 2 - 180, height // 2))
            else:
                sc.blit(font_score.render(f'Поражение! Ваш результат: {score}', 1, pygame.Color('red')), (width // 2 - 180, height // 2))
            #record updating
            if current_record == 0 and score > 0:
                for i in records:
                    if i[1] == level_n:
                        i[0] = score
            elif len(records) < 10:
                records.append([score, level_n])
            elif len(records) >= 10 and score > current_min_record:
                for i in records:
                    if i[0] == current_min_record:
                        i[0] = score
            records.sort(key=custom_key, reverse=True)
            #saving records in file
            with open("records_default.txt", 'w') as f:
                for i in records:
                    f.write(str(i[0]) + ' ' + str(i[1]) + '\n')
            pygame.display.flip()
            pygame.time.delay(3000)
            restart()
            game.menu()
        # updating the screen
        pygame.display.flip()
        clock.tick(fps)
#start the game
running = True
while running:
    start()
pygame.quit()
sys.exit()