import pygame
from src.config import *

pygame.font.init()
FONTE_TITULO = pygame.font.SysFont('arial', 18, bold=True)
FONTE_TEXTO = pygame.font.SysFont('arial', 14)
FONTE_DESTAQUE = pygame.font.SysFont('arial', 24, bold=True)
CINZA_FUNDO = (40, 40, 40)
CINZA_CLARO = (70, 70, 70)
VERDE_ACESO = (50, 255, 50)
VERMELHO_ACESO = (255, 50, 50)
BRANCO = (255, 255, 255)
AMARELO = (255, 220, 0)

def desenhar_cerebro_simplificado(win, brain, x, y):
    layer_in_x = x + 20
    layer_hid_x = x + 120
    layer_out_x = x + 220
    y_nodes = [y, y+40, y+80]
    labels = ["Altura Pássaro", "Dist. Cano", "Altura Buraco"]
    
    rows, cols = brain.w_ih.shape
    for i in range(rows):
        for h in range(cols):
            weight = brain.w_ih[i][h]
            cor = VERDE_ACESO if weight > 0 else VERMELHO_ACESO
            espessura = 1 if abs(weight) < 0.5 else 2 
            start = (layer_in_x, y_nodes[i])
            end = (layer_hid_x, y + 20 + (h * 20))
            pygame.draw.line(win, cor, start, end, espessura)

    rows, cols = brain.w_ho.shape
    for h in range(rows):
        weight = brain.w_ho[h][0]
        cor = VERDE_ACESO if weight > 0 else VERMELHO_ACESO
        espessura = 1 if abs(weight) < 0.5 else 3
        start = (layer_hid_x, y + 20 + (h * 20))
        end = (layer_out_x, y + 40)
        pygame.draw.line(win, cor, start, end, espessura)
    for i in range(3):
        pygame.draw.circle(win, BRANCO, (layer_in_x, y_nodes[i]), 5)
        text = FONTE_TEXTO.render(labels[i], 1, BRANCO)
        win.blit(text, (layer_in_x, y_nodes[i] - 18))

    pygame.draw.circle(win, WHITE, (layer_out_x, y + 40), 8)
    lbl_pula = FONTE_TITULO.render("PULAR?", 1, WHITE)
    win.blit(lbl_pula, (layer_out_x + 15, y + 30))

def draw_dashboard(win, bird, generation, alive_count, score):
    rect_painel = pygame.Rect(LARGURA_TELA, 0, LARGURA_PAINEL, ALTURA_TELA)
    pygame.draw.rect(win, CINZA_FUNDO, rect_painel)
    pygame.draw.line(win, WHITE, (LARGURA_TELA, 0), (LARGURA_TELA, ALTURA_TELA), 2)
    
    base_x = LARGURA_TELA + 20
    cursor_y = 30
    win.blit(FONTE_TITULO.render("ESTATÍSTICAS", 1, AMARELO), (base_x + 70, cursor_y))
    cursor_y += 40
    
    win.blit(FONTE_TEXTO.render(f"Geração Atual: {generation}", 1, WHITE), (base_x, cursor_y))
    cursor_y += 25
    win.blit(FONTE_TEXTO.render(f"Vivos: {alive_count}", 1, WHITE), (base_x, cursor_y))
    cursor_y += 25
    win.blit(FONTE_DESTAQUE.render(f"Pontos: {score}", 1, WHITE), (base_x, cursor_y))
    
    cursor_y += 50
    if bird:
        win.blit(FONTE_TITULO.render("O CÉREBRO (LÍDER)", 1, AMARELO), (base_x + 50, cursor_y))
        cursor_y += 40
        desenhar_cerebro_simplificado(win, bird.brain, base_x, cursor_y)
        
        cursor_y += 150
        win.blit(FONTE_TEXTO.render("INTENÇÃO DE PULO:", 1, WHITE), (base_x, cursor_y))
        cursor_y += 25
        bar_width = 200
        bar_height = 30
        rect_bar = pygame.Rect(base_x + 30, cursor_y, bar_width, bar_height)
        pygame.draw.rect(win, CINZA_CLARO, rect_bar)
        mid_x = base_x + 30 + (bar_width // 2)
        pygame.draw.line(win, WHITE, (mid_x, cursor_y - 5), (mid_x, cursor_y + bar_height + 5), 2)
        decision = bird.brain.last_output
        fill_width = abs(decision) * (bar_width // 2)
        fill_width = min(fill_width, bar_width // 2)
        
        if decision > 0.5:
            rect_fill = pygame.Rect(mid_x, cursor_y + 5, fill_width, bar_height - 10)
            pygame.draw.rect(win, VERDE_ACESO, rect_fill)
            win.blit(FONTE_TITULO.render("SIM!", 1, VERDE_ACESO), (mid_x + 10, cursor_y + 5))
        else:
            rect_fill = pygame.Rect(mid_x - fill_width, cursor_y + 5, fill_width, bar_height - 10)
            pygame.draw.rect(win, VERMELHO_ACESO, rect_fill)
            win.blit(FONTE_TITULO.render("NÃO", 1, VERMELHO_ACESO), (mid_x - 50, cursor_y + 5))