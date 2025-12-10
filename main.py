import pygame
from src.config import *
from src.game_objects import Pipe
from src.neural_network import decide_action
from src.genetic import EvolutionManager

def main():
    pygame.init()
    win = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Flappy IA - Genetic Algorithm")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30)

    ga = EvolutionManager(pop_size=20)
    birds = ga.create_population()
    saved_birds = []
    
    pipes = [Pipe(600)]
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.top_rect.width < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < 200:
                pipe.passed = True
                add_pipe = True
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        win.fill(COR_FUNDO)
        for pipe in pipes:
            pipe.draw(win) 
        pygame.display.update()

if __name__ == "__main__":
    main()