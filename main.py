import pygame
import os
from src.config import *
from src.game_objects import Pipe, Bird
from src.neural_network import decide_action
from src.genetic import EvolutionManager
from src.dashboard import draw_dashboard

def desenhar_botao(win, rect, cor_interna):
    pygame.draw.rect(win, (200, 200, 200), rect)
    pygame.draw.rect(win, (0, 0, 0), rect, 2)
    tamanho_interno = 40
    rect_interno = pygame.Rect(rect.x + (rect.width - 40)//2, rect.y + (rect.height - 40)//2, 40, 40)
    pygame.draw.rect(win, cor_interna, rect_interno)
    pygame.draw.rect(win, (0, 0, 0), rect_interno, 1)

def tela_selecao(win, font):
    selecionado = False
    cor_escolhida_index = 0
    botoes = []
    
    for i, cor in enumerate(CORES_SKIN):
        linha, col = i // 4, i % 4
        rect = pygame.Rect(50 + col * 100, 300 + linha * 100, 80, 80)
        botoes.append((rect, cor, i))
        
    while not selecionado:
        win.fill(COR_FUNDO)
        texto = font.render("Escolha a Skin da IA", True, WHITE)
        win.blit(texto, (LARGURA_TELA//2 - texto.get_width()//2, 100))
        
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
            if event.type == pygame.QUIT: pygame.quit(); quit()
        pygame.display.update()
    return cor_escolhida_index

def main():
    pygame.init()
    try: pygame.mixer.init()
    except: pass

    win = pygame.display.set_mode((LARGURA_TOTAL, ALTURA_TELA))
    pygame.display.set_caption("Flappy IA - Genetic Evolution")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 30)
    
    indice_skin = tela_selecao(win, font)
    
    nomes_arquivos = ["BirdB.png", "BirdC.png", "BirdG.png", "BirdO.png", "BirdPi.png", "BirdPu.png", "BirdR.png", "BirdY.png"]
    caminho_imagem = os.path.join("assets", "Birds", nomes_arquivos[indice_skin])
    
    try:
        if os.path.exists("musica.mp3"):
            pygame.mixer.music.load("musica.mp3"); pygame.mixer.music.play(-1); pygame.mixer.music.set_volume(0.5)
        if os.path.exists(caminho_imagem):
            img = pygame.image.load(caminho_imagem).convert_alpha()
            Bird.IMG = pygame.transform.scale(img, (34, 24))
        else: raise FileNotFoundError
    except:
        s = pygame.Surface((34, 24))
        s.fill(CORES_SKIN[indice_skin])
        Bird.IMG = s

    ga = EvolutionManager(pop_size=TAMANHO_POPULACAO)
    birds = ga.create_population()
    saved_birds = []
    pipes = [Pipe(600)]
    score = 0
    velocidade_atual = VEL_CANOS
    recorde_canos = 0
    
    try:
        bg = pygame.image.load(os.path.join("assets", "Background.png")).convert()
        bg = pygame.transform.scale(bg, (LARGURA_TELA, ALTURA_TELA))
    except: bg = None

    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False; pygame.quit(); quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                for b in birds: 
                    b.fitness -= 5
                    saved_birds.append(b)
                birds.clear()

        if len(birds) == 0:
            birds = ga.next_generation(saved_birds)
            saved_birds = []
            pipes = [Pipe(600)]
            score = 0
            velocidade_atual = VEL_CANOS

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move(velocidade_atual)
            if pipe.x + pipe.top_rect.width < 0: rem.append(pipe)
            if not pipe.passed and len(birds) > 0 and (pipe.x + 70) < birds[0].x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            for b in birds:
                b.fitness += 5 
                
            if score > recorde_canos: recorde_canos = score
            velocidade_atual = min(velocidade_atual + 0.5, 15)
            pipes.append(Pipe(600))

        for r in rem: pipes.remove(r)

        for bird in birds:
            bird.fitness += 0.5
            bird.move()
            
            pulou = decide_action(bird, pipes, LARGURA_TELA, ALTURA_TELA)
            
            if pulou:
                bird.fitness -= 0.5 
        
        for i in range(len(birds)-1, -1, -1):
            b = birds[i]
            colidiu = False
            for p in pipes:
                if p.collide(b): colidiu = True; break
            
            if colidiu or not b.alive:
                b.fitness -= 2
                saved_birds.append(b)
                birds.pop(i)

        win.fill(COR_PAINEL)
        if bg: win.blit(bg, (0,0))
        else: pygame.draw.rect(win, COR_FUNDO, (0, 0, LARGURA_TELA, ALTURA_TELA))

        for p in pipes: p.draw(win)
        for b in birds: b.draw(win)
        
        best = birds[0] if birds else None
        draw_dashboard(win, best, ga.generation, len(birds), score, recorde_canos, velocidade_atual)

        pygame.display.update()

if __name__ == "__main__":
    main()