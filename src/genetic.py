import random
import numpy as np
from src.game_objects import Bird
from src.neural_network import Brain

class EvolutionManager:
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.generation = 0

    def create_population(self):
            birds = []
            for _ in range(self.pop_size):
                b = Bird(230, 350)
                b.brain = Brain(3, 4, 1) 
                birds.append(b)
            return birds
    
    def mutate(self, brain, rate=0.1, scale=0.5):
        def mutate_arr(arr):
            mask = np.random.rand(*arr.shape) < rate
            noise = np.random.normal(0, scale, arr.shape)
            arr[mask] += noise[mask]
            
        mutate_arr(brain.w_ih)
        mutate_arr(brain.w_ho)
        mutate_arr(brain.bias_h)
        mutate_arr(brain.bias_o)