import pygame
import random

# Configurações Iniciais
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Blackjack - O 21 do INSPER")

# Cores
VERDE_MESA = (34, 139, 34)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
VERDE_BOTAO = (50, 200, 50)

# Fontes
fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
fonte_menu = pygame.font.SysFont("Arial", 32)

def desenhar_texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x - img.get_width() // 2, y))

def menu_principal():
    rodando = True
    while rodando:
        tela.fill(VERDE_MESA)
        
        # Título
        desenhar_texto("BLACKJACK 21", fonte_titulo, BRANCO, LARGURA // 2, 100)
        
        # Posição dos Botões
        botao_jogar = pygame.Rect(LARGURA // 2 - 100, 250, 200, 50)
        botao_regras = pygame.Rect(LARGURA // 2 - 100, 330, 200, 50)
        botao_sair = pygame.Rect(LARGURA // 2 - 100, 410, 200, 50)

        # Desenhar Botões
        for botao, texto in [(botao_jogar, "JOGAR"), (botao_regras, "REGRAS"), (botao_sair, "SAIR")]:
            pygame.draw.rect(tela, CINZA, botao, border_radius=10)
            desenhar_texto(texto, fonte_menu, PRETO, botao.centerx, botao.y + 10)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if botao_jogar.collidepoint(mouse_pos):
                    return "JOGANDO"
                if botao_regras.collidepoint(mouse_pos):
                    return "REGRAS"
                if botao_sair.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()