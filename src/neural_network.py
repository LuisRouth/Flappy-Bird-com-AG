import numpy as np

class Brain:
    """Implementação do Grafo Neural (Perceptron Multicamadas)"""
    def __init__(self, n_inputs, n_hidden, n_output):
        # Inicialização dos pesos (arestas do grafo)
        self.w_ih = np.random.uniform(-1, 1, (n_inputs, n_hidden)) # Input -> Hidden
        self.w_ho = np.random.uniform(-1, 1, (n_hidden, n_output)) # Hidden -> Output
        self.bias_h = np.random.uniform(-1, 1, (1, n_hidden))
        self.bias_o = np.random.uniform(-1, 1, (1, n_output))

    def feed_forward(self, inputs):
        """Processamento do sinal através do grafo"""
        inputs = np.array(inputs).reshape(1, -1)
        
        # Camada Oculta
        hidden = np.tanh(np.dot(inputs, self.w_ih) + self.bias_h)
        
        # Camada de Saída
        output = np.tanh(np.dot(hidden, self.w_ho) + self.bias_o)
        
        return output[0][0]

def decide_action(bird, pipes, screen_width, screen_height):
    """Lógica que conecta o sensor (jogo) ao cérebro (grafo)"""
    # 1. Achar o próximo cano
    closest_pipe = None
    closest_dist = float('inf')
    for pipe in pipes:
        dist = pipe.x + 70 - bird.x
        if 0 < dist < closest_dist:
            closest_pipe = pipe
            closest_dist = dist
            
    if closest_pipe and bird.brain:
        # 2. Criar inputs normalizados
        inputs = [
            bird.y / screen_height,
            closest_dist / screen_width,
            closest_pipe.height / screen_height
        ]
        
        # 3. Consultar o grafo
        prediction = bird.brain.feed_forward(inputs)
        
        # 4. Agir
        if prediction > 0.5:
            bird.jump()