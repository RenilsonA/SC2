from websocket_server import WebsocketServer
import math as m
import numpy as np
import mapas
import time

porta = WebsocketServer(port=6660)
pacote_anterior = []
saida_anterior = 0.0
saida = 0.0
dt = 0.02

def checarU(mapa, nivel):
    if(mapa == 2):
        return 8
    else:
        return 10

def computacaoInicial(x, y, mapa, nivel, profundidade, dt, alvo_x, alvo_y):
    melhorDist = np.inf     #minDistance
    melhorI = 0             #bestControlSignal
    uMax = checarU(mapa, nivel)
    for i in range(-uMax, uMax, 1):
        for j in range(-uMax, uMax, 1):
            valorUI = i / 10.0
            valorUJ = j / 10.0
            minDistance = np.inf
            positions = []
            vatorU = [valorUI, valorUJ]
            uLength = len(vatorU)
            vatorU.append(vatorU[uLength-1])
            x1 = x
            y1 = y
            for k in range(profundidade):
                currentDistance = m.sqrt((x1 - alvo_x) * (x1 - alvo_x) + (y1 - alvo_y)*(y1 - alvo_y))
                if currentDistance < minDistance:
                    minDistance = currentDistance
                uIndex = m.floor(uLength * k / profundidade)
                u = vatorU[uIndex]
                xp = mapas.define_equacoes(mapa, nivel, x1, y1, u)
                x1 = x1 + xp[0]*dt
                y1 = y1 + xp[1]*dt
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
    global dt

    values = [float(x) for x in pacote[:-1].split(",") if x.strip()]
    vitorias, mapa, nivel, jogador, alvo, caixas, caveiras = repartir_mensagens(values)

    if pacote_anterior != values:
        const = mapas.define_equacoes(mapa, nivel, 0, 0, 0, False)
        menor = (jogador[0] - alvo[0]) * (jogador[0] - alvo[0]) + (jogador[1] - alvo[1])*(jogador[1] - alvo[1])
        Tx = alvo[0]
        Ty = alvo[1]
        limMax = 0.9
        """if(abs(jogador[0]) > limMax or abs(jogador[1]) > limMax):
            Tx = -jogador[0]
            Ty = -jogador[1]"""
        if(len(caixas) > 1 and mapa != 2):
            if((jogador[0] - caixas[0][0]) * (jogador[0] - caixas[0][0]) + (jogador[1] - caixas[0][1])*(jogador[1] - caixas[0][1]) < menor):
                menor = (jogador[0] - caixas[0][0]) * (jogador[0] - caixas[0][0]) + (jogador[1] - caixas[0][1])*(jogador[1] - caixas[0][1])
                Tx = caixas[0][0]
                Ty = caixas[0][1]
            if(len(caixas) > 2):
                if((jogador[0] - caixas[1][0]) * (jogador[0] - caixas[1][0]) + (jogador[1] - caixas[1][1])*(jogador[1] - caixas[1][1]) < menor):
                    menor = (jogador[0] - caixas[1][0]) * (jogador[0] - caixas[1][0]) + (jogador[1] - caixas[1][1])*(jogador[1] - caixas[1][1])
                    Tx = caixas[1][0]
                    Ty = caixas[1][1]
                if(len(caixas) > 3):
                    if((jogador[0] - caixas[2][0]) * (jogador[0] - caixas[2][0]) + (jogador[1] - caixas[2][1])*(jogador[1] - caixas[2][1]) < menor):
                        menor = (jogador[0] - caixas[2][0]) * (jogador[0] - caixas[2][0]) + (jogador[1] - caixas[2][1])*(jogador[1] - caixas[2][1])
                        Tx = caixas[2][0]
                        Ty = caixas[2][1]
        saida = const*saida + (1 - const)*computacaoInicial(jogador[0], jogador[1], mapa, nivel, 20, dt, Tx, Ty)
        if saida >= 1:
            saida = 0.9
        if saida <= -1:
            saida = -0.9
    else:
        saida = 0

    #saida_anterior = saida
    pacote_anterior = values 
    servidor.send_message(cliente, str(saida))
    time.sleep(0.01)

porta.set_fn_new_client(cliente)
porta.set_fn_message_received(receber_mensagem)
porta.run_forever()
