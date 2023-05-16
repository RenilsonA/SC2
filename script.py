from websocket_server import WebsocketServer
import math as m
import numpy as np
import mapas
import time

porta = WebsocketServer(port=6660)
pacote_anterior = []
saida_anterior = 0.0
saida = 0.0
contador = 0
level_anterior = 0

def maximo(mapa, nivel):
    uMax = 10
    if mapa == 1:
        uMax = 10
        if nivel == 3:
            uMax = 8
        elif nivel == 4:
            uMax = 8
    if mapa == 2:
        uMax = 10
        if nivel == 2:
            uMax = 9
        elif nivel == 3:
            uMax = 10
        elif nivel == 4:
            uMax = 10
    return uMax


def computacaoInicial(x, y, mapa, nivel, quant, dt, destino_x, destino_y):
    melhorDist = np.inf
    melhorI = 0        
    uMax = maximo(mapa, nivel)
    for i in range(-uMax, uMax + 1, 1):
        valorUI = i / uMax
        minDistance = np.inf
        x1 = x
        y1 = y
        u = valorUI
        for k in range(quant):
            for q in range(len(destino_x)):
                currentDistance = ((-x1 + destino_x[q]) * (-x1 + destino_x[q]) + (-y1 + destino_y[q])*(-y1 + destino_y[q]))
                if currentDistance < minDistance:
                    minDistance = currentDistance
            l12 = mapas.define_equacoes(mapa, nivel, x1, y1, u)
            x1 = x1 + l12[0]*dt
            y1 = y1 + l12[1]*dt
        for j in range(-uMax, uMax + 1, 1):
            valorUJ = j / uMax
            x11 = x1
            y11 = y1
            u = valorUJ
            for k in range(quant):
                for q in range(len(destino_x)):
                    currentDistance = ((-x11 + destino_x[q]) * (-x11 + destino_x[q]) + (-y11 + destino_y[q])*(-y11 + destino_y[q]))
                    if currentDistance < minDistance:
                        minDistance = currentDistance
                l12 = mapas.define_equacoes(mapa, nivel, x11, y11, u)
                x11 = x11 + l12[0]*dt
                y11 = y11 + l12[1]*dt

            if(minDistance < melhorDist):
                melhorDist = minDistance
                melhorI = valorUI#(valorUI + valorUJ) / 2
    return melhorI

def repartir_mensagens(pacote):
    vitorias = int(pacote[0])
    mapa = int(pacote[1])
    nivel = int(pacote[2])
    jogador = pacote[3], pacote[4]
    alvo = pacote[5], pacote[6]
    caixas, caveiras = [], []
    if(len(pacote) > 8):
        caixas.append((pacote[7], pacote[8]))
    if(len(pacote) > 10):
        caixas.append((pacote[9], pacote[10]))
    if(len(pacote) > 12):
        caixas.append((pacote[11], pacote[12]))
        for i in range(14, len(pacote), 1):
            caveiras.append(pacote[i])
    return vitorias, mapa, nivel, jogador, alvo, caixas, caveiras

def cliente(cliente, servidor):
    servidor.send_message(cliente, str(0))

def receber_mensagem(cliente, servidor, pacote):
    global pacote_anterior
    global saida
    global contador
    global level_anterior

    values = [float(x) for x in pacote[:-1].split(",") if x.strip()]
    vitorias, mapa, nivel, jogador, alvo, caixas, caveiras = repartir_mensagens(values)

    if level_anterior != nivel:
        level_anterior = nivel
        saida = 0

    const = mapas.define_equacoes(mapa, nivel, 0, 0, 0, False)
    menor = (jogador[0] - alvo[0]) * (jogador[0] - alvo[0]) + (jogador[1] - alvo[1])*(jogador[1] - alvo[1])
    Tx = []
    Ty = []
    Tx.append(alvo[0])
    Ty.append(alvo[1])
    quant = 50
    dt = 0.01
    limMax = 1.2
    """if(abs(jogador[0]) > limMax or abs(jogador[1]) > limMax):
        print(jogador[0], jogador[1])
        Tx = 0
        Ty = 0
    else:"""
    if(len(caixas) >= 1):
        Tx.append(caixas[0][0])
        Ty.append(caixas[0][1])
        if(len(caixas) >= 2):
            Tx.append(caixas[1][0])
            Ty.append(caixas[1][1])
            if(len(caixas) >= 3):
                Tx.append(caixas[2][0])
                Ty.append(caixas[2][1])
    saida = saida + (const)*computacaoInicial(jogador[0], jogador[1], mapa, nivel, quant, dt, Tx, Ty)
    if abs(saida) >= 1:
        saida = (saida/abs(saida))

    pacote_anterior = values 
    servidor.send_message(cliente, str(saida))

porta.set_fn_new_client(cliente)
porta.set_fn_message_received(receber_mensagem)
porta.run_forever()
