import pygame
import os
from src.config import *
from src.game_objects import Pipe, Bird
from src.neural_network import decide_action
from src.genetic import EvolutionManager

def desenhar_botao(win, rect, cor_interna):
    pygame.draw.rect(win, (200, 200, 200), rect)
    pygame.draw.rect(win, (0, 0, 0), rect, 2)
    
    tamanho_interno = 40
    center_x = rect.x + (rect.width - tamanho_interno) // 2
    center_y = rect.y + (rect.height - tamanho_interno) // 2
    rect_interno = pygame.Rect(center_x, center_y, tamanho_interno, tamanho_interno)
    
    pygame.draw.rect(win, cor_interna, rect_interno)
    pygame.draw.rect(win, (0, 0, 0), rect_interno, 1)

def tela_selecao(win, font):
    selecionado = False
    cor_escolhida_index = 0
    
    botoes = []
    margem_x = 50
    start_y = 300
    w_btn = 80
    h_btn = 80
    gap = 20
    
    for i, cor in enumerate(CORES_SKIN):
        linha = i // 4
        coluna = i % 4
        x = margem_x + coluna * (w_btn + gap)
        y = start_y + linha * (h_btn + gap)
        rect = pygame.Rect(x, y, w_btn, h_btn)
        botoes.append((rect, cor, i))
        
    while not selecionado:
        win.fill(COR_FUNDO)
        
        texto = font.render("Escolha a Skin da IA", True, WHITE)
        win.blit(texto, (LARGURA_TELA//2 - texto.get_width()//2, 100))
        
        texto_sub = font.render("Clique em uma cor para iniciar", True, (50, 50, 50))
        win.blit(texto_sub, (LARGURA_TELA//2 - texto_sub.get_width()//2, 150))
        
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        for rect, cor, index in botoes:
            desenhar_botao(win, rect, cor)
            
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(win, WHITE, rect, 3)
                if click[0]:
                    cor_escolhida_index = index
                    selecionado = True
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        pygame.display.update()
        
    return cor_escolhida_index

def main():
    pygame.init()
    win = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Flappy IA - Genetic Evolution")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30)
    
    indice_skin = tela_selecao(win, font)
    
    nomes_arquivos = [
        "BirdB.png",
        "BirdC.png",
        "BirdG.png",
        "BirdO.png",
        "BirdPi.png",
        "BirdPu.png",
        "BirdR.png",
        "BirdY.png"
    ]
    
    nome_arquivo = nomes_arquivos[indice_skin]
    caminho_imagem = os.path.join("assets", "Birds", nome_arquivo)
    
    print(f"Iniciando simulação com skin: {nome_arquivo}")
    
    try:
        img = pygame.image.load(caminho_imagem).convert_alpha()
        Bird.IMG = pygame.transform.scale(img, (34, 24))
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
        Bird.IMG = None

    ga = EvolutionManager(pop_size=50)
    birds = ga.create_population()
    saved_birds = []
    
    pipes = [Pipe(600)]
    score = 0
    
    try:
        bg_img = pygame.image.load(os.path.join("assets", "Background.png"))
        bg_img = pygame.transform.scale(bg_img, (LARGURA_TELA, ALTURA_TELA))
    except:
        bg_img = None

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        if len(birds) == 0:
            print(f"Geração {ga.generation} extinta. Evoluindo...")
            birds = ga.next_generation(saved_birds)
            saved_birds = []
            pipes = [Pipe(600)]
            score = 0

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            if pipe.x + pipe.top_rect.width < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < birds[0].x if birds else 0: 
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            bird.fitness += 0.1
            bird.move()
            decide_action(bird, pipes, LARGURA_TELA, ALTURA_TELA)

        for i in range(len(birds) - 1, -1, -1):
            bird = birds[i]
            colidiu = False
            
            for pipe in pipes:
                if pipe.collide(bird):
                    colidiu = True
                    break
            
            if colidiu or not bird.alive:
                bird.fitness -= 1
                saved_birds.append(bird)
                birds.pop(i)

        if bg_img:
            win.blit(bg_img, (0,0))
        else:
            win.fill(COR_FUNDO)

        for pipe in pipes:
            pipe.draw(win)
            
        for bird in birds:
            bird.draw(win)
            
        text_gen = font.render(f"Gen: {ga.generation}", 1, WHITE)
        text_alive = font.render(f"Vivos: {len(birds)}", 1, WHITE)
        text_score = font.render(f"Score: {score}", 1, WHITE)
        
        win.blit(text_gen, (10, 10))
        win.blit(text_alive, (10, 50))
        win.blit(text_score, (10, 90))

        pygame.display.update()

if __name__ == "__main__":
    main()