import numpy as np
import random
import pygame
import sys
import math

from pygame import draw

from No import *
from Estado import *
from MiniMaxAlphaBeta import *

BLUE = (0,0,255)
DARKBLUE = (0,0,139)

RED = (255,0,0)
DARKRED = (139,0,0)

YELLOW = (255,255,0)
DARKYELLOW = (139,139,0)

BLACK = (0,0,0)
GREEN = (0, 255, 0)

ROW_COUNT = 7
COLUMN_COUNT = 5

DOGS = 0
JAGUAR = 1

tab = Estado()
jogo = No(tab)

jogo.printTabuleiro()
game_over = False

pygame.init()

SQUARESIZE = 80

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/4)

# TODO: Variaveis do jogo
start = True
points = None
dogs_eaten = 0

# =========================

def draw_board(jogo, points):
    global start
    draw_square()
    draw_triangle()
    if start:
        points = draw_points()
        draw_dogs(points, start)
        draw_jaguar(points, start)
        start = False
    else:
        draw_points(points)
        draw_dogs(points, start)
        draw_jaguar(points, start)
    pygame.display.update()
    return points

def draw_square():
    columns = 5
    rows = 5
    for c in range(columns):
        c1 = (int(c*SQUARESIZE+SQUARESIZE/2), int(SQUARESIZE+SQUARESIZE/2))
        c2 = (int(c*SQUARESIZE+SQUARESIZE/2), int((rows-1)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))
        pygame.draw.line(screen, GREEN, c1, c2)

    for r in range(rows):
        c1 = (int(SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))
        c2 = (int((columns-1)*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))
        pygame.draw.line(screen, GREEN, c1, c2)

    for c in (1,3):
        for r in (1,3):
            c1 = (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))
            for i in (-1, 1):
                for j in (-1, 1):
                    c2 = (int((c+i)*SQUARESIZE+SQUARESIZE/2), int((r+j)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2))
                    pygame.draw.line(screen, GREEN, c1, c2)

def draw_triangle():
    adjustment = SQUARESIZE * 4
    c = 2
    r = 0
    c1 = (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+adjustment+SQUARESIZE/2))
    c2 = (int(c*SQUARESIZE+SQUARESIZE/2), int((r+2)*SQUARESIZE+SQUARESIZE+adjustment+SQUARESIZE/2))
    pygame.draw.line(screen, GREEN, c1, c2)
    next_values = []
    for i in (-2, 2):
        j = 2
        c2 = (int((c+i)*SQUARESIZE+SQUARESIZE/2), int((r+j)*SQUARESIZE+SQUARESIZE+adjustment+SQUARESIZE/2))
        next_values.append(c2)
        pygame.draw.line(screen, GREEN, c1, c2)
    pygame.draw.line(screen, GREEN, next_values[0], next_values[1])
    r = 1
    c1 = (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+adjustment+SQUARESIZE/2))
    for i in (-1, 1):
        c2 = (int((c+i)*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+adjustment+SQUARESIZE/2))
        pygame.draw.line(screen, GREEN, c1, c2)

def draw_points(p = None):
    if p is None:
        points = []
        for r in range(ROW_COUNT):
            for c in range(COLUMN_COUNT):
                if r == 5 and c in (0, 4):
                    points.append(None)
                    continue
                if r == 6 and c in (1, 3):
                    points.append(None)
                    continue
                points.append([pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS), None, (r, c)])
        return points
    for item in p:
        if item is not None:
            if item[1] is None:
                pygame.draw.circle(screen, BLUE, (int(item[0][0] + RADIUS), int(item[0][1] + RADIUS)), RADIUS)

def draw_dogs(p, start):
    if start:
        i = 0
        for r in range(ROW_COUNT // 2):
            if r == 3:
                break
            for c in range(COLUMN_COUNT):
                if r == 2 and c == 2:
                    i += 1
                    continue
                else:
                    p[i] = [pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS), 0, (r, c)]
                    i += 1
        return
    for item in p:
        if item is not None:
            if item[1] == 0:
                pygame.draw.circle(screen, YELLOW, (int(item[0][0] + RADIUS), int(item[0][1] + RADIUS)), RADIUS)

def draw_jaguar(p, start):
    if start:
        x = COLUMN_COUNT // 2
        y = ROW_COUNT // 2 + 1
        p[12] = [pygame.draw.circle(screen, RED, (int(x*SQUARESIZE+SQUARESIZE/2), height-int(y*SQUARESIZE+SQUARESIZE/2)), RADIUS), 1, (2, 2)]
    for item in p:
        if item is not None:
            if item[1] == 1:
                pygame.draw.circle(screen, RED, (int(item[0][0] + RADIUS), int(item[0][1] + RADIUS)), RADIUS)
                break

def clicked_point(mouse_position, points):
    ps = tuple(p for p in points if p is not None and p[0].collidepoint(mouse_position))
    return ps[0] if len(ps) == 1 else None

def check_part_by_coordinates(coor):
    for p in points:
        if p is not None:
            if p[2] == coor:
                return p

def dist_points(p1, p2):
    return math.sqrt((p1[0][0] - p2[0][0])**2 + (p1[0][1] - p2[0][1])**2)

def mensagem(msg, font, coor = (40,10)):
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
    label = font.render(msg, 1, YELLOW)
    screen.blit(label, coor)

def back_to_point_default(point):
    if point[1] is None: # se é um ponto vazio
        pygame.draw.circle(screen, BLUE, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)
    elif point[1] == 0: # se é um cachorro
        pygame.draw.circle(screen, YELLOW, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)
    else: # é o jaguar
        pygame.draw.circle(screen, RED, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)

def validate_action(p1, p2):
    global dogs_eaten

    if p2[1] is not None:
        return (False,)

    # Valida a movimentação na horizontal entre as três últimas peças do tabuleiro.
    if p1[2][0] == p2[2][0] == 6:
        if (p2[0][0] - p1[0][0] == SQUARESIZE*2 or p2[0][0] - p1[0][0] == -SQUARESIZE*2):
            return (True,)
        else:
            if p1[2][0] == 6 and p2[2][0] == 6:
                p = check_part_by_coordinates((6, 2))
                if p is None or p[1] is None:
                    return (False,)
                dogs_eaten+=1
                return (True,p)
        return (False,)

    # Se não for uma casa adjacente.
    if (p2[0][0] - p1[0][0] > SQUARESIZE or p2[0][0] - p1[0][0] < -SQUARESIZE) or (p2[0][1] - p1[0][1] > SQUARESIZE or p2[0][1] - p1[0][1] < -SQUARESIZE):
        if p1[1] == 0:
            return (False,)
        if ((p2[0][0] - p1[0][0] in (SQUARESIZE*2, -SQUARESIZE*2)) and (p2[0][1] - p1[0][1] in (SQUARESIZE*2, -SQUARESIZE*2))) or\
            ((p2[0][0] - p1[0][0] in (SQUARESIZE*2, -SQUARESIZE*2)) and (p2[0][1] - p1[0][1] == 0)) or\
            ((p2[0][0] - p1[0][0] == 0) and (p2[0][1] - p1[0][1] in (SQUARESIZE*2, -SQUARESIZE*2))):

            r = p1[2][0] if p2[2][0] == p1[2][0] else p2[2][0] + (-1 if p2[2][0] > p1[2][0] else 1)
            c = p1[2][1] if p2[2][1] == p1[2][1] else p2[2][1] + (-1 if p2[2][1] > p1[2][1] else 1)
            p = check_part_by_coordinates((r, c))
            if p is None or p[1] is None:
                return (False,)
            if (r == 4 and c != 2) and p1[2][0] != 4:
                return (False,)
            if r == 5 and p1[2][0] != 5:
                if (p2[2][0] == 4 and p2[2][1] == 2) and p1[2][0] == 6:
                    dogs_eaten+=1
                    return (True,p)
                if (p1[2][0] == 4 and p1[2][1] == 2) and p2[2][0] == 6:
                    dogs_eaten+=1
                    return (True,p)
                return (False,)
            dogs_eaten+=1
            return (True,p)

        return (False,)
    else:
        # Se for algum ponto da linha 5 exceto o ponto da coluna 2, não fará nenhum movimento para baixo.
        if p1[2][0] == 4 and p1[2][1] != 2:
            if p2[0][1] - p1[0][1] >= SQUARESIZE:
                return (False,)

        # Se for algum ponto da linha 5 ou 6 e que venha ANTES da coluna 2, não fará nenhum movimento
        # para cima e para cima na diagonal ESQUERDA.
        if p1[2][0] in (5, 6) and p1[2][1] < 2:
            if ((p2[0][0] - p1[0][0] < SQUARESIZE) and (p2[0][1] - p1[0][1] <= -SQUARESIZE))\
                or ((p2[0][0] - p1[0][0] > -SQUARESIZE) and (p2[0][1] - p1[0][1] >= SQUARESIZE)):
                return (False,)
        # Se for algum ponto da linha 5 ou 6 e que venha DEPOIS da coluna 2, não fará nenhum movimento
        # para cima e para cima na diagonal DIREITA.
        if p1[2][0] in (5, 6) and p1[2][1] > 2:
            if ((p2[0][0] - p1[0][0] > -SQUARESIZE) and (p2[0][1] - p1[0][1] <= -SQUARESIZE))\
                or ((p2[0][0] - p1[0][0] < SQUARESIZE) and (p2[0][1] - p1[0][1] >= SQUARESIZE)):
                return (False,)

        # Verifica se a peça pode fazer um movimento na diagonal, com base no ponto onde ela se encontra.
        diagonal_moviment = False
        if ((p1[2][0] % 2 == 0) and (p1[2][1] % 2 == 0)) or ((p1[2][0] % 2 == 1) and (p1[2][1] % 2 == 1)):
            diagonal_moviment = True # pode se mover na diagonal
            if (p1[2][0] in (5, 6) and p1[2][1] == 2):
                diagonal_moviment = False # NÃO pode se mover na diagonal
        
        if (abs(p2[0][0] - p1[0][0]) == SQUARESIZE) and (abs(p2[0][1] - p1[0][1]) == SQUARESIZE):
            if not diagonal_moviment:
                return (False,)

    return (True,)

def wait_and_clean(ms = 500):
    pygame.display.update()
    pygame.time.wait(ms)
    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

# =========================

screen = pygame.display.set_mode(size)
points = draw_board(jogo, points)
point1 = point2 = None
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 25)

turn = JAGUAR

while not game_over:

    msg = "Rodada dos cachorros" if turn == DOGS else "Rodada da onça"
    mensagem(msg, myfont)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            point = clicked_point(mouse_position, points)

            print("-"*30)
            print(point)
                
            if point is None: # nenhuma peça selecionada
                mensagem("Selecione uma peça!", myfont)
                continue

            if point1 == point: # selecionou a mesma peça de novo
                point1 = back_to_point_default(point1)
                continue

            if point1 == point2 == None: # é a primeira peça selecionada
                if (point[1] == 1 and turn == DOGS) or (point[1] == 0 and turn == JAGUAR):
                    mensagem("Rodada errada!", myfont)
                    pygame.display.update()
                    wait_and_clean(750)
                    continue

                point1 = point
                
                if point[1] == 1: # se é jaguar
                    pygame.draw.circle(screen, DARKRED, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)
                else:
                    if point[1] == 0: # se é um cachorro
                        pygame.draw.circle(screen, DARKYELLOW, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)
                    else: # é um ponto vazio
                        point1 = None
                        mensagem("Ponto vazio!", myfont)
                        pygame.draw.circle(screen, DARKBLUE, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)
                        wait_and_clean(500)
                        pygame.draw.circle(screen, BLUE, (int(point[0][0] + RADIUS), int(point[0][1] + RADIUS)), RADIUS)

            else: # é a segunda peça selecionada, neste caso, a ação deve ser validada.
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                point2 = point

                v = validate_action(point1, point2)
                if not v[0]:
                    point2 = None
                    mensagem("Ação inválida", myfont)
                    wait_and_clean(750)
                    continue
                
                if len(v) == 2:
                    print("CACHORROS COMIDOS =>", dogs_eaten)
                    v[1][1] = None
                
                print("-"*30)
                print("*** TROCA ***")
                print("ANTES")
                print("p1 =>", point1)
                print("p2 =>", point2)
                point1[1], point2[1] = point2[1], point1[1]
                print("DEPOIS")
                print("p1 =>", point1)
                print("p2 =>", point2)
                point1 = point2 = None
                turn = (turn+1)%2
                draw_board(jogo, points)

        pygame.display.update()

    # if turn == AI and not game_over:
    #     novoJogo, minimax_score = minimax(jogo, 5, -math.inf, math.inf,True)
    #     #novoJogo, minimax_score = minimax(jogo, 4,True)

    #     jogo = novoJogo
        
    #     if jogo.estado.jogadorVenceu(jogo.estado.tabuleiro, jogo.estado.pecaIA):
    #         label = myfont.render("Eu Venci!!", 1, YELLOW)
    #         screen.blit(label, (40,10))
    #         game_over = True

    #     jogo.printTabuleiro()
    #     draw_board(jogo)

    #     turn += 1
    #     turn = turn % 2

    # if game_over:
    #     pygame.time.wait(3000)