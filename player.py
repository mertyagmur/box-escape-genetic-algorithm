import pygame
import random
import math
import mlp
import numpy as np

class Player:
    def __init__(self):
        self.x = 200
        self.y = 200
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.alive = True
        self.velocity = 5
        self.move_amount = 30
        self.possible_directions = ["UP", "DOWN", "LEFT", "RIGHT", "UPLEFT", "UPRIGHT", "DOWNLEFT", "DOWNRIGHT"]
        self.direction = random.choice(self.possible_directions)
        self.move_period = 60
        self.move_period_counter = 0
        self.dirvect = None
        self.alive_time = 0
        

        self.input_size = 4
        self.hidden_size = 16
        self.output_size = 8
        self.radar = np.random.randn(self.input_size + 2)
        self.mlp = mlp.MLP(self.input_size, self.hidden_size, self.output_size)

    def move(self, enemy):
        if self.move_period_counter <= self.move_period:
            if self.direction == "UP":
                #self.y -= self.velocity
                self.dirvect = self.get_dirvect(0, 1)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "DOWN":
                #self.y += self.velocity
                self.dirvect = self.get_dirvect(0, -1)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "LEFT":
                #self.x -= self.velocity
                self.dirvect = self.get_dirvect(-1, 0)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "RIGHT":
                #self.x += self.velocity
                self.dirvect = self.get_dirvect(1, 0)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "UPLEFT":
                #self.x -= self.velocity * math.sqrt(2)
                #self.y += self.velocity * math.sqrt(2)
                self.dirvect = self.get_dirvect(-1, 1)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "UPRIGHT":
                #self.x += self.velocity * math.sqrt(2)
                #self.y += self.velocity * math.sqrt(2)
                self.dirvect = self.get_dirvect(1, 1)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "DOWNLEFT":
                #self.x -= self.velocity * math.sqrt(2)
                #self.y -= self.velocity * math.sqrt(2)
                self.dirvect = self.get_dirvect(-1, -1)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            elif self.direction == "DOWNRIGHT":
                #self.x += self.velocity * math.sqrt(2)
                #self.y -= self.velocity * math.sqrt(2)
                self.dirvect = self.get_dirvect(1, -1)
                self.x += self.dirvect.x * self.velocity
                self.y += self.dirvect.y * self.velocity
            return self.dirvect
        else:
            #self.direction = random.choice(self.possible_directions)
            self.look(enemy)
            self.think()
            self.move_period_counter = 0

    def get_dirvect(self, dx, dy):
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx_normalized = dx / distance
        dy_normalized = dy / distance
        return pygame.Vector2(dx_normalized, dy_normalized)

    def check_collision(self, enemy):
        return pygame.Rect.colliderect(enemy.rect, self.rect)
    
    def look(self, enemy):
        self.radar[0] = enemy.x - self.x
        self.radar[1] = enemy.y - self.y
        self.radar[2] = enemy.dirvect.x
        self.radar[3] = enemy.dirvect.y

    def think(self):
        #input_data = np.random.randn(self.input_size, 1)
        input_data = np.array([self.radar[0], self.radar[1], self.radar[2], self.radar[3]])
        output = self.mlp.forward(input_data)
        direction_decision = self.possible_directions[list(output).index(max(output))]
        self.direction = direction_decision
        
    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        pygame.draw.rect(window, self.color, self.rect)