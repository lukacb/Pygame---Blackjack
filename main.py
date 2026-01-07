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

def jogar():
    baralho = criar_baralho()
    
    # Mãos iniciais (cada um começa com 2 cartas)
    mao_j1 = [baralho.pop(), baralho.pop()]
    mao_j2 = [baralho.pop(), baralho.pop()]
    mao_banca = [baralho.pop(), baralho.pop()]
    
    turno = 0  # 0: J1, 1: J2, 2: Banca
    mensagens = ["Vez do Jogador 1", "Vez do Jogador 2", "Vez da Banca..."]
    jogo_finalizado = False

    rodando = True
    while rodando:
        tela.fill(VERDE_MESA)
        
        # --- DESENHAR INFORMAÇÕES NA TELA ---
        desenhar_texto(mensagens[turno], fonte_menu, BRANCO, LARGURA // 2, 20)
        
        # Mostrar pontos (Apenas para o que já jogou ou está jogando)
        ponto_j1 = calcular_pontuacao(mao_j1)
        ponto_j2 = calcular_pontuacao(mao_j2)
        ponto_banca = calcular_pontuacao(mao_banca)

        desenhar_texto(f"J1: {ponto_j1}", fonte_menu, BRANCO, 200, 500)
        desenhar_texto(f"J2: {ponto_j2}", fonte_menu, BRANCO, 600, 500)
        
        # Se for o turno da banca, mostramos os pontos dela, senão escondemos
        txt_banca = f"Banca: {ponto_banca}" if turno == 2 else "Banca: ?"
        desenhar_texto(txt_banca, fonte_menu, BRANCO, LARGURA // 2, 150)

        # --- BOTÕES ---
        btn_hit = pygame.Rect(LARGURA // 2 - 110, 400, 100, 50)
        btn_stand = pygame.Rect(LARGURA // 2 + 10, 400, 100, 50)
        
        if turno < 2: # Só mostra botões se for vez de humanos
            pygame.draw.rect(tela, CINZA, btn_hit)
            pygame.draw.rect(tela, CINZA, btn_stand)
            desenhar_texto("HIT", fonte_menu, PRETO, btn_hit.centerx, btn_hit.y + 10)
            desenhar_texto("STOP", fonte_menu, PRETO, btn_stand.centerx, btn_stand.y + 10)

        # --- LÓGICA DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and turno < 2:
                mouse_pos = evento.pos
                
                # Ação PEDIR (HIT)
                if btn_hit.collidepoint(mouse_pos):
                    if turno == 0:
                        mao_j1.append(baralho.pop())
                        if calcular_pontuacao(mao_j1) > 21: turno = 1
                    elif turno == 1:
                        mao_j2.append(baralho.pop())
                        if calcular_pontuacao(mao_j2) > 21: turno = 2

                # Ação PARAR (STAND)
                if btn_stand.collidepoint(mouse_pos):
                    turno += 1

        # --- LÓGICA DA BANCA ---
        if turno == 2 and not jogo_finalizado:
            pygame.display.update()
            pygame.time.delay(1000) # Pausa para a banca jogar
            
            # Regra clássica: Banca para no 17
            if calcular_pontuacao(mao_banca) < 17:
                mao_banca.append(baralho.pop())
            else:
                jogo_finalizado = True
                # Aqui chamar uma função para comparar quem ganhou

        if jogo_finalizado:
            # Lógica para mostrar quem ganhou e voltar ao menu
            # Por enquanto, apenas volta após 3 segundos
            pygame.time.delay(3000)
            return "MENU"

        pygame.display.update()