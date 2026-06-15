import math
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lunar Lander")

clock = pygame.time.Clock()
running = True

particles = []
particle_timer = 0


class LunarLander:
    def __init__(self):
        self.lander = pygame.image.load("img/lander2.png").convert_alpha()
        self.lander.set_colorkey((255, 255, 255))

        self.lander_rect = self.lander.get_rect()

        self.set_coordinates()

        self.x = self.lander_rect.centerx
        self.y = self.lander_rect.centery

        self.vx = 0
        self.vy = 0

        self.angle = 0

    def set_coordinates(self):
        x_rand = random.randint(30, 770)
        self.lander_rect.center = (x_rand, -10)


lander = LunarLander()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        lander.angle += 3

    if keys[pygame.K_RIGHT]:
        lander.angle -= 3

    lander.vy += 0.05

    thrust = keys[pygame.K_UP]

    if thrust:
        a = math.radians(lander.angle)

        power = 0.1

        lander.vx += math.sin(a) * power
        lander.vy -= math.cos(a) * power

    lander.x += lander.vx
    lander.y += lander.vy

    lander.lander_rect.center = (
        int(lander.x),
        int(lander.y)
    )

    screen.fill("black")

    line = [
        [0, 500], [10, 490], [20, 510], [30, 520],
        [50, 550], [70, 500], [100, 400], [120, 380], [130, 400],
        [150, 550], [200, 585], [210, 580], [220, 570],
        [230, 560], [250, 550], [260, 500], [300, 400], [310, 380], [320, 350],
        [340, 320], [360, 300], [380, 320], [390, 310], [400, 310], [420, 280],
        [450, 300], [455, 340], [460, 360], [470, 380], [480, 400], [490, 420],
        [500, 460], [520, 500], [540, 480], [560, 470], [580, 490], [600, 500],
        [650, 500], [660, 490], [670, 450], [690, 400], [730, 380], [760, 370],
        [780, 340], [799, 300]
    ]

    fill = line + [[800, 600], [0, 600]]

    pygame.draw.line(screen, (255, 0, 0), [560, 490], [700, 490], 15)
    pygame.draw.polygon(screen, "white", fill)

    pygame.draw.lines(
        screen,
        "white",
        False,
        line,
        6
    )

    particle_timer += 1

    if thrust and particle_timer > 2:
        particle_timer = 0

        a = math.radians(lander.angle)

        particles.append([
            lander.lander_rect.centerx - math.sin(a) * 25,
            lander.lander_rect.centery + math.cos(a) * 25,

            -math.sin(a) * random.randint(4, 8),
            math.cos(a) * random.randint(4, 8),

            4
        ])

    for particle in particles[:]:

        particle[0] += particle[2]
        particle[1] += particle[3]

        particle[4] -= 0.15

        pygame.draw.circle(
            screen,
            "red",
            (int(particle[0]), int(particle[1])),
            max(1, int(particle[4]))
        )

        if particle[4] <= 0:
            particles.remove(particle)

    terrain_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
    pygame.draw.polygon(terrain_surface, "white", fill)

    terrain_mask = pygame.mask.from_surface(terrain_surface)
    lander_mask = pygame.mask.from_surface(lander.lander)

    offset = (
        lander.lander_rect.x,
        lander.lander_rect.y
    )

    if (
        terrain_mask.overlap(lander_mask, offset)
        or lander.lander_rect.right < 0
        or lander.lander_rect.left > 800
        or lander.lander_rect.bottom < 0
        or lander.lander_rect.top > 600
    ):

        lander.set_coordinates()

        lander.x = lander.lander_rect.centerx
        lander.y = lander.lander_rect.centery

        lander.vx = 0
        lander.vy = 0
        lander.angle = 0

    rotated_lander = pygame.transform.rotate(
        lander.lander,
        lander.angle
    )

    rotated_lander.set_colorkey((255, 255, 255))

    new_rect = rotated_lander.get_rect(
        center=lander.lander_rect.center
    )

    screen.blit(rotated_lander, new_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()