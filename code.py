import pygame
import sys
import time
from pygame.math import Vector2
from random import randint

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('TankArcade2D')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    clock = pygame.time.Clock()
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.mixer.init()

    fontUI = pygame.font.Font(None, 30)
    tank_image = pygame.image.load('images/tank.png')
    bullet_image = pygame.image.load('images/bullet.png')
    brick_image = pygame.image.load('images/block_brick.png')
    bullet_image = pygame.transform.scale(bullet_image, (10, 15))
    bangs_images = [
        pygame.image.load('images/bang1.png'),
        pygame.image.load('images/bang2.png'),
        pygame.image.load('images/bang3.png'),
    ]
    small_font = pygame.font.SysFont("comicsansms", 25)
    medium_font = pygame.font.SysFont("comicsansms", 50)
    large_font = pygame.font.SysFont("Yu Mincho Demibold", 85)
    smallest_font = pygame.font.SysFont("Yu Mincho Demibold", 25)

    FPS = 60
    TILE = 32


    def terminate():
        pygame.quit()
        sys.exit()


    def text_objects(text, color, text_size="small"):
        text_surface = small_font.render(text, True, color)
        if text_size == "medium":
            text_surface = medium_font.render(text, True, color)
        if text_size == "large":
            text_surface = large_font.render(text, True, color)
        if text_size == "vsmall":
            text_surface = smallest_font.render(text, True, color)

        return text_surface, text_surface.get_rect()


    def message_to_screen(msg, color, y_displace=0, mes_size="small"):
        text_surf, text_rect = text_objects(msg, color, mes_size)
        text_rect.center = (int(width / 2), int(height / 2) + y_displace)
        screen.blit(text_surf, text_rect)


    def text_to_button(msg, color, btn_x, btn_y, btn_width, btn_height, btn_size="vsmall"):
        text_surf, text_rect = text_objects(msg, color, btn_size)
        text_rect.center = ((btn_x + (btn_width / 2)), btn_y + (btn_height / 2))
        screen.blit(text_surf, text_rect)


    def button(text, x, y, btn_width, btn_height, inactive_color, active_color, action=None):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        if x + btn_width > cur[0] > x and y + btn_height > cur[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, btn_width, btn_height))
            if click[0] == 1 and action is not None:
                if action == "quit":
                    terminate()

                elif action == "controls":
                    return True

                if action == "play":
                    return True

                if action == "main":
                    return True

        else:
            pygame.draw.rect(screen, inactive_color, (x, y, btn_width, btn_height))

        text_to_button(text, 'black', x, y, btn_width, btn_height)


    def game_intro():
        while True:
            screen.fill('black')
            message_to_screen("Welcome to TankArcade2D!", 'red', -100, mes_size="large")
            message_to_screen("Shoot and destroy the enemy tank", 'yellow', 15)
            message_to_screen("before they destroy you", 'yellow', 60)
            btn1 = button("Play", 150, 500, 150, 50, 'green', 'yellow', action="play")
            btn2 = button("Controls", 350, 500, 150, 50, 'green', 'yellow', action="controls")
            btn3 = button("Quit", 550, 500, 150, 50, 'green', 'yellow', action="quit")
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif btn1:
                    return
                elif btn2:
                    return game_controls()
                elif btn3:
                    terminate()
            pygame.display.update()
            pygame.display.flip()
            clock.tick(FPS)


    def pause():
        paused = True
        message_to_screen("Paused", 'white', -100, mes_size="large")
        message_to_screen("Press Esc to continue playing or Q to quit", 'green', 25)
        pygame.display.update()
        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        paused = False
                    elif ev.key == pygame.K_q:
                        terminate()


    def game_over(player):
        pygame.mixer.music.load('lose_music.mp3')
        pygame.mixer.music.play()
        end_time = time.time()
        with open('data.txt', mode='a+') as file:
            file.write(f'Winner: {player}, time: {int(end_time - start_time)}, '
                       f'shots: {bullet_count}\n')

        while True:
            screen.fill('black')
            message_to_screen("Game Over", 'red', -100, mes_size="large")
            message_to_screen(f"{player} wins", 'red', -30)
            message_to_screen(f"It took {int(end_time - start_time)} seconds", 'red', 10)
            message_to_screen(f"{bullet_count} shots were fired", 'red', 50)

            btn1 = button("Play", 150, 500, 150, 50, 'green', 'yellow', action="play")
            btn2 = button("Controls", 350, 500, 150, 50, 'green', 'yellow', action="controls")
            btn3 = button("Quit", 550, 500, 150, 50, 'green', 'yellow', action="quit")
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif btn1:
                    return
                elif btn2:
                    return game_controls()
                elif btn3:
                    terminate()
            pygame.display.update()
            pygame.display.flip()
            clock.tick(FPS)


    def game_controls():
        while True:
            screen.fill('black')
            message_to_screen("Controls", 'yellow', -100, mes_size="large")
            message_to_screen("Fire: Q and Enter", 'yellow', -30)
            message_to_screen("Move Tank: WASD and Arrows", 'yellow', 10)
            message_to_screen("Pause: Escape", 'yellow', 50)

            btn1 = button("Play", 150, 500, 150, 50, 'green', 'yellow', action="play")
            btn2 = button("Main", 350, 500, 150, 50, 'green', 'yellow', action="main")
            btn3 = button("Quit", 550, 500, 150, 50, 'green', 'yellow', action="quit")
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    terminate()
                elif btn1:
                    return
                elif btn2:
                    return game_intro()
                elif btn3:
                    terminate()
            pygame.display.update()
            pygame.display.flip()
            clock.tick(FPS)


    class Tank:
        def __init__(self, color, px, py, angle, vector):
            self.color = color
            pos = (px, py)
            objects.append(self)
            self.type = 'tank'
            self.image = pygame.transform.rotate(tank_image, -angle)
            self.original_image = self.image

            self.rect = self.image.get_rect(center=pos)
            self.position = Vector2(pos)
            self.direction = Vector2(vector, 0)
            self.speed = 0
            self.angle_speed = 0
            self.angle = 0

            self.hp = 1
            self.shotTimer = 0
            self.shot = False
            self.shotDelay = 60
            self.bulletSpeed = 5
            self.bulletDamage = 1

        def update(self):
            if self.angle_speed != 0:
                # Rotate the direction vector and then the image.
                self.direction.rotate_ip(self.angle_speed)
                self.angle += self.angle_speed
                self.image = pygame.transform.rotate(self.original_image, -self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
            # Update the position vector and the rect.
            self.position += self.direction * self.speed
            self.rect.center = self.position
            for obj in objects:
                if obj != self and obj.type in 'block' and self.rect.colliderect(obj.rect):
                    self.position += -self.direction * self.speed
                    self.rect.center = self.position

            if self.shot and self.shotTimer == 0:
                global bullet_count
                bullet_count += 1
                new_position = self.position + self.direction * 10
                Bullet(self, new_position, self.direction, self.bulletDamage, self.bulletSpeed, self.angle)
                self.shotTimer = self.shotDelay
                self.shot = False

            if self.shotTimer > 0:
                self.shotTimer -= 1

        def draw(self):
            screen.blit(self.image, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)


    class Bullet:
        def __init__(self, parent, pos, direction, damage, speed, angle):
            bullets.append(self)
            self.image = pygame.transform.rotate(bullet_image, -angle - 90)
            self.rect = self.image.get_rect(center=pos)
            self.parent = parent
            self.speed = speed
            self.position = pos
            self.direction = Vector2(direction)
            self.damage = damage

        def update(self):
            self.position += self.direction * self.speed
            self.rect.center = self.position

            if self.position[0] < 0 or self.position[0] > width or self.position[1] < 0 or self.position[1] > height:
                bullets.remove(self)
            else:
                for obj in objects:
                    if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.position):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.position)
                        break

        def draw(self):
            screen.blit(self.image, self.rect)


    class Block:
        def __init__(self, px, py, size):
            objects.append(self)
            self.type = 'block'

            self.rect = pygame.Rect(px, py, size, size)
            self.hp = 1

        def update(self):
            pass

        def draw(self):
            screen.blit(brick_image, self.rect)

        def damage(self, value):
            self.hp -= value
            if self.hp <= 0:
                objects.remove(self)


    class UI:
        def __init__(self):
            pass

        def update(self):
            pass

        def draw(self):
            i = 0
            for obj in objects:
                if obj.type == 'tank':
                    pygame.draw.rect(screen, obj.color, (5 + i * 70, 5, 22, 22))

                    text = fontUI.render(str(obj.hp), 1, obj.color)
                    rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                    screen.blit(text, rect)
                    i += 1


    class Bang:
        def __init__(self, pos):
            objects.append(self)
            self.type = 'bang'

            self.position = pos
            self.frame = 0

        def update(self):
            self.frame += 0.2
            if self.frame >= 3:
                objects.remove(self)

        def draw(self):
            image = bangs_images[int(self.frame)]
            rect = image.get_rect(center=self.position)
            screen.blit(image, rect)


    bullet_count = 0
    bullets = []
    objects = []
    player1 = Tank('blue', 100, 275, 90, 1)
    player2 = Tank('red', 650, 275, -90, -1)
    ui = UI()
    for _ in range(50):
        while True:
            x = randint(0, width // TILE - 1) * TILE
            y = randint(0, height // TILE - 1) * TILE
            rect = pygame.Rect(x, y, TILE, TILE)
            fined = False
            for obj in objects:
                if rect.colliderect(obj.rect):
                    fined = True

            if not fined:
                break

        Block(x, y, TILE)

    start = True
    running = True
    game_intro()
    while running:
        if start:
            bullet_count = 0
            start_time = time.time()
            bullets = []
            objects = []
            player1 = Tank('blue', 100, 275, 90, 1)
            player2 = Tank('red', 650, 275, -90, -1)
            ui = UI()
            for _ in range(50):
                while True:
                    x = randint(0, width // TILE - 1) * TILE
                    y = randint(0, height // TILE - 1) * TILE
                    rect = pygame.Rect(x, y, TILE, TILE)
                    fined = False
                    for obj in objects:
                        if rect.colliderect(obj.rect):
                            fined = True

                    if not fined:
                        break

                Block(x, y, TILE)
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.play(-1)
            start = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player1.shot = True
                if event.key == pygame.K_RETURN:
                    player2.shot = True

                if event.key == pygame.K_w:
                    player1.speed = 1
                elif event.key == pygame.K_s:
                    player1.speed = -1
                elif event.key == pygame.K_a:
                    player1.angle_speed = -4
                elif event.key == pygame.K_d:
                    player1.angle_speed = 4

                if event.key == pygame.K_UP:
                    player2.speed = 1
                elif event.key == pygame.K_DOWN:
                    player2.speed = -1
                elif event.key == pygame.K_LEFT:
                    player2.angle_speed = -4
                elif event.key == pygame.K_RIGHT:
                    player2.angle_speed = 4

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player1.speed = 0
                elif event.key == pygame.K_s:
                    player1.speed = 0
                elif event.key == pygame.K_a:
                    player1.angle_speed = 0
                elif event.key == pygame.K_d:
                    player1.angle_speed = 0

                if event.key == pygame.K_LEFT:
                    player2.angle_speed = 0
                elif event.key == pygame.K_RIGHT:
                    player2.angle_speed = 0
                elif event.key == pygame.K_UP:
                    player2.speed = 0
                elif event.key == pygame.K_DOWN:
                    player2.speed = 0
                if event.key == pygame.K_ESCAPE:
                    pause()
        screen.fill('black')
        for obj in objects:
            obj.update()
        for bullet in bullets:
            bullet.update()
        ui.update()

        for obj in objects:
            obj.draw()
        for bullet in bullets:
            bullet.draw()
        ui.draw()

        if player1.hp <= 0:
            game_over('2 player')
            start = True
        elif player2.hp <= 0:
            game_over('1 player')
            start = True
        pygame.display.update()
        clock.tick(FPS)
