import pygame
from pygame.math import Vector2

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('TankArcade2D')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    clock = pygame.time.Clock()
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)

    tank_image = pygame.image.load('images/tank.png')
    bullet_image = pygame.image.load('images/bullet.png')
    bullet_image = pygame.transform.scale(bullet_image, (10, 15))
    smallfont = pygame.font.SysFont("comicsansms", 25)
    medfont = pygame.font.SysFont("comicsansms", 50)
    largefont = pygame.font.SysFont("Yu Mincho Demibold", 85)
    vsmallfont = pygame.font.SysFont("Yu Mincho Demibold", 25)

    FPS = 60
    TILE = 32


    def text_objects(text, color, size="small"):
        if size == "small":
            text_surface = smallfont.render(text, True, color)
        if size == "medium":
            text_surface = medfont.render(text, True, color)
        if size == "large":
            text_surface = largefont.render(text, True, color)
        if size == "vsmall":
            text_surface = vsmallfont.render(text, True, color)

        return text_surface, text_surface.get_rect()


    def message_to_screen(msg, color, y_displace=0, size="small"):
        textSurf, textRect = text_objects(msg, color, size)
        textRect.center = (int(width / 2), int(height / 2) + y_displace)
        screen.blit(textSurf, textRect)


    def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="vsmall"):
        textSurf, textRect = text_objects(msg, color, size)
        textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
        screen.blit(textSurf, textRect)


    def button(text, x, y, width, height, inactive_color, active_color, action=None, size=" "):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        # print(click)
        if x + width > cur[0] > x and y + height > cur[1] > y:
            pygame.draw.rect(screen, active_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                if action == "quit":
                    pygame.quit()
                    quit()

                if action == "controls":
                    game_controls()

                if action == "play":
                    gameLoop()

                if action == "main":
                    game_intro()

        else:
            pygame.draw.rect(screen, inactive_color, (x, y, width, height))

        text_to_button(text, 'black', x, y, width, height)


    def game_intro():
        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
            screen.fill('black')
            message_to_screen("Welcome to TankArcade2D!", 'red', -100, size="large")
            message_to_screen("Shoot and destroy the enemy tank", 'yellow', 15)
            message_to_screen("before they destroy you.", 'yellow', 60)
            button("Play", 150, 500, 100, 50, 'green', 'yellow', action="play", size="vsmall")
            button("Controls", 350, 500, 100, 50, 'green', 'yellow', action="controls", size="vsmall")
            button("Quit", 550, 500, 100, 50, 'green', 'yellow', action="quit", size="vsmall")
            pygame.display.update()


    class Tank:
        def __init__(self, px, py, angle, vector):
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

            self.hp = 5
            self.shotTimer = 0
            self.shot = False
            self.shotDelay = 60
            self.bulletSpeed = 5
            self.bulletDamage = 1

        def update(self):
            old_position = self.position
            if self.angle_speed != 0:
                # Rotate the direction vector and then the image.
                self.direction.rotate_ip(self.angle_speed)
                self.angle += self.angle_speed
                self.image = pygame.transform.rotate(self.original_image, -self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
            # Update the position vector and the rect.
            self.position += self.direction * self.speed
            self.rect.center = self.position

            if self.shot and self.shotTimer == 0:
                new_position = self.position + self.direction * 10
                Bullet(self, new_position, self.direction, self.bulletDamage, self.bulletSpeed, self.angle)
                self.shotTimer = self.shotDelay
                self.shot = False

            if self.shotTimer > 0:
                self.shotTimer -= 1

            for obj in objects:
                if obj != self and obj.type in 'block' and self.rect.colliderect(obj.rect):
                    self.rect.center = old_position

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
                    if obj != self.parent and obj.rect.collidepoint(self.position):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        break

        def draw(self):
            screen.blit(self.image, self.rect)


    bullets = []
    objects = []
    player1 = Tank(100, 275, 90, 1)
    player2 = Tank(650, 275, -90, -1)
    running = True
    while running:
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
        game_intro()


        for obj in objects:
            obj.update()
        for bullet in bullets:
            bullet.update()

        for obj in objects:
            obj.draw()
        for bullet in bullets:
            bullet.draw()

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
