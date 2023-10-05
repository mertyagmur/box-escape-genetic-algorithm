import pygame
from player import Player
import enemy
import math
import random
import numpy as np

pygame.init()
window = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

population_size = 100
players = []

enemy = enemy.Enemy()
generation_count = 0

def create_population():
    global generation_count, population, players
    print(f"Generation {generation_count}")
    if generation_count == 0:
        for i in range(population_size):
            players.append(Player())
        generation_count += 1
    else:
        crossover()
        generation_count += 1
    #alive_times = [player.alive_time for player in players]
    #print(max(alive_times))

def update_players():
    for player in players:
        if player.alive:
            player.draw(window)
            player.alive_time += 1
        if player.check_collision(enemy):
            player.alive = False

def is_all_dead():
    for player in players:
        if player.alive:
            return False
    return True

def crossover():
    global players
    next_gen = []
    sorted_population = sorted(players, key=lambda player: player.alive_time)
    fittest = sorted_population[int(20*population_size/100):]
    alive_times = [fit.alive_time for fit in fittest]
    print(sum(alive_times)/len(alive_times))
    next_gen.extend(fittest)
    for player in next_gen:
        player.alive = True
        player.alive_time = 0
        player.radar = np.random.randn(player.input_size + 2)
    #enemy.x = 50
    #enemy.y = 50

    while len(next_gen) <= population_size:
        parent1 = random.choice(fittest)
        parent2 = random.choice(fittest)

        parent1_weights_input_hidden = parent1.mlp.weights_input_hidden
        parent1_weights_hidden_output = parent1.mlp.weights_hidden_output
        parent2_weights_input_hidden = parent2.mlp.weights_input_hidden
        parent2_weights_hidden_output = parent2.mlp.weights_hidden_output
        child_weights_input_hidden = []
        child_weights_hidden_output = []
        child = Player()

        for w1, w2 in zip(parent1_weights_input_hidden, parent2_weights_input_hidden):
            for i1, i2 in zip(w1, w2):
                prob = random.random()
                if prob < 0.40:
                    child_weights_input_hidden.append(i1)
                elif prob < 0.80:
                    child_weights_input_hidden.append(i2)
                else:
                    child_weights_input_hidden.append(random.uniform(0, 1))

        for W1, W2 in zip(parent1_weights_hidden_output, parent2_weights_hidden_output):
            for I1, I2 in zip(W1, W2):
                prob = random.random()
                if prob < 0.40:
                    child_weights_hidden_output.append(I1)
                elif prob < 0.80:
                    child_weights_hidden_output.append(I2)
                else:
                    child_weights_hidden_output.append(random.uniform(0, 1))
        child.mlp.weights_input_hidden = np.array(child_weights_input_hidden).reshape(4, 16)
        child.mlp.weights_hidden_output = np.array(child_weights_hidden_output).reshape(16, 8)

        next_gen.append(child)
    players = next_gen

create_population()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((0, 0, 64))

    for player in players:
        player.move(enemy)
        player.move_period_counter += 1

        if player.x <= 0 or player.x >= 800 - 30:
            #player.direction = "RIGHT" if player.direction == "LEFT" else "LEFT"
            if player.direction == "RIGHT":
                player.direction = "LEFT"
            elif player.direction == "LEFT":
                player.direction = "RIGHT"
            elif player.direction == "DOWNRIGHT":
                player.direction = "DOWNLEFT"
            elif player.direction == "DOWNLEFT":
                player.direction = "DOWNRIGHT"
            elif player.direction == "UPRIGHT":
                player.direction = "UPLEFT"
            elif player.direction == "UPLEFT":
                player.direction = "UPRIGHT"
        if player.y <= 0 or player.y >= 800 - 30:
            #player.direction = "DOWN" if player.direction == "UP" else "UP"
            #player.direction = "DOWNLEFT" if player.direction == "DOWNRIGHT" else "DOWNRIGHT"
            #player.direction = "UPLEFT" if player.direction == "UPRIGHT" else "UPRIGHT"
            if player.direction == "UP":
                player.direction = "DOWN"
            elif player.direction == "DOWN":
                player.direction = "UP"
            elif player.direction == "DOWNRIGHT":
                player.direction = "UPRIGHT"
            elif player.direction == "DOWNLEFT":
                player.direction = "UPLEFT"
            elif player.direction == "UPRIGHT":
                player.direction = "DOWNRIGHT"
            elif player.direction == "UPLEFT":
                player.direction = "DOWNLEFT"

    closest_player = None
    min_distance = 999999
    for player in players:
        if player.alive:
            distance = math.sqrt((enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_player = player
    
    """ dirvect = pygame.math.Vector2((closest_player.x - enemy_x),
                                      closest_player.y - enemy_y)
    dirvect.normalize()
    # Move along this normalized vector towards the player at current speed.
    dirvect.scale_to_length(enemy_velocity)
    enemy_rect.move_ip(dirvect) """

    
    update_players()
    
    if is_all_dead():
        print("All dead!")
        create_population()
    

    enemy.draw(window)
    enemy_dirvect = enemy.get_direction(closest_player)

    enemy.move()
    
    try:
        if enemy.x <= 0 or enemy.x >= 800 - 30:
            enemy_dirvect = -enemy_dirvect
        if enemy.y <= 0 or enemy.y >= 800 - 30:
            enemy_dirvect = -enemy_dirvect
    except:
        pass

    pygame.display.flip()

pygame.quit()
exit() 