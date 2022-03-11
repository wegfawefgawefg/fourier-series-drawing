'''
basic pygame setup

we are making a fourier drawer 
given a list of pairs
where each pair is circle size, and speed

each circle will spin, but stay stationary
each subsequent circle will be attached to the previous one at the spinning point
when all the circles are stacked together, the circles will be connected, and a picture will be drawn by the path 
traced by the spinning point on the last circle
'''
import math
import random
import pygame
import json
import sys

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class Circle:
    def __init__(self, size, rotation_speed, angle):
        self.size = size
        self.rotation_speed = rotation_speed
        self.angle = angle

    def get_end_point(self, pos):
        x = pos[0] + self.size * math.cos(self.angle)
        y = pos[1] + self.size * math.sin(self.angle)
        return (x, y)

    def draw(self, screen, pos):
        pygame.draw.circle(screen, (255, 0, 0), pos, self.size, 1)
        pygame.draw.line(screen, (255, 255, 255), pos, self.get_end_point(pos))

    def update(self, speed = 0.1):
        self.angle += speed * self.rotation_speed

def main():
    pygame.init()

    font = pygame.font.SysFont("monospace", 15)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    center = [0.5 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGHT]

    base_paths = []
    fps = ["path", "tpath"][1:]
    for fp in fps:
        with open(fp + ".json") as f:
            base_path = json.load(f)
        base_paths.append(base_path)
    colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(len(base_paths))]


    # size = 0.1 * SCREEN_WIDTH
    # rotation_speed = 0.1
    # num_circles = 10
    # circles = []
    # for _ in range(num_circles):
    #     circles.append(Circle(size, rotation_speed))
    #     size *= 0.5
    #     rotation_speed *= 0.5

    # import fourier_series.json
    with open('fourier_series.json') as f:
        data = json.load(f)

    sizes = data['magnitudes']
    angles = data['angles']
    rotation_speeds = data['rotation_speeds']
    middle = data['center']

    circles = []
    num_circles = len(sizes)
    for i in range(num_circles):
        circle = Circle(
            size=sizes[i],
            rotation_speed=rotation_speeds[i],
            angle=angles[i]
        )
        circles.append(circle)

    spin_speed = 0.05
    spin_speed_d = spin_speed / 50.0

    path = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        # is up pressed
        if pygame.key.get_pressed()[pygame.K_UP]:
            spin_speed += spin_speed_d
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            spin_speed -= spin_speed_d
        screen.fill((0, 0, 0))

        end_position = middle
        for i, circle in enumerate(circles):
            # draw clear circles with outlines
            circle.draw(screen, end_position)

            end_position = circle.get_end_point(end_position)
            if i == len(circles) - 1:
                path.append(end_position)

        for i in range(len(path) - 1):
            pygame.draw.line(screen, (255, 255, 255), path[i], path[i + 1])

        for i, base_path in enumerate(base_paths):
            for j in range(len(base_path) - 1):
                pygame.draw.line(screen, colors[i], base_path[j], base_path[j + 1])

        for circle in circles:
            circle.update(spin_speed)

        text = font.render(f"spin speed: {spin_speed}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()