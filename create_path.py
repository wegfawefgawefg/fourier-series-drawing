'''
basic pygame setup

we want to draw the path of the mouse

then store all the coordinates in a list in json
'''
import pygame
import json
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    running = True
    path = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                path.append(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        # screen.fill((0, 0, 0))
        for p in path:
            pygame.draw.circle(screen, (255, 0, 0), p, 3)

        # connect points with lines
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (255, 255, 255), path[i], path[i + 1])
        pygame.display.flip()
        clock.tick(60)
    with open('path.json', 'w') as f:
        json.dump(path, f)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()