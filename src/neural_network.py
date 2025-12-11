import numpy as np
from src.config import DIST_CANOS

class Brain:
    def __init__(self, n_inputs, n_hidden, n_output):
        self.w_ih = np.random.uniform(-1, 1, (n_inputs, n_hidden))
        self.w_ho = np.random.uniform(-1, 1, (n_hidden, n_output))
        self.bias_h = np.random.uniform(-1, 1, (1, n_hidden))
        self.bias_o = np.random.uniform(-1, 1, (1, n_output))
        self.last_output = 0 

    def feed_forward(self, inputs):
        inputs = np.array(inputs).reshape(1, -1)
        hidden = np.tanh(np.dot(inputs, self.w_ih) + self.bias_h)
        output = np.tanh(np.dot(hidden, self.w_ho) + self.bias_o)
        
        self.last_output = output[0][0]
        return self.last_output

def decide_action(bird, pipes, screen_width, screen_height):
    closest_pipe = None
    closest_dist = float('inf')
    
    for pipe in pipes:
        dist = pipe.x + 70 - bird.x
        if dist > -20 and dist < closest_dist:
            closest_pipe = pipe
            closest_dist = dist
            
    if closest_pipe and bird.brain:
        y_cano_cima = closest_pipe.height 
        y_cano_baixo = closest_pipe.height + DIST_CANOS
        
        inputs = [
            bird.y / screen_height,
            closest_dist / screen_width,
            y_cano_cima / screen_height,
            y_cano_baixo / screen_height,
            bird.vel / 10.0
        ]
        
        prediction = bird.brain.feed_forward(inputs)
        
        if prediction > 0.5:
            bird.jump()
            return True
            
    return False