import numpy as np

MAX_LINHA = 7
MAX_COLUNA = 5

VAZIO = 0
PECA_HUMANO = 1
PECA_IA = 2

class Estado:
    
    def __init__(self, tabuleiro= [], destino = None):
        self.maxLinha = MAX_LINHA
        self.maxColuna = MAX_COLUNA
        self.pecaHumano = PECA_HUMANO
        self.pecaIA = PECA_IA
        self.vazio = VAZIO
        if tabuleiro!= []:
            #cria o estado inicial
            self.tabuleiro = tabuleiro
            
        else:
            self.tabuleiro = self.pegaEstadoInicial()


    def pegaEstadoInicial(self):
        """
        Este metodo retorna o estado incial com o tabuleiro vazio
        """
        estadoInicial= np.zeros((7,5))
        return estadoInicial


    def proximaLinhaLivre(self,tabuleiro,coluna):
        """
        Encontra a primeira posicao livre em uma coluna para por uma peca
        """
        for l in range(self.maxLinha):
            if tabuleiro[l][coluna]==self.vazio:
                return l 
        return -1 # nao tem espaco na coluna


    def funcaoSucessora(self,peca):
        """
        Esta é a função sucessora. Gera todo os possiveis
        lugares que podem ser alcançados a partir do estado atual.
        """
        estados = []
        for coluna in range(self.maxColuna):
            novoTabuleiro = np.copy(self.tabuleiro)
            linha = self.proximaLinhaLivre(novoTabuleiro,coluna)
            if linha>-1: #coluna com espaco livre
                novoTabuleiro[linha][coluna] = peca
                estados.append(novoTabuleiro)                
        return estados  

    def empate(self,tabuleiro):
        """
	    Verifica se o jogo empatou
	    """
        for c in range(self.maxColuna):
            if tabuleiro[self.maxLinha-1][c]==self.vazio:
                return False
        return True

    def jogadorVenceu(self,tabuleiro, peca):
	    """
	    Verifica de o jogador dono da peca venceu o jogo.
	    """
	    #verifica se hove uma sequecia de 4 na horizontal
	    for c in range(self.maxColuna-3):
		    for r in range(self.maxLinha):
			    if tabuleiro[r][c] == peca and \
                   tabuleiro[r][c+1] == peca and \
                   tabuleiro[r][c+2] == peca and \
                   tabuleiro[r][c+3] == peca:
				    return True

	    #verifica se hove uma sequecia de 4 na vertical
	    for c in range(self.maxColuna):
		    for r in range(self.maxLinha-3):
			    if tabuleiro[r][c] == peca and \
                   tabuleiro[r+1][c] == peca and \
                   tabuleiro[r+2][c] == peca and \
                   tabuleiro[r+3][c] == peca:
				    return True

	    #verifica se hove uma sequecia de 4 na diagonal principal
	    for c in range(self.maxColuna-3):
		    for r in range(self.maxLinha-3):
			    if tabuleiro[r][c] == peca and \
                   tabuleiro[r+1][c+1] == peca and \
                   tabuleiro[r+2][c+2] == peca and \
                   tabuleiro[r+3][c+3] == peca:
				    return True

	    #verifica se hove uma sequecia de 4 na diagonal secundaria
	    for c in range(self.maxColuna-3):
		    for r in range(3, self.maxLinha):
			    if tabuleiro[r][c] == peca and \
                   tabuleiro[r-1][c+1] == peca and \
                   tabuleiro[r-2][c+2] == peca and \
                   tabuleiro[r-3][c+3] == peca:
				    return True    


    def funcaoObjetivo(self):
        """
        Este método verifica se o caminho está no estado objetivo
        """
        #verifica se eh fim de jogo
        return self.jogadorVenceu(self.tabuleiro,self.pecaHumano) or \
               self.jogadorVenceu(self.tabuleiro,self.pecaIA) or \
               self.empate(self.tabuleiro)         

if __name__== "__main__":
    estado = Estado()
    print(np.flip(estado.tabuleiro,0))
    lista=estado.funcaoSucessora(1)
    for l in lista:
        print("--------")
        print(np.flip(l,0))

        




