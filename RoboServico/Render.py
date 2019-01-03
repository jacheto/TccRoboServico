# Classe que contém a Engine gráfica para a iteração com o usuário.
# Inicialmente foi utilizado o pygame.
# Nessa classe é feita a conversão de medidas do mundo real para pixels na tela, e vice-versa.


import pygame
import math
import Cores as cor
from Geometria import *
from Unidades import *
from Constantes import *

# Classe que define as configurações de escala do monitor
class Monitor:
    def __init__(self, tamanhoMonitor, definicaoX, definicaoY, escala, usarEscalaReal):
        self.tamanhoMonitor = tamanhoMonitor
        self.definicaoX = definicaoX
        self.definicaoY = definicaoY

        if usarEscalaReal:
            self.proporcao = definicaoY / definicaoX
            tamanhoX = tamanhoMonitor / (self.proporcao ** 2 + 1) ** 0.5
            self.pixelPorMetro = definicaoX / tamanhoX
        else:
            self.pixelPorMetro = 1

        self.atualizarEscala(escala)

    def atualizarEscala(self, escala):
        if(escala < 1*mm):
            self.escala = 1*mm
        elif(escala > 1*m):
            self.escala = 1*m
        else:
            self.escala = escala

        self.pxs = int(self.pixelPorMetro * self.escala)

# Classe que contém uma versão renderizável de uma Figura genérica (ver Objetos.py)
class FrameObject():
    def __init__(self, color, pz, pxs, x, y, width):
        self.color = color
        self.width = width
        self.pontoZero = pz
        self.pxs = pxs
        self.pos = self.m2px_point(x, y)

    # converte ponto no espaço de metros para pixels
    def m2px_point(self, x, y):
        return Point(x, y).mult(self.pxs).add(self.pontoZero).cint().tuple()

    # converte dimensão de metro para pixels
    def m2px_value(self, value):
        return int(value * self.pxs)

# Classe que contém uma versão renderizável de um círculo
class FrameCircle(FrameObject):
    def __init__(self, color, pz, pxs, x, y, radius, width):
        super().__init__(color, pz, pxs, x, y, width)
        self.radius = self.m2px_value(radius)
        
    def render(self, screen):
        if math.hypot(self.pos[0], self.pos[1])-self.radius < 1000:
            pygame.draw.circle(screen, self.color, self.pos, self.radius, self.width)


# Classe que contém uma versão renderizável de um ponto
class FramePoint(FrameObject):
    def __init__(self, color, pz, pxs, x, y, size):
        super().__init__(color, pz, pxs, x, y, 0)
        self.size = size

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size, self.width)


# Classe que contém uma versão renderizável de uma linha
class FrameLine(FrameObject):
    def __init__(self, color, pz, pxs, x, y, d, ang, width, AA):
        super().__init__(color, pz, pxs, x, y, width)
        self.p_i = self.m2px_point(x, y)
        self.p_f = self.m2px_point(x + d * math.cos(ang), y + d * math.sin(ang))
        self.AA = AA
        
    def render(self, screen):
        if self.AA:
            pygame.draw.aaline(screen, self.color, self.p_i, self.p_f, 5)
        else:
            pygame.draw.line(screen, self.color, self.p_i, self.p_f, self.width)

# Classe que contém uma versão renderizável de um retângulo
class FrameRect(FrameObject):
    def __init__(self, color, pz, pxs, x, y, w, h, width):
        super().__init__(color, pz, pxs, x, y, width)
        self.rect = (self.pos[0], self.pos[1], self.m2px_value(w), self.m2px_value(h))
        
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.width)

# Classe que contém uma versão renderizável de um polígono
class FramePolygon(FrameObject):
    def __init__(self, color, pz, pxs, x, y, points, width):
        super().__init__(color, pz, pxs, x, y, width)
        self.points = []
        p0 = Point(x, y)
        for p in points:
            p.add(p0)
            self.points.append(self.m2px_point(p.x, p.y))
            
    def render(self, screen):
        pygame.draw.polygon(screen, self.color, self.points, self.width)

# Retorna a posição do mouse
def getMousePos():
    return Point().setFromTuple(pygame.mouse.get_pos())

# Retorna a velocidade do mouse
def getMouseVel():
    return Point().setFromTuple(pygame.mouse.get_rel())


# Classe que contém o motor gráfico da simulação, responsável pela renderização dos objetos na tela
class render:
    def __init__(self, dimensoesJanela, corFundo, fps, monitor):
        self.WIDTH = dimensoesJanela[0]
        self.HEIGH = dimensoesJanela[1]
        self.monitor = monitor
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(dimensoesJanela)
        self.corFundo = corFundo
        self.pontoZero = Point(0, 0)
        self.pontoCentro = Point(self.WIDTH/2, self.HEIGH/2)
        self.frameObjects = []
        self.fps = fps
        self.drag = False
        self.scaleUpdate = 0
        self.scaleUpdateRate = 0.1
        self.cameraPos = Point(0, 0)
        pygame.init()
        global s
        s = 1 / fps

    # Redireciona o objeto conforme sua forma para a criação de sua versão renderizável
    def desenhar(self, objeto):
        if objeto.forma.tipo == TF_CIRCULO:
            self.desenharCirculo(objeto.forma.cor, objeto.pos.x, objeto.pos.y, objeto.forma.raio, 0)
        elif objeto.forma.tipo == TF_PONTO:
            self.desenharPonto(objeto.forma.cor, objeto.pos.x, objeto.pos.y, objeto.forma.tamanho)
        elif objeto.forma.tipo == TF_LINHA:
            self.desenharLinha(objeto.forma.cor, objeto.pos.x, objeto.pos.y, objeto.forma.d, objeto.forma.ang, 0)
        elif objeto.forma.tipo == TF_RECT:
            self.desenharRect(objeto.forma.cor, objeto.pos.x, objeto.pos.y, objeto.forma.w, objeto.forma.h, 0)
        elif objeto.forma.tipo == TF_POLIGONO:
            self.desenharPoligono(objeto.forma.cor, objeto.pos.x, objeto.pos.y, objeto.forma.listaPontos, 0)

    # Cria uma versão renderizável de um círculo a partir dos dados de sua forma
    def desenharCirculo(self, cor, x, y, raio, espessura=0):
        forma = FrameCircle(cor, self.pontoZero, self.monitor.pxs, x, y, raio, espessura)
        self.frameObjects.append(forma)

    # Cria uma versão renderizável de um ponto a partir dos dados de sua forma
    def desenharPonto(self, cor, x, y, tamanho):
        forma = FramePoint(cor, self.pontoZero, self.monitor.pxs, x, y, tamanho)
        self.frameObjects.append(forma)

    # Cria uma versão renderizável de uma linha a partir dos dados de sua forma
    def desenharLinha(self, cor, x, y, d, ang, espessura=1, AA=False):
        forma = FrameLine(cor, self.pontoZero, self.monitor.pxs, x, y, d, ang, espessura, AA)
        self.frameObjects.append(forma)

    # Cria uma versão renderizável de um retângulo a partir dos dados de sua forma
    def desenharRect(self, cor, x, y, largura, altura, espessura=0):
        forma = FrameRect(cor, self.pontoZero, self.monitor.pxs, x, y, largura, altura, espessura)
        self.frameObjects.append(forma)

    # Cria uma versão renderizável de um polígono a partir dos dados de sua forma
    def desenharPoligono(self, cor, x, y, listaPontos, espessura=0):
        forma = FramePolygon(cor, self.pontoZero, self.monitor.pxs, x, y, listaPontos, espessura)
        self.frameObjects.append(forma)

    # Escreve um texto na tela
    def escrever(self, text, posX, posY, size):
        largeText = pygame.font.Font('freesansbold.ttf', size)
        TextSurf = largeText.render(text, True, cor.black)
        TextRect = TextSurf.get_rect()
        TextRect.center = (posX, posY)
        self.screen.blit(TextSurf, TextRect)


    # Renderiza todos os objetos na tela no frame atual
    # A fazer: Segregar essa função entre:
    # 1- captura de inputs do usuário (teclado e mouse)
    # 2- renderização dos objetos
    # 3- criação do HUD (linhas de escala + textos)
    def atualizar(self):
        executando = True

        self.scaleUpdate = 0

        # Capturando os inputs do usuário

        mouseVel = getMouseVel()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drag = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.drag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.scaleUpdate = 1
                if event.button == 4:
                    self.scaleUpdate = -1

        # Tratando os inputs do usuário

        if self.drag:
            self.pontoZero.add(mouseVel)
            self.cameraPos.sub(mouseVel)

        if self.scaleUpdate != 0:
            ponto_ref = PointSub(self.pontoCentro, self.pontoZero)
            scaleChange = (1 + self.scaleUpdateRate) ** self.scaleUpdate

            p1 = PointMult(ponto_ref, 1/self.monitor.pxs)
            self.monitor.atualizarEscala(self.monitor.escala / scaleChange)
            p2 = PointMult(ponto_ref, 1/self.monitor.pxs)

            self.pontoZero.add(PointMult(PointSub(p2, p1), self.monitor.pxs))

        # Renderizando os objetos na tela

        self.screen.fill(self.corFundo)

        for object in self.frameObjects:
            object.render(self.screen)

        # Desneho do HUD

        quantY = 0
        escalaGrid = 1
        maxY = 40
        minY = 3
        pulo = 10
        while quantY*2 >= maxY or quantY*2 <= minY:
            space = self.monitor.pxs * m * escalaGrid
            quantX = int(self.WIDTH / space / 2)
            quantY = int(self.HEIGH / space / 2)
            if quantY*2 <= minY:
                escalaGrid /= pulo
            if quantY*2 >= maxY:
                escalaGrid *= pulo
        centroX, centroY = int(self.WIDTH/2), int(self.HEIGH/2)
        offsetX, offsetY = -int(( self.pontoZero.x - centroX ) / space), -int(( self.pontoZero.y - centroY ) / space)
        for n in range(-quantX+offsetX-3, quantX+offsetX+3):
            pygame.draw.line(self.screen, cor.darkGray, (self.pontoZero.x + n * space, 0), (self.pontoZero.x + n * space, self.HEIGH), 1)
        for n in range(-quantY+offsetY-3, quantY+1+offsetY+3):
            pygame.draw.line(self.screen, cor.darkGray, (0, self.pontoZero.y + n * space), (self.WIDTH, self.pontoZero.y + n * space), 1)

        # Esvaziando os frameObjects para o próximo frame

        self.frameObjects = []

        # Update do pygame (tela e fps)

        pygame.display.update()
        self.clock.tick(self.fps)

        return executando