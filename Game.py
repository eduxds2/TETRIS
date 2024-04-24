import pygame
import random

pygame.init()

# Define o tamanho da tela
largura_tela = 800  # Defina a largura da tela conforme necessário
altura_tela = 600   # Defina a altura da tela conforme necessário

# Tamanho do campo
altura = 20
largura = 10

# Tamanho do bloco (cada célula do campo de jogo)
tamanho_bloco = 30  # Defina o tamanho do bloco conforme necessário

# Calcula as coordenadas X e Y para posicionar o campo de jogo no centro da tela
campo_x = (largura_tela - largura * tamanho_bloco) // 2
campo_y = (altura_tela - altura * tamanho_bloco) // 2

# Cores disponíveis para as peças e o campo
cores = [
    (0, 0, 255),    # Azul
    (0, 255, 0),    # Verde
    (255, 0, 0),    # Vermelho
    (255, 255, 0),  # Amarelo
    (128, 0, 128),  # Roxo
    (255, 165, 0),  # Laranja
    (0, 255, 255)   # Ciano
]

# Outras cores
PRETO = (0, 0, 0)
CINZA = (128, 128, 128)
COR_TEXTOS = (128, 0, 128)
VERDE = (0, 255, 0)
VERMELHO=(255, 0, 0)
AMARELO=(255, 255, 0)

class Peca:
    x = 0
    y = 0

    figuras = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tipo = random.randint(0, len(self.figuras) - 1)
        self.cor = random.randint(1, len(cores) - 1)
        self.rotacao = 0

    def imagem(self):
        return self.figuras[self.tipo][self.rotacao]

    def rotacionar(self):
        self.rotacao = (self.rotacao + 1) % len(self.figuras[self.tipo])


class Tetris:
    def __init__(self, altura, largura, dificuldade):
        # Inicialização do jogo
        self.nivel = 2
        self.pontuacao = 0
        self.estado = "iniciar"
        self.campo = []
        self.altura = altura
        self.largura = largura
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.peca_atual = None
        self.velocidade = 40  # Defina a velocidade padrão aqui
        self.linhas_feitas = 0  # Adicione o atributo linhas_feitas aqui
        
        self.altura = altura
        self.largura = largura
        self.campo = []
        self.pontuacao = 0
        self.estado = "iniciar"
        for i in range(altura):
            nova_linha = []
            for j in range(largura):
                nova_linha.append(0)
            self.campo.append(nova_linha)

        if dificuldade == "facil":
            self.velocidade = 40
        elif dificuldade == "normal":
            self.velocidade = 60
        elif dificuldade == "hard":
            self.velocidade = 150

    def nova_peca(self):
        self.peca_atual = Peca(3, 0)

    def intersecta(self):
        intersecao = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.peca_atual.imagem():
                    if i + self.peca_atual.y > self.altura - 1 or \
                            j + self.peca_atual.x > self.largura - 1 or \
                            j + self.peca_atual.x < 0 or \
                            self.campo[i + self.peca_atual.y][j + self.peca_atual.x] > 0:
                        intersecao = True
        return intersecao

    def quebrar_linhas(self):
        linhas = 0
        for i in range(1, self.altura):
            zeros = 0
            for j in range(self.largura):
                if self.campo[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                linhas += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.largura):
                        self.campo[i1][j] = self.campo[i1 - 1][j]
        # Pontuação aleatória por linha
        pontos = random.randint(10, 500)
        self.pontuacao += pontos * linhas

        # Incrementa o contador de linhas feitas e ajusta a velocidade do jogo
        self.linhas_feitas += linhas
        if self.linhas_feitas >= 10:
            self.velocidade *= 1.5
            #self.linhas_feitas = 0

    def mover_espaco(self):
        while not self.intersecta():
            self.peca_atual.y += 1
        self.peca_atual.y -= 1
        self.congelar()

    def mover_baixo(self):
        self.peca_atual.y += 1
        if self.intersecta():
            self.peca_atual.y -= 1
            self.congelar()

    def congelar(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.peca_atual.imagem():
                    self.campo[i + self.peca_atual.y][j + self.peca_atual.x] = self.peca_atual.cor
        self.quebrar_linhas()
        self.nova_peca()
        if self.intersecta():
            self.estado = "perdeu"
            pygame.mixer.music.stop()  # Para a música de fundo
            barulho_jogo.play()  # Reproduz o som de "game over"

    def mover_lateral(self, dx):
        x_antigo = self.peca_atual.x
        self.peca_atual.x += dx
        if self.intersecta():
            self.peca_atual.x = x_antigo

    def rotacionar(self):
        rotacao_antiga = self.peca_atual.rotacao
        self.peca_atual.rotacionar()
        if self.intersecta():
            self.peca_atual.rotacao = rotacao_antiga

# Define o tamanho da tela
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Define o título da janela
pygame.display.set_caption("Tetris")

# Som
pygame.mixer.music.set_volume(0.1)
musica_de_fundo = pygame.mixer.music.load('Musicas/fundo.wav')
pygame.mixer.music.play(-1)

# Som de game over
barulho_jogo = pygame.mixer.Sound('Musicas/game_over.wav')

# Loop até o usuário clicar no botão de fechar.
fechado = False
relogio = pygame.time.Clock()
fps = 40
#tamanho jogo largura
jogo = None
contador = 0
pressionando_baixo = False
pausado = False
selecionando_dificuldade = True
dificuldade_selecionada = "facil"
velocidade_jogo = fps

def pausar_jogo():
    pausado = True
    ponto_pausa_musica = pygame.mixer.music.get_pos() // 1000  # Armazena o ponto de pausa da música em segundos
    pygame.mixer.music.pause()  # Pausa a música de fundo
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_TAB:
                pausado = False
                pygame.mixer.music.unpause()  # Continua a reprodução da música de fundo
                pygame.mixer.music.play(-1, ponto_pausa_musica)  # Define o ponto de início da música
                break
            elif evento.type == pygame.QUIT:
                pygame.quit()
                exit()
        tela.fill(PRETO)
        fonte = pygame.font.SysFont('Calibri', 50, True, False)
        texto_pausa = fonte.render("PAUSADO", True, COR_TEXTOS)
        tela.blit(texto_pausa, (tela.get_width() // 2 - 100, tela.get_height() // 2 - 50))
        pygame.display.flip()
        relogio.tick(30)  # Limita o loop a 30 frames por segundo

while not fechado:
    if jogo is None and not selecionando_dificuldade:
        jogo = Tetris(altura, largura, dificuldade_selecionada)
        jogo.nova_peca()  # Adiciona essa linha para inicializar uma nova peça

    contador += 1
    if contador > 100000:
        contador = 0

    if jogo is not None and jogo.estado == "iniciar" and (contador % (fps // jogo.nivel // 2) == 0 or pressionando_baixo):
        if not pausado:  # Adicione esta condição para verificar se o jogo está pausado
            jogo.mover_baixo()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fechado = True
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and jogo is not None and jogo.estado == "iniciar":
                jogo.rotacionar()
            if evento.key == pygame.K_DOWN and jogo is not None and jogo.estado == "iniciar":
                pressionando_baixo = True
            if evento.key == pygame.K_LEFT and jogo is not None and jogo.estado == "iniciar":
                jogo.mover_lateral(-1)
            if evento.key == pygame.K_RIGHT and jogo is not None and jogo.estado == "iniciar":
                jogo.mover_lateral(1)
            if evento.key == pygame.K_SPACE and jogo is not None and jogo.estado == "iniciar":
                jogo.mover_espaco()
            if evento.key == pygame.K_s and jogo is not None and jogo.estado == "perdeu":
                # Reinicia o jogo
                jogo = None
                pygame.mixer.music.play(-1)  # Reinicia a música de fundo
            if evento.key == pygame.K_n and jogo is not None and jogo.estado == "perdeu":
                fechado = True
            if evento.key == pygame.K_RETURN and selecionando_dificuldade:
                if dificuldade_selecionada == "facil":
                    velocidade_jogo = 40
                elif dificuldade_selecionada == "normal":
                    velocidade_jogo = 60
                elif dificuldade_selecionada == "hard":
                    velocidade_jogo = 150
                selecionando_dificuldade = False
            if evento.key == pygame.K_TAB:  # Adicione esta condição para pausar o jogo ao pressionar TAB
                pausar_jogo()
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_DOWN:
                pressionando_baixo = False

        # Selecionar a dificuldade
        if selecionando_dificuldade:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if dificuldade_selecionada == "facil":
                        dificuldade_selecionada = "hard"
                    elif dificuldade_selecionada == "normal":
                        dificuldade_selecionada = "facil"
                    elif dificuldade_selecionada == "hard":
                        dificuldade_selecionada = "normal"
                elif evento.key == pygame.K_DOWN:
                    if dificuldade_selecionada == "facil":
                        dificuldade_selecionada = "normal"
                    elif dificuldade_selecionada == "normal":
                        dificuldade_selecionada = "hard"
                    elif dificuldade_selecionada == "hard":
                        dificuldade_selecionada = "facil"

    tela.fill(PRETO)

    # Exibir a seleção de dificuldade se necessário
    if selecionando_dificuldade:
        fonte = pygame.font.SysFont('Calibri', 30, True, False)
        texto_dificuldade = fonte.render("Selecione a Dificuldade:", True, CINZA)
        texto_facil = fonte.render("Facil", True, VERDE if dificuldade_selecionada == "facil" else PRETO)
        texto_normal = fonte.render("Normal", True, AMARELO if dificuldade_selecionada == "normal" else PRETO)
        texto_hard = fonte.render("Dificil", True, VERMELHO if dificuldade_selecionada == "hard" else PRETO)

        tela.blit(texto_dificuldade, [tela.get_width() // 2 - 130, tela.get_height() // 2 - 100])
        tela.blit(texto_facil, [tela.get_width() // 2 - 40, tela.get_height() // 2])
        tela.blit(texto_normal, [tela.get_width() // 2 - 50, tela.get_height() // 2 + 40])
        tela.blit(texto_hard, [tela.get_width() // 2 - 40, tela.get_height() // 2 + 80])
    # Exibir o jogo se estiver em andamento
    elif jogo is not None:
        # Desenha o campo do jogo
        for i in range(jogo.altura):
            for j in range(jogo.largura):
                pygame.draw.rect(tela, CINZA, [jogo.x + jogo.zoom * j, jogo.y + jogo.zoom * i, jogo.zoom, jogo.zoom], 1)
                if jogo.campo[i][j] > 0:
                    pygame.draw.rect(tela, cores[jogo.campo[i][j]],
                                    [jogo.x + jogo.zoom * j + 1, jogo.y + jogo.zoom * i + 1, jogo.zoom - 2, jogo.zoom - 2])

        # Desenha a peça atual
        if jogo.peca_atual is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in jogo.peca_atual.imagem():
                        pygame.draw.rect(tela, cores[jogo.peca_atual.cor],
                                        [jogo.x + jogo.zoom * (j + jogo.peca_atual.x) + 1,
                                        jogo.y + jogo.zoom * (i + jogo.peca_atual.y) + 1,
                                        jogo.zoom - 2, jogo.zoom - 2])

        # Desenha a pontuação e linhas feitas
        fonte = pygame.font.SysFont('Calibri', 25, True, False)
        texto_pontos = fonte.render("Pontos: " + str(jogo.pontuacao), True, CINZA)
        texto_linhas = fonte.render("Linhas: " + str(jogo.linhas_feitas), True, CINZA)
        tela.blit(texto_pontos, [0, 0])
        tela.blit(texto_linhas, [0, 30])

        # Desenha o texto "Perdeu" e as opções de continuar/sair
        if jogo.estado == "perdeu":
            fonte1 = pygame.font.SysFont('Calibri', 65, True, False)
            texto_perdeu = fonte1.render("Perdeu", True, COR_TEXTOS)
            texto_continuar = fonte.render("Continuar (S)", True, COR_TEXTOS)
            texto_sair = fonte.render("Sair (N)", True, COR_TEXTOS)

            # Posiciona o texto "Perdeu" no centro da tela
            texto_perdeu_rect = texto_perdeu.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2))
            # Posiciona os botões "Continuar" e "Sair" abaixo do texto "Perdeu"
            texto_continuar_rect = texto_continuar.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2 + 50))
            texto_sair_rect = texto_sair.get_rect(center=(tela.get_width() // 2, tela.get_height() // 2 + 100))

            tela.blit(texto_perdeu, texto_perdeu_rect)
            tela.blit(texto_continuar, texto_continuar_rect)
            tela.blit(texto_sair, texto_sair_rect)

    pygame.display.flip()
    relogio.tick(velocidade_jogo)  # Ajusta a velocidade do jogo de acordo com a dificuldade selecionada

pygame.quit()
