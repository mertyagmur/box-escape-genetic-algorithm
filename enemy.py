import pygame
import random
import math

class Enemy:
    def __init__(self):
        self.x = 340
        self.y = 340
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        self.color = (255, 0, 0)
        self.velocity = 20
        self.move_period_counter = 0
        self.dirvect = [0, 0]

    def get_direction(self, closest_player):
        dx = closest_player.x - self.x
        dy = closest_player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            dx_normalized = dx / distance
            dy_normalized = dy / distance
            self.dirvect = pygame.Vector2(dx_normalized, dy_normalized)

    def move(self):
        self.x += self.dirvect.x * self.velocity
        self.y += self.dirvect.y * self.velocity

    def reverse_direction(self, dirvect):
        if self.x <= 0 or self.x >= 800 - 200:
            dirvect = -dirvect
        if self.y <= 0 or self.y >= 800 - 200:
            dirvect = -dirvect

    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, 50, 50)
        pygame.draw.rect(window, self.color, self.rect)