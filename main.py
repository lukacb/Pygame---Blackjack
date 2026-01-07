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

def conferir_resultados(p_j1, p_j2, p_banca):
    resultados = {"j1": "", "j2": ""}
    
    # Lógica para o Jogador 1
    if p_j1 > 21:
        resultados["j1"] = "J1 Estourou! (Perdeu)"
    elif p_banca > 21:
        resultados["j1"] = "J1 Ganhou! (Banca estourou)"
    elif p_j1 > p_banca:
        resultados["j1"] = "J1 Ganhou!"
    elif p_j1 < p_banca:
        resultados["j1"] = "J1 Perdeu!"
    else:
        resultados["j1"] = "J1 Empatou (Push)"

    # Lógica para o Jogador 2
    if p_j2 > 21:
        resultados["j2"] = "J2 Estourou! (Perdeu)"
    elif p_banca > 21:
        resultados["j2"] = "J2 Ganhou! (Banca estourou)"
    elif p_j2 > p_banca:
        resultados["j2"] = "J2 Ganhou!"
    elif p_j2 < p_banca:
        resultados["j2"] = "J2 Perdeu!"
    else:
        resultados["j2"] = "J2 Empatou (Push)"
        
    return resultados

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

def tela_regras():
    while True:
        tela.fill(VERDE_MESA)
        desenhar_texto("REGRAS DO JOGO", fonte_titulo, BRANCO, LARGURA // 2, 50)
        regras = [
            "- J1 e J2 jogam contra a banca.",
            "- Objetivo: Chegar o mais próximo de 21 sem passar.",
            "- Ás vale 1 ou 11.",
            "- Figuras valem 10.",
            "Bom jogo!"
        ]
        for i, linha in enumerate(regras):
            desenhar_texto(linha, fonte_menu, BRANCO, LARGURA // 2, 150 + (i * 40))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                return "MENU"
        
        pygame.display.update()

def jogar():
    baralho = criar_baralho()
    
    mao_j1 = [baralho.pop(), baralho.pop()]
    mao_j2 = [baralho.pop(), baralho.pop()]
    mao_banca = [baralho.pop(), baralho.pop()]
    
    turno = 0  
    mensagens = ["Vez do Jogador 1", "Vez do Jogador 2", "Vez da Banca..."]
    jogo_finalizado = False

    rodando = True
    while rodando:
        tela.fill(VERDE_MESA)
        
        # --- DESENHAR CARTAS
        # Desenha cartas do J1
        for i, carta in enumerate(mao_j1):
            rect = pygame.Rect(100 + i*30, 400, 70, 100)
            pygame.draw.rect(tela, BRANCO, rect, border_radius=5)
            desenhar_texto(f"{carta.valor_nome}", fonte_menu, PRETO, rect.centerx, rect.y + 10)

        # Desenha cartas do J2
        for i, carta in enumerate(mao_j2):
            rect = pygame.Rect(550 + i*30, 400, 70, 100)
            pygame.draw.rect(tela, BRANCO, rect, border_radius=5)
            desenhar_texto(f"{carta.valor_nome}", fonte_menu, PRETO, rect.centerx, rect.y + 10)

        # Desenha cartas da Banca
        for i, carta in enumerate(mao_banca):
            rect = pygame.Rect(LARGURA//2 - 35 + i*30, 200, 70, 100)
            # Esconde a segunda carta da banca se não for o turno dela
            if i == 1 and turno < 2:
                pygame.draw.rect(tela, PRETO, rect, border_radius=5)
            else:
                pygame.draw.rect(tela, BRANCO, rect, border_radius=5)
                desenhar_texto(f"{carta.valor_nome}", fonte_menu, PRETO, rect.centerx, rect.y + 10)

        # --- TEXTOS E PONTOS ---
        desenhar_texto(mensagens[turno], fonte_menu, BRANCO, LARGURA // 2, 20)
        ponto_j1 = calcular_pontuacao(mao_j1)
        ponto_j2 = calcular_pontuacao(mao_j2)
        ponto_banca = calcular_pontuacao(mao_banca)

        desenhar_texto(f"J1: {ponto_j1}", fonte_menu, BRANCO, 200, 520)
        desenhar_texto(f"J2: {ponto_j2}", fonte_menu, BRANCO, 650, 520)
        txt_banca = f"Banca: {ponto_banca}" if turno == 2 else "Banca: ?"
        desenhar_texto(txt_banca, fonte_menu, BRANCO, LARGURA // 2, 150)

        # --- BOTÕES ---
        btn_hit = pygame.Rect(LARGURA // 2 - 110, 320, 100, 40)
        btn_stand = pygame.Rect(LARGURA // 2 + 10, 320, 100, 40)
        
        if turno < 2:
            pygame.draw.rect(tela, CINZA, btn_hit, border_radius=5)
            pygame.draw.rect(tela, CINZA, btn_stand, border_radius=5)
            desenhar_texto("HIT", fonte_menu, PRETO, btn_hit.centerx, btn_hit.y + 5)
            desenhar_texto("STOP", fonte_menu, PRETO, btn_stand.centerx, btn_stand.y + 5)

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and turno < 2:
                if btn_hit.collidepoint(evento.pos):
                    if turno == 0:
                        mao_j1.append(baralho.pop())
                        if calcular_pontuacao(mao_j1) > 21: turno = 1
                    elif turno == 1:
                        mao_j2.append(baralho.pop())
                        if calcular_pontuacao(mao_j2) > 21: turno = 2
                if btn_stand.collidepoint(evento.pos):
                    turno += 1

        # --- LÓGICA DA BANCA ---
        if turno == 2 and not jogo_finalizado:
            pygame.display.update() # Atualiza para mostrar os pontos da banca
            pygame.time.delay(1000)
            if calcular_pontuacao(mao_banca) < 17:
                mao_banca.append(baralho.pop())
            else:
                res = conferir_resultados(ponto_j1, ponto_j2, ponto_banca)
                jogo_finalizado = True

        # --- FINALIZAÇÃO ---
        if jogo_finalizado:
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(180); overlay.fill((0, 0, 0))
            tela.blit(overlay, (0,0))
            desenhar_texto("RESULTADOS", fonte_titulo, BRANCO, LARGURA // 2, 150)
            desenhar_texto(res["j1"], fonte_menu, BRANCO, LARGURA // 2, 250)
            desenhar_texto(res["j2"], fonte_menu, BRANCO, LARGURA // 2, 300)
            desenhar_texto(f"Banca fez: {ponto_banca}", fonte_menu, CINZA, LARGURA // 2, 380)
            pygame.display.update()
            pygame.time.delay(4000)
            return "MENU"

        pygame.display.update()

estado = "MENU"
while True:
    if estado == "MENU":
        estado = menu_principal()
    elif estado == "JOGANDO":
        estado = jogar()
    elif estado == "REGRAS":
        estado = tela_regras()
        estado = "MENU"
    