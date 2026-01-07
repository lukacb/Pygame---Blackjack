import pygame
import sys
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

# --- 2. CLASSES E LÓGICA ---
class Carta:
    def __init__(self, naipe, valor_nome, valor_real):
        self.naipe = naipe
        self.valor_nome = valor_nome
        self.valor_real = valor_real  

    def __str__(self):
        return f"{self.valor_nome} de {self.naipe}"

def criar_baralho():
    naipes = ["Copas", "Espadas", "Ouros", "Paus"]
    valores = {
        "Ás": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, 
        "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10
    }
    
    baralho = []
    for naipe in naipes:
        for nome, valor in valores.items():
            baralho.append(Carta(naipe, nome, valor))
    
    random.shuffle(baralho)
    return baralho

def calcular_pontuacao(mao):
    pontos = sum(carta.valor_real for carta in mao)
    
    # Se passou de 21 e tem um Ás (que vale 11), transforma em 1
    as_no_jogo = sum(1 for carta in mao if carta.valor_nome == "Ás")
    
    while pontos > 21 and as_no_jogo > 0:
        pontos -= 10
        as_no_jogo -= 1
        
    return pontos

# Estado inicial do jogo
baralho = criar_baralho()

# Mãos dos jogadores
mao_jogador1 = [baralho.pop(), baralho.pop()]
mao_jogador2 = [baralho.pop(), baralho.pop()]
mao_banca = [baralho.pop(), baralho.pop()]

# Exemplo de como checar os pontos
print(f"Jogador 1: {calcular_pontuacao(mao_jogador1)} pontos")
print(f"Banca: {calcular_pontuacao(mao_banca)} pontos")

# --- 3. FUNÇÕES DE APOIO VISUAL ---
def desenhar_texto(texto, fonte, cor, x, y):
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x - img.get_width() // 2, y))

# --- 4. FUNÇÕES DE CADA TELA ---
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