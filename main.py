import pygame

from vrect import VRect

pygame.init()
surf = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Vector Rect test")
clock = pygame.time.Clock()

vrect = VRect(250, 250, 100, 100, 45)

dot = [250, 0]


running = True
while running:
    clock.tick(60)

    surf.fill("white")
    vrect.draw(surf, "black")
    pygame.draw.circle(surf, "red", dot, 5)

    dot[1] += 1

    print(vrect.collidepoint(*dot), dot)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
