import pygame
import math
import time

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.done = False
        self.circles = []

    def run(self):
        s=0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                s+=10
                (pos_x, pos_y) = pygame.mouse.get_pos()
                if (s!=0):
                    circle = Circle(self.screen, s, pos_x, pos_y)
                    self.circles.append(circle)
                s=0
            self.screen.fill((0, 0, 0))  # Clear the screen
            for circle in self.circles:
                circle.gravity(self.screen)
            if (self.circles):
            	self.circles[-1].text(self.screen)
            pygame.display.flip()
            self.clock.tick(15)

class Circle:
    def __init__(self, screen, r, x, y):
        self.t = 0
        self.r = r
        self.x = x
        self.y = y
        self.dir = 1
        self.screen = screen
        self.velocity = 0

    def gravity(self, screen):
        # Add gravity to velocity if not resting
        if abs(self.velocity) > 0 or self.y < SCREEN_HEIGHT - self.r:
            self.velocity += 9.8  # Gravity accelerates the object downward
        
        self.y += self.velocity
        self.velocity=round(self.velocity,3)
        if (abs(self.velocity)<5):
            self.velocity=0
        # Check if the object hits the ground
        if self.y >= SCREEN_HEIGHT - self.r:  # Hits the bottom of the screen
            self.y = SCREEN_HEIGHT - self.r  # Place the object on the ground
            self.velocity = -self.velocity * 0.8  # Reverse the velocity (bounce) and dampen it (0.8 to reduce bounce height)
            
        
        # Draw the circle
        pygame.draw.circle(surface=screen, center=[self.x, self.y], radius=self.r, color=(255, 255, 255), width=1)

    def text(self, screen):
        self.screen = screen
        width = 28
        font = pygame.font.Font('freesansbold.ttf', width)
        string = f'Velocity: {self.velocity:.2f}'
        pos_x = 100
        pos_y = 130
        text = font.render(string, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (pos_x, pos_y)
        screen.blit(text, textRect)

if __name__ == "__main__":
    game = Game()
    game.run()
