'''
take in a list of points in json
draw the path
'''

from pprint import pprint
import random
import pygame
import json

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    paths = []
    for fp in ["path", "tpath"]:
        with open(fp + ".json") as f:
            path = json.load(f)
        paths.append(path)
    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(len(paths))]

    pprint(paths)
    print("len(paths):", len(paths))
    for p in paths:
        print("len(p):", len(p))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        screen.fill((0, 0, 0))

        for i, path in enumerate(paths):
            for j in range(len(path) - 1):
                pygame.draw.line(screen, colors[i], path[j], path[j + 1])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()