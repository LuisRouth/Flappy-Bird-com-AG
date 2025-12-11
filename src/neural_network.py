import numpy as np

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
        inputs = [
            bird.y / screen_height,
            closest_dist / screen_width,
            closest_pipe.height / screen_height,
        ]
        
        prediction = bird.brain.feed_forward(inputs)
        if prediction > 0.5:
            bird.jump()
            return True
            
    return False