import pygame
import random
import numpy as np

WIDTH, HEIGHT = 800, 600
OBJECT_COUNT = 10
SPAWN_INTERVAL = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
frame_count = 0

class Asteroid:
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx, self.vy = velocity
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx = -self.vx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy = -self.vy
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def collide(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = np.hypot(dx, dy)
        if distance < self.radius + other.radius:
            self.on_collision(other)
            other.on_collision(self)
    
    def on_collision(self, other):
        self.vx, self.vy = -self.vx, -self.vy

class Comet(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, 15, (255, 255, 255), (random.uniform(-3, 3), random.uniform(-3, 3)))
        self.trail = []
    
    def move(self):
        super().move()
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:
            self.trail.pop(0)
    
    def draw(self, screen):
        for i, pos in enumerate(self.trail):
            pygame.draw.circle(screen, (200, 200, 200), (int(pos[0]), int(pos[1])), max(1, self.radius - i))
        super().draw(screen)
    
    def on_collision(self, other):
        self.vx *= 1.05
        self.vy *= 1.05

class BlackHole(Asteroid):
    def __init__(self, x, y):
        super().__init__(x, y, 25, (0, 0, 0), (0, 0))
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (50, 50, 50), (int(self.x), int(self.y)), self.radius + 10, 2)
    
    def on_collision(self, other):
        other.radius -= 2
        if other.radius <= 5:
            if other in objects:
                objects.remove(other)

objects = []
def spawn_object(black_holes_spawned=False):
    if not black_holes_spawned:
        obj_type = random.choice([Asteroid, Comet])
    else:
        obj_type = random.choice([Asteroid, Comet])
    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
    if obj_type == Asteroid:
        obj = Asteroid(x, y, 20, (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                       (random.uniform(-3, 3), random.uniform(-3, 3)))
    else:
        obj = obj_type(x, y)
    objects.append(obj)

for _ in range(7):
    x, y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
    objects.append(BlackHole(x, y))

for _ in range(OBJECT_COUNT):
    spawn_object(black_holes_spawned=True)

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    frame_count += 1
    if frame_count % SPAWN_INTERVAL == 0:
        spawn_object(black_holes_spawned=True)
    for i in range(len(objects) - 1, -1, -1):
        obj = objects[i]
        obj.move()
        for j in range(i + 1, len(objects)):
            if j < len(objects):
                obj.collide(objects[j])
        obj.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
