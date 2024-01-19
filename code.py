import pygame
from pygame.math import Vector2

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('TankArcade2D')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    clock = pygame.time.Clock()
    tank_image = pygame.image.load('images/tank.png')
    bullet_image = pygame.image.load('images/bullet.png')
    bullet_image = pygame.transform.scale(bullet_image, (10, 15))

    FPS = 60
    TILE = 32


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
                if event.key == pygame.K_KP_ENTER:
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

        for obj in objects:
            obj.update()
        for bullet in bullets:
            bullet.update()

        screen.fill('black')
        for obj in objects:
            obj.draw()
        for bullet in bullets:
            bullet.draw()

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
