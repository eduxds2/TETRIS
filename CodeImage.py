
    
    # Carregar e exibir a imagem
    imagem = pygame.image.load(r'Imagens\imagem.png')
    #lado direito
    largura_imagem = 1000
    #lado para cima
    altura_imagem = 285
    imagem = pygame.transform.scale(imagem, (largura_imagem, altura_imagem))
    posicao_imagem = (20, tela.get_height() - altura_imagem - 20)
    tela.blit(imagem, posicao_imagem)
