import math
import pygame

pygame.init()

def dist(p1, p2):
    """Calculate euclidean distance between two points"""
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


class Source:
    """This is our camera which emits rays"""
    def __init__(self, source, start_angle):
        self.source = source
        self.rays = [
            Ray(self.source, start_angle + math.radians(90 + angle * 0.0625))
            for angle in range(640)
        ]

    def illuminate(self, s, walls):
        view = []
        for ray in self.rays:
            view.append(ray.cast(walls))
            ray.show(s)
        return view


# First making a class boundary
class Boundary:
    """Making a boundary by specifying the end points"""
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2

    def show(self, s):
        """
        Displays the boundary, takes screen as an input on which it
        will display the boundary
        """
        pygame.draw.line(s, (255, 111, 105), self.p1, self.p2, 6)


# Make a class ray
class Ray:
    def __init__(self, origin, angle):
        self.p0 = origin
        self.p = (
            self.p0[0] + math.sin(angle) * 25,
            self.p0[1] + math.cos(angle) * 25,
        )

    def show(self, s):
        """
        Displays the boundary, takes screen as an input on which it will
        display the boundary
        """
        pygame.draw.aaline(s, (255, 204, 92), self.p0, self.p, 1)

    def cast(self, walls):
        min_dist = float('inf')
        for wall in walls:
            x1, y1 = wall.p1
            x2, y2 = wall.p2

            x3, y3 = self.p0
            x4, y4 = self.p

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den:
                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
                if 0 < t < 1 and u > 0:
                    temp_pt = [x1 + t * (x2 - x1), y1 + t * (y2 - y1)]
                    if dist(self.p0, temp_pt) < min_dist:
                        min_dist = dist(self.p0, temp_pt)
                        self.p = temp_pt
        return dist(self.p0, self.p)

# Step 1 - Create a screen
scene_h = 500
scene_w = 600
screen = pygame.display.set_mode((scene_w * 2, scene_h))
pygame.display.set_caption('Rendering 2D Raycasting')

# Making a clock instance in pygame
clock = pygame.time.Clock()

# Making the walls
walls = [
    Boundary((0, 0), (scene_w, 0)),
    Boundary((0, scene_h), (scene_w, scene_h)),
    Boundary((scene_w, 0), (scene_w, scene_h)),
    Boundary((0, 0), (0, scene_h)),
    Boundary((0, 200), (100, 200)),
    Boundary((200, 200), (250, 200)),
    Boundary((250, 100), (250, 200)),
    Boundary((250, 100), (400, 100)),
    Boundary((550, 0), (550, 200)),
    Boundary((400, 200), (400, 350)),
    Boundary((400, 350), (600, 350)),
    Boundary((250, 300), (250, 500)),
    Boundary((250, 400), (100, 400)),
]

angle = ang = 0
x = y = 0
x_i = y_i = 40

# This loop is the main loop
run = True
while run:
    # To give the screen a specific color
    screen.fill((0, 0, 0))
    # Display the walls
    for wall in walls:
        wall.show(screen)
    # Making the source
    s1 = Source([x_i, y_i], angle)
    # Length of rays are stored in list views
    views = s1.illuminate(screen, walls)
    # To display the pov of camera
    left = 1200
    top = max(views)
    down = min(views)
    
    for view in views:
        v1 = math.sqrt(math.pow(scene_w, 2) + math.pow(scene_h, 2))
        # Calculate distance to the segment as a proportion of the world size
        distance = view / v1
        # Use the inverse square law to calculate brightness
        brightness = 0.03 / math.pow(distance, 2)
        # Correct for gamma and stop invalid (>255) colors
        brightness = min(1, math.pow(brightness, (1 / 2.2)))
        color = [brightness * u for u in (255, 111, 105)]

        left -= scene_w / len(views)
        height = min(100 / distance, scene_h)
        pygame.draw.rect(
            screen, color,
            (left, (scene_h - height)/ 2, scene_w / len(views), height)
        )

    pygame.draw.circle(screen,  (150, 206, 180), (x_i, y_i), 20)
    face = angle + math.radians(20)
    # This quits the pygame interface when we click X
    # pygame.event.get() returns all the events happening
    # on that particular frame - clicks, pointers, keypress etc.
    for event in pygame.event.get():
        # pygame.QUIT corresponds to the user clicking the X
        if event.type == pygame.QUIT:
            run = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ang = -math.radians(2)
                
            elif event.key == pygame.K_LEFT:
                ang = math.radians(2)
                
            elif event.key == pygame.K_d:
                face += math.radians(90)
                x = - int(3 * math.cos(face))
                y = int(3 * math.sin(face))
                
            elif event.key == pygame.K_a:
                face += math.radians(90)
                x = int(3 * math.cos(face))
                y = - int(3 * math.sin(face))
                
            elif event.key == pygame.K_w:
                x = int(3 * math.cos(face))
                y = - int(3 * math.sin(face))
                
            elif event.key == pygame.K_s:
                x = - int(3 * math.cos(face))
                y = int(3 * math.sin(face))

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s]:
                x = y = 0
                
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                ang = 0

    x_i += x
    y_i += y
    angle += ang

    clock.tick(150)
    pygame.display.update()
    
pygame.display.quit()
