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

def computacaoInicial(x, y, mapa, nivel, quant, dt, destino_x, destino_y):
    melhorDist = np.inf
    melhorI = 0        
    uMax = 10
    for i in range(-uMax, uMax, 1):
        for j in range(-uMax, uMax, 1):
            valorUI = i / uMax
            valorUJ = j / uMax
            minDistance = np.inf
            x1 = x
            y1 = y
            u = valorUI
            for k in range(quant):
                currentDistance = m.sqrt((-x1 + destino_x) * (-x1 + destino_x) + (-y1 + destino_y)*(-y1 + destino_y))
                if currentDistance < minDistance:
                    minDistance = currentDistance
                l12 = mapas.define_equacoes(mapa, nivel, x1, y1, u)
                x1 = x1 + l12[0]*dt
                y1 = y1 + l12[1]*dt
                
            u = valorUJ
            for k in range(quant):
                currentDistance = m.sqrt((-x1 + destino_x) * (-x1 + destino_x) + (-y1 + destino_y)*(-y1 + destino_y))
                if currentDistance < minDistance:
                    minDistance = currentDistance
                l12 = mapas.define_equacoes(mapa, nivel, x1, y1, u)
                x1 = x1 + l12[0]*dt
                y1 = y1 + l12[1]*dt

            if(minDistance < melhorDist):
                melhorDist = minDistance
                melhorI = valorUI
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
    Tx = alvo[0]
    Ty = alvo[1]
    quant = 250
    dt = 0.01
    limMax = 1.2
    if(len(caixas) >= 1 and mapa != 3):
        if((jogador[0] - caixas[0][0]) * (jogador[0] - caixas[0][0]) + (jogador[1] - caixas[0][1])*(jogador[1] - caixas[0][1]) < 4*menor):
            menor = (jogador[0] - caixas[0][0]) * (jogador[0] - caixas[0][0]) + (jogador[1] - caixas[0][1])*(jogador[1] - caixas[0][1])
            Tx = caixas[0][0]
            Ty = caixas[0][1]
        if(len(caixas) >= 2):
            if((jogador[0] - caixas[1][0]) * (jogador[0] - caixas[1][0]) + (jogador[1] - caixas[1][1])*(jogador[1] - caixas[1][1]) < 4*menor):
                menor = (jogador[0] - caixas[1][0]) * (jogador[0] - caixas[1][0]) + (jogador[1] - caixas[1][1])*(jogador[1] - caixas[1][1])
                Tx = caixas[1][0]
                Ty = caixas[1][1]
            if(len(caixas) >= 3):
                if((jogador[0] - caixas[2][0]) * (jogador[0] - caixas[2][0]) + (jogador[1] - caixas[2][1])*(jogador[1] - caixas[2][1]) < 4*menor):
                    menor = (jogador[0] - caixas[2][0]) * (jogador[0] - caixas[2][0]) + (jogador[1] - caixas[2][1])*(jogador[1] - caixas[2][1])
                    Tx = caixas[2][0]
                    Ty = caixas[2][1]
    saida = saida + (const)*computacaoInicial(jogador[0], jogador[1], mapa, nivel, quant, dt, Tx, Ty)
    if abs(saida) >= 1:
        saida = (saida/abs(saida))

    pacote_anterior = values 
    servidor.send_message(cliente, str(saida))

porta.set_fn_new_client(cliente)
porta.set_fn_message_received(receber_mensagem)
porta.run_forever()
