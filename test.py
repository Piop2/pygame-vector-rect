import pygame

from vrect import VRect

pygame.init()
surf = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Vector Rect test")
clock = pygame.time.Clock()

vrect = VRect(250, 250, 100, 100)

dot = (250, 190)

running = True
while running:
    clock.tick(60)

    surf.fill("black")
    vrect.draw(surf, "white", 0, True) if not vrect.collidepoint(*dot) else vrect.draw(
        surf, "green", 0, True
    )

    pygame.draw.circle(surf, "red", dot, 5)

    vrect.a += 0.5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
