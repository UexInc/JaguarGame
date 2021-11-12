from No import *
import numpy as np
import random
import math

def minimax(noh, profundidade,alpha, beta,ehJogadorMaximizador):
	
	ehNoTerminal = noh.estado.funcaoObjetivo()
	if profundidade == 0 or ehNoTerminal:
		if ehNoTerminal:
			if noh.estado.jogadorVenceu(noh.estado.tabuleiro,noh.estado.pecaIA):
				return (None, 100000000000000)
			elif noh.estado.jogadorVenceu(noh.estado.tabuleiro,noh.estado.pecaHumano):
				return (None, -10000000000000)
			else: #o jogo acabou
				return (None, 0)
		else: #chegou a profundidade final
			return (None, noh.calculaHeuristica(noh.estado.tabuleiro,noh.estado.pecaIA))
	if ehJogadorMaximizador:
		jogadasValidas = noh.estado.funcaoSucessora(noh.estado.pecaIA)
		valor = -math.inf
		melhorJogada = No(random.choice(jogadasValidas))
		for jogada in jogadasValidas:	
			novoNo = No(Estado(jogada))		
			_,novaPontuacao = minimax(novoNo, profundidade-1,alpha, beta, False)
			if novaPontuacao > valor:
				valor = novaPontuacao
				melhorJogada  = novoNo
			alpha = max(alpha, valor)
			if alpha >= beta:
				break
		return melhorJogada , valor

	else: #jogador Minimizador
		jogadasValidas = noh.estado.funcaoSucessora(noh.estado.pecaHumano)
		valor= math.inf
		melhorJogada = No(random.choice(jogadasValidas))
		for jogada in jogadasValidas:
		    novoNo = No(Estado(jogada))	
		    _,novaPontuacao = minimax(novoNo, profundidade-1, alpha, beta,True)
		    if novaPontuacao < valor:
		    	valor = novaPontuacao
		    	melhorJogada  = novoNo
		    beta = min(beta, valor)
		    if alpha >= beta:
		    	break
		return melhorJogada , valor