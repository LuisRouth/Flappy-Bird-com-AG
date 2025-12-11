import random
import numpy as np
from src.game_objects import Bird
from src.neural_network import Brain
from src.config import TAMANHO_POPULACAO

class EvolutionManager:
    def __init__(self, pop_size=TAMANHO_POPULACAO):
        self.pop_size = pop_size
        self.generation = 0

    def create_population(self):
            birds = []
            for _ in range(self.pop_size):
                b = Bird(230, 350)
                b.brain = Brain(5, 5, 1) 
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
    
    def next_generation(self, birds):
        self.generation += 1
        birds.sort(key=lambda x: x.fitness, reverse=True)
        
        new_birds = []
        
        for i in range(2):
            if i < len(birds):
                best = Bird(230, 350)
                best.brain = Brain(5, 5, 1)
                best.brain.w_ih = birds[i].brain.w_ih.copy()
                best.brain.w_ho = birds[i].brain.w_ho.copy()
                best.brain.bias_h = birds[i].brain.bias_h.copy()
                best.brain.bias_o = birds[i].brain.bias_o.copy()
                new_birds.append(best)
        
        while len(new_birds) < self.pop_size:
            limit = min(10, len(birds))
            if limit > 0:
                parent = random.choice(birds[:limit])
                child = Bird(230, 350)
                child.brain = Brain(5, 5, 1)
                
                child.brain.w_ih = parent.brain.w_ih.copy()
                child.brain.w_ho = parent.brain.w_ho.copy()
                child.brain.bias_h = parent.brain.bias_h.copy()
                child.brain.bias_o = parent.brain.bias_o.copy()
                
                self.mutate(child.brain)
                new_birds.append(child)
            else:
                b = Bird(230, 350)
                b.brain = Brain(5, 5, 1)
                new_birds.append(b)
            
        return new_birds