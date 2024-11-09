import pygame
import math

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.circles = []

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos_x, pos_y = pygame.mouse.get_pos()
                    radius = 10  # Set a fixed radius
                    circle = Circle(self.screen, radius, pos_x, pos_y)
                    self.circles.append(circle)

            self.screen.fill((0, 0, 0))  # Clear the screen

            # Update and draw all circles
            for circle in self.circles: 
                circle.gravity(self.screen)
            if self.circles:
                self.circles[-1].text(self.screen)

            # Check for circle collisions and prevent intersection
            for i in range(len(self.circles)):
                for j in range(i + 1, len(self.circles)):  # Only check each pair once
                    dx = self.circles[i].x - self.circles[j].x
                    dy = self.circles[i].y - self.circles[j].y
                    distance = math.hypot(dx, dy)
                    min_distance = self.circles[i].r + self.circles[j].r

                    # Check for collision
                    if distance < min_distance and distance != 0:  # Prevent division by zero
                        overlap = min_distance - distance
                        angle = math.atan2(dy, dx)

                        # Move circles apart by half the overlap distance
                        self.circles[i].x += math.cos(angle) * (overlap / 2)
                        self.circles[i].y += math.sin(angle) * (overlap / 2)
                        self.circles[j].x -= math.cos(angle) * (overlap / 2)
                        self.circles[j].y -= math.sin(angle) * (overlap / 2)

                        # Apply repulsive velocity to keep them moving apart
                        force = 0.5 * (min_distance - distance)
                        self.circles[i].velx += math.cos(angle) * force
                        self.circles[i].velocity += math.sin(angle) * force
                        self.circles[j].velx -= math.cos(angle) * force
                        self.circles[j].velocity -= math.sin(angle) * force

            pygame.display.flip()
            self.clock.tick(30)

class Circle:
    def __init__(self, screen, r, x, y):
        self.r = r
        self.x = x
        self.y = y
        self.screen = screen
        self.velocity = 0
        self.velx = 0

    def gravity(self, screen):
        if abs(self.velocity) > 0 or self.y < SCREEN_HEIGHT - self.r:
            self.velocity += 1  
        
        self.y += self.velocity
        self.x += self.velx
        # Round velocity to avoid very small bounces
        if abs(self.velocity) < 0.44:
            self.velocity = 0

        # Check if the object hits the ground
        if self.y >= SCREEN_HEIGHT - self.r :  
            self.y = SCREEN_HEIGHT - self.r  
            self.velocity = -self.velocity * 0.8  
        if self.x>= SCREEN_WIDTH - self.r :  
            self.x = SCREEN_WIDTH - self.r 
            self.velx = -self.velx*0.8  
        if self.x<= self.r:
            self.x = self.r  
            self.velx = -self.velx*1.2
        # Draw the circle
        pygame.draw.circle(surface=screen, center=[self.x, self.y], radius=self.r, color=(255, 255, 255), width=1)

    def text(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 28)
        string = f'Velocity: {self.velocity:.2f}'
        text = font.render(string, True, (255, 255, 255))
        textRect = text.get_rect(topleft=(100, 130))
        screen.blit(text, textRect)

if __name__ == "__main__":
    game = Game()
    game.run()
