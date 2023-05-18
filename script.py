from websocket_server import WebsocketServer
import numpy as np
import mapas

porta = WebsocketServer(port=6660)
passou = 0
saida = 0.0
contador = 0
level_anterior = 0

def maximo(mapa, nivel):
    uMax = 10
    if mapa == 1:
        if nivel == 3:
            uMax = 8
        elif nivel == 4:
            uMax = 8
    if mapa == 2:
        if nivel == 2:
            uMax = 10
        elif nivel == 3:
            uMax = 9
        elif nivel == 4:
            uMax = 10
    if mapa == 3:
        if nivel == 2:
            uMax = 8
        if nivel == 4:
            uMax = 8
    if mapa == 4:
        if nivel == 1:
            uMax = 8
        elif nivel == 3:
            uMax = 8
        elif nivel == 4:
            uMax = 10
    return uMax


def Colisao(X, Y, CaveirasX, CaveirasY):
    for i in CaveirasX:
        if ((i - 0.1 <= X) and (i + 0.1 <= X)):
            for j in CaveirasY:
                if ((j - 0.1 <= Y) and (j + 0.1 <= Y)):
                    return True
    return False

def computacaoInicial(x, y, mapa, nivel, quant, dt, ObjetivosX, ObjetivosY, CaveirasX, CaveirasY):
    melhorDist = np.inf
    melhorI = 0        
    uMax = maximo(mapa, nivel)
    for i in range(-uMax, uMax + 1):
        valorUI = i / uMax
        distMinima = np.inf
        distancia = np.inf
        x1 = x
        y1 = y
        u = valorUI
        for k in range(quant):
            for q in range(len(ObjetivosX)):
                f = 1 if q == 0 else 2
                distancia = f*((x1 - ObjetivosX[q])*(x1 - ObjetivosX[q]) + (y1 - ObjetivosY[q])*(y1 - ObjetivosY[q]))
                if (distancia < distMinima):
                    distMinima = distancia
            l12 = mapas.define_equacoes(mapa, nivel, x1, y1, u)
            x1 += l12[0]*dt
            y1 += l12[1]*dt
            if(distMinima < melhorDist):
                melhorDist = distMinima
                melhorI = valorUI
        for j in range(-uMax, uMax + 1):
            valorUJ = j / uMax
            x11 = x1
            y11 = y1
            u = valorUJ
            for k in range(quant):
                for q in range(len(ObjetivosX)):
                    f = 1 if q == 0 else 2
                    distancia = f*(x11 - ObjetivosX[q])*(x11 - ObjetivosX[q]) + (y11 - ObjetivosY[q])*(y11 - ObjetivosY[q])
                    if (distancia < distMinima): 
                        distMinima = distancia
                l12 = mapas.define_equacoes(mapa, nivel, x11, y11, u)
                x11 += l12[0]*dt
                y11 += l12[1]*dt

                if(distMinima < melhorDist):
                    melhorDist = distMinima
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
        for i in range(13, len(pacote), 2):
            caveiras.append((pacote[i], pacote[i+1]))
    return vitorias, mapa, nivel, jogador, alvo, caixas, caveiras

def cliente(cliente, servidor):
    servidor.send_message(cliente, str(0))

def receber_mensagem(cliente, servidor, pacote):
    global saida
    global contador
    global level_anterior
    global passou

    values = [float(x) for x in pacote[:-1].split(",") if x.strip()]
    vitorias, mapa, nivel, jogador, alvo, caixas, caveiras = repartir_mensagens(values)

    if level_anterior != nivel:
        print("Quantidade de fases passadas:", passou)
        passou += 1
        level_anterior = nivel
        saida = 0

    k = mapas.define_equacoes(mapa, nivel, 0, 0, 0, False)
    CaveirasX = []
    CaveirasY = []
    ObjetivosX = []
    ObjetivosY = []
    ObjetivosX.append(alvo[0])
    ObjetivosY.append(alvo[1])
    quant = 50
    dt = 0.01
    if(len(caixas) >= 1 and nivel != 3):
        ObjetivosX.append(caixas[0][0])
        ObjetivosY.append(caixas[0][1])
        if(len(caixas) >= 2):
            ObjetivosX.append(caixas[1][0])
            ObjetivosY.append(caixas[1][1])
            if(len(caixas) >= 3):
                ObjetivosX.append(caixas[2][0])
                ObjetivosY.append(caixas[2][1])
    if(len(caveiras) >= 1):
        CaveirasX.append(caveiras[0][0])
        CaveirasY.append(caveiras[0][1])
        if(len(caveiras) >= 2):
            CaveirasX.append(caveiras[1][0])
            CaveirasY.append(caveiras[1][1])
            if(len(caveiras) >= 3):
                CaveirasX.append(caveiras[2][0])
                CaveirasY.append(caveiras[2][1])
    saida = saida + (k)*computacaoInicial(jogador[0], jogador[1], mapa, nivel, quant, dt, ObjetivosX, ObjetivosY, CaveirasX, CaveirasY)
    if abs(saida) >= 1:
        saida = (saida/abs(saida))

    servidor.send_message(cliente, str(saida))

porta.set_fn_new_client(cliente)
porta.set_fn_message_received(receber_mensagem)
porta.run_forever()
