import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('TankArcade2D')
    size = width, height = 800, 400
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    clock = pygame.time.Clock()

    FPS = 60
    TILE = 32
    DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


    class Tank:
        def __init__(self, color, px, py, direct, keyList):
            objects.append(self)
            self.type = 'tank'

            self.color = color
            self.rect = pygame.Rect(px, py, TILE, TILE)
            self.direct = direct
            self.moveSpeed = 2

            self.keyLEFT = keyList[0]
            self.keyRIGHT = keyList[1]
            self.keyUP = keyList[2]
            self.keyDOWN = keyList[3]
            self.keySHOT = keyList[4]

        def update(self):
            if keys[self.keyLEFT]:
                self.rect.x -= self.moveSpeed
                self.direct = 3
            elif keys[self.keyRIGHT]:
                self.rect.x += self.moveSpeed
                self.direct = 1
            elif keys[self.keyUP]:
                self.rect.y -= self.moveSpeed
                self.direct = 0
            elif keys[self.keyDOWN]:
                self.rect.y += self.moveSpeed
                self.direct = 2

        def draw(self):
            pygame.draw.rect(screen, self.color, self.rect)

            x = self.rect.centerx + DIRECTS[self.direct][0] * 30
            y = self.rect.centery + DIRECTS[self.direct][1] * 30
            pygame.draw.line(screen, 'white', self.rect.center, (x, y), 4)


    objects = []
    Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
    Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        for obj in objects:
            obj.update()

        screen.fill('black')
        for obj in objects:
            obj.draw()

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
