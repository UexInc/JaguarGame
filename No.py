import numpy as np
from Estado import *

TAMANHO_JANELA = 4

class No:
    '''
    Essa classe representa um noh na arvore de busca
    '''
    
    def __init__(self, estado):
        """
        Construtor
        """
        self.estado = estado
        self.profundidade = 0
                   
    def liberaPeca(self,tabuleiro,coluna,peca):
        '''
        Coloca um peca no tabuleiro
        '''
        linha = self.estado.proximaLinhaLivre(tabuleiro,coluna)
        tabuleiro[linha][coluna] = peca


    def ehUmaPosicaoValida(self, coluna):
	    '''
	    Verifica se a posicao estah livre
	    '''
	    return self.estado.tabuleiro[self.estado.maxLinha-1][coluna] == 0


    def printTabuleiro(self):
	    '''
 	    Mostra o tabuleiro
 	    '''
	    print(np.flip(self.estado.tabuleiro, 0))
        
    def avalia_janela(self,janela, peca):
	    '''
 	    Analisa um parte do tabulerio 
	    '''
	    pontuacao  = 0
	    peca_oponente = self.estado.pecaHumano
	    if peca == self.estado.pecaHumano:
	        peca_oponente = self.estado.pecaIA

	    if janela.count(peca) == 4:
	        pontuacao  += 100
	    elif janela.count(peca) == 3 and janela.count(self.estado.vazio) == 1:
	        pontuacao  += 5
	    elif janela.count(peca) == 2 and janela.count(self.estado.vazio) == 2:
	        pontuacao  += 2

	    if janela.count(peca_oponente) == 3 and janela.count(self.estado.vazio) == 1:
	        pontuacao  -= 4

	    #print(janela," = ", pontuacao)
	    return pontuacao 

    def calculaHeuristica(self,tabuleiro, peca):
	    pontuacao = 0
	    #pontuacao coluna central 
	    array_central = [int(i) for i in list(tabuleiro[:, self.estado.maxColuna//2])]
	    pontuacao_centro = array_central.count(peca)
	    pontuacao  += pontuacao_centro * 3
	    #print(array_central) 
    
	    #pontuacao Horizontal
	    for r in range(self.estado.maxLinha):
		    array_linha = [int(i) for i in list(tabuleiro[r,:])]
		    for c in range(self.estado.maxColuna-3):
			    janela = array_linha[c:c+TAMANHO_JANELA]
			    pontuacao  += self.avalia_janela(janela, peca)

	    #pontuacao Vertical
	    for c in range(self.estado.maxColuna):
		    col_array = [int(i) for i in list(tabuleiro[:,c])]
		    for r in range(self.estado.maxLinha-3):
			    janela = col_array[r:r+TAMANHO_JANELA]
			    pontuacao  += self.avalia_janela(janela, peca)

	    #pontuacao Diagonal Principal
	    for r in range(self.estado.maxLinha-3):
		    for c in range(self.estado.maxColuna-3):
			    janela = [int(tabuleiro[r+i][c+i]) for i in range(TAMANHO_JANELA)]
			    pontuacao  += self.avalia_janela(janela, peca)

        #pontuacao Diagonal Secundaria
	    for r in range(self.estado.maxLinha-3):
		    for c in range(self.estado.maxColuna-3):
			    janela = [int(tabuleiro[r+3-i][c+i]) for i in range(TAMANHO_JANELA)]
			    pontuacao += self.avalia_janela(janela, peca)
	    return pontuacao 

