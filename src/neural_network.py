import numpy as np

class Brain:
    """Implementação do Grafo Neural (Perceptron Multicamadas)"""
    def __init__(self, n_inputs, n_hidden, n_output):
        # Inicialização dos pesos (arestas do grafo)
        self.w_ih = np.random.uniform(-1, 1, (n_inputs, n_hidden)) # Input -> Hidden
        self.w_ho = np.random.uniform(-1, 1, (n_hidden, n_output)) # Hidden -> Output
        self.bias_h = np.random.uniform(-1, 1, (1, n_hidden))
        self.bias_o = np.random.uniform(-1, 1, (1, n_output))

