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

    FPS = 60
    TILE = 32


    class Tank:
        def __init__(self, color, px, py, angle):
            pos = (px, py)
            objects.append(self)
            self.type = 'tank'
            self.image = pygame.transform.rotate(tank_image, -angle)
            self.original_image = self.image

            self.color = color
            self.rect = self.image.get_rect(center=pos)
            self.position = Vector2(pos)
            self.direction = Vector2(-1, 0)
            self.speed = 0
            self.angle_speed = 0
            self.angle = 0

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

            for obj in objects:
                if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                    self.rect.center = old_position

        def draw(self):
            screen.blit(self.image, self.rect)


    objects = []
    player1 = Tank('blue', 100, 275, 90)
    player2 = Tank('red', 650, 275, -90)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
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

        screen.fill('black')
        for obj in objects:
            obj.draw()

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
