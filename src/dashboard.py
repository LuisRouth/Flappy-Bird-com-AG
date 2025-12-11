import pygame
from src.config import *

pygame.font.init()
FONTE_TITULO = pygame.font.SysFont('arial', 18, bold=True)
FONTE_TEXTO = pygame.font.SysFont('arial', 14)
FONTE_DESTAQUE = pygame.font.SysFont('arial', 24, bold=True)

def desenhar_cerebro_simplificado(win, brain, x, y):
    layer_in_x = x + 20
    layer_hid_x = x + 120
    layer_out_x = x + 220 
    y_nodes = [y, y+40, y+80]
    
    labels = ["Y Pássaro", "Dist. Cano", "Y Buraco"]
    
    rows, cols = brain.w_ih.shape
    for i in range(rows):
        for h in range(cols):
            weight = brain.w_ih[i][h]
            cor = VERDE_NEON if weight > 0 else VERMELHO_NEON
            width = 1 if abs(weight) < 0.5 else 2 
            pygame.draw.line(win, cor, (layer_in_x, y_nodes[i]), (layer_hid_x, y + 20 + (h * 20)), width)

    rows, cols = brain.w_ho.shape
    for h in range(rows):
        weight = brain.w_ho[h][0]
        cor = VERDE_NEON if weight > 0 else VERMELHO_NEON
        width = 1 if abs(weight) < 0.5 else 3
        pygame.draw.line(win, cor, (layer_hid_x, y + 20 + (h * 20)), (layer_out_x, y + 40), width)

    for i in range(3):
        pygame.draw.circle(win, WHITE, (layer_in_x, y_nodes[i]), 5)
        text = FONTE_TEXTO.render(labels[i], 1, WHITE)
        win.blit(text, (layer_in_x, y_nodes[i] - 18))

    pygame.draw.circle(win, WHITE, (layer_out_x, y + 40), 8)
    win.blit(FONTE_TITULO.render("PULAR", 1, WHITE), (layer_out_x + 15, y + 30))

def draw_dashboard(win, bird, generation, alive_count, score, recorde, velocidade, music_on):
    rect_painel = pygame.Rect(LARGURA_TELA, 0, LARGURA_PAINEL, ALTURA_TELA)
    pygame.draw.rect(win, COR_PAINEL, rect_painel)
    pygame.draw.line(win, WHITE, (LARGURA_TELA, 0), (LARGURA_TELA, ALTURA_TELA), 2)
    
    base_x = LARGURA_TELA + 20
    cursor_y = 20
    win.blit(FONTE_TITULO.render("ESTATÍSTICAS", 1, AZUL_CLARO), (base_x + 50, cursor_y))
    cursor_y += 40
    
    win.blit(FONTE_TEXTO.render(f"Geração: {generation}", 1, WHITE), (base_x, cursor_y))
    cursor_y += 25
    win.blit(FONTE_TEXTO.render(f"Vivos: {alive_count}", 1, WHITE), (base_x, cursor_y))
    cursor_y += 25
    win.blit(FONTE_DESTAQUE.render(f"Pontos: {score}", 1, WHITE), (base_x, cursor_y))
    cursor_y += 30
    win.blit(FONTE_TITULO.render(f"Recorde: {recorde}", 1, AMARELO), (base_x, cursor_y))
    cursor_y += 30
    win.blit(FONTE_TEXTO.render(f"Velocidade: {velocidade:.1f}", 1, AZUL_CLARO), (base_x, cursor_y))
    cursor_y += 40
    
    if bird:
        win.blit(FONTE_TITULO.render("REDE NEURAL (LÍDER)", 1, AMARELO), (base_x + 40, cursor_y))
        cursor_y += 40
        desenhar_cerebro_simplificado(win, bird.brain, base_x, cursor_y)
        cursor_y += 150 
        
        win.blit(FONTE_TEXTO.render("INTENÇÃO:", 1, WHITE), (base_x, cursor_y))
        cursor_y += 20
        
        bar_width = 200
        mid_x = base_x + 30 + (bar_width // 2)
        pygame.draw.rect(win, (70,70,70), (base_x + 30, cursor_y, bar_width, 20))
        pygame.draw.line(win, WHITE, (mid_x, cursor_y-5), (mid_x, cursor_y+25), 2)
        
        decision = bird.brain.last_output
        fill_w = min(abs(decision) * (bar_width//2), bar_width//2)
        
        if decision > 0.5:
            pygame.draw.rect(win, VERDE_NEON, (mid_x, cursor_y+2, fill_w, 16))
        else:
            pygame.draw.rect(win, VERMELHO_NEON, (mid_x-fill_w, cursor_y+2, fill_w, 16))

    y_music = ALTURA_TELA - 130
    rect_music = pygame.Rect(base_x + 30, y_music, LARGURA_PAINEL - 80, 40)
    
    cor_btn = VERDE_NEON if music_on else VERMELHO_NEON
    texto_btn = "MÚSICA: ON" if music_on else "MÚSICA: OFF"
    
    pygame.draw.rect(win, cor_btn, rect_music)
    pygame.draw.rect(win, WHITE, rect_music, 2)
    
    lbl = FONTE_TITULO.render(texto_btn, 1, (0,0,0))
    win.blit(lbl, (rect_music.centerx - lbl.get_width()//2, rect_music.centery - lbl.get_height()//2))
    y_inst = ALTURA_TELA - 60
    pygame.draw.rect(win, (0,0,0), (base_x, y_inst - 5, LARGURA_PAINEL-20, 50)) 
    
    instrucao_1 = FONTE_TITULO.render("[K] MATAR TODOS", 1, VERMELHO_NEON)
    win.blit(instrucao_1, (base_x + 30, y_inst))
    instrucao_2 = FONTE_TEXTO.render("(Pula para próxima geração)", 1, WHITE)
    win.blit(instrucao_2, (base_x + 30, y_inst + 25))
    return rect_music