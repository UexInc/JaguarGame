import numpy as np

MAX_LINHA = 7
MAX_COLUNA = 5

TAMANHO_JANELA = 4

VAZIO = 0
PECA_HUMANO = 1
PECA_IA = 2

def cria_tabuleiro():
	tabuleiro = np.zeros((MAX_LINHA,MAX_COLUNA))
	return tabuleiro

def avalia_janela(janela, peca):
	pontuacao  = 0
	peca_oponente = PECA_HUMANO
	if peca == PECA_HUMANO:
		peca_oponente = PECA_IA

	if janela.count(peca) == 4:
		pontuacao  += 100
	elif janela.count(peca) == 3 and janela.count(VAZIO) == 1:
		pontuacao  += 5
	elif janela.count(peca) == 2 and janela.count(VAZIO) == 2:
		pontuacao  += 2

	if janela.count(peca_oponente) == 3 and janela.count(VAZIO) == 1:
		pontuacao  -= 4

	#print(janela," = ", pontuacao)
	return pontuacao 

def avalia_estado(tabuleiro, peca):

	pontuacao = 0

	#pontuacao coluna central 
	array_central = [int(i) for i in list(tabuleiro[:, MAX_COLUNA//2])]
	pontuacao_centro = array_central.count(peca)
	pontuacao  += pontuacao_centro * 3
	#print(array_central) 
    
	#pontuacao Horizontal
	for r in range(MAX_LINHA):
		array_linha = [int(i) for i in list(tabuleiro[r,:])]
		for c in range(MAX_COLUNA-3):
			janela = array_linha[c:c+TAMANHO_JANELA]
			pontuacao  += avalia_janela(janela, peca)

	#pontuacao Vertical
	for c in range(MAX_COLUNA):
		col_array = [int(i) for i in list(tabuleiro[:,c])]
		for r in range(MAX_LINHA-3):
			janela = col_array[r:r+TAMANHO_JANELA]
			pontuacao  += avalia_janela(janela, peca)

	#pontuacao Diagonal Principal
	for r in range(MAX_LINHA-3):
		for c in range(MAX_COLUNA-3):
			janela = [int(tabuleiro[r+i][c+i]) for i in range(TAMANHO_JANELA)]
			pontuacao  += avalia_janela(janela, peca)

    #pontuacao Diagonal Secundaria
	for r in range(MAX_LINHA-3):
		for c in range(MAX_COLUNA-3):
			janela = [int(tabuleiro[r+3-i][c+i]) for i in range(TAMANHO_JANELA)]
			pontuacao  += avalia_janela(janela, peca)
	return pontuacao 

def preencheTabuleiro(tabuleio):
    cc=1
    for i in range(MAX_LINHA):
        for j in range(MAX_COLUNA):
            tab[i][j] = cc
            cc+=1


tab = cria_tabuleiro()
#preencheTabuleiro(tab)

tab[3][0] = PECA_HUMANO
tab[2][0] = PECA_HUMANO
tab[1][0] = PECA_HUMANO
tab[0][0] = PECA_IA
tab[4][0] = PECA_IA
print(tab)

h = avalia_estado(tab, PECA_HUMANO)
print(h)


'''
def melhorJogada(tabuleiro):
    melhorMovimento = None
    for movimento in tabuleiro:
        if movimento eh melhor que melhorMovimento:
            melhorMovimento = movimento
    return melhorMovimento




def minimax(tabuleiro, nivel, ehJogadorMax):

    if tabuleiro is umEstadoFinal:
        return valor(tabuleiro)
    
    if ehJogadorMax:
        melhorValor = -100000000
        for movimento in tabuleiro:
            valor = minimax(tabuleiro, nivel+1, False)
            melhorValor = max(melhorValor, valor) 
        return melhorValor

    else:
        bestVal = +100000000
        for movimento in tabuleiro:
            valor = minimax(tabuleiro, nivel+1, True)
            melhorValor = min(melhorValor, valor) 
        return melhorValor 

def ehUmEstadoFinal(tabuleiro):
    for celula in tabuleiro:
        if celula is empty:
            return True
    return False

'''