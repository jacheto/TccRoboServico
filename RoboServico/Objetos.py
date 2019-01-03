# Responsável pelas propriedades físicas dos objetos, necessário para a simulação.

from Geometria import *
from Unidades import *
from Constantes import *
import Render

# Contém métodos genéricos de uma forma geométrica em 2D, necessários para a renderização dos corpos
class Forma():
    def __init__(self, cor, tipo):
        self.tipo = tipo
        self.cor = cor

# Contém os métodos exclusivos de um Circulo
class Circulo(Forma):
    def __init__(self, cor, raio):
        super().__init__(cor, TF_CIRCULO)
        self.raio = raio

# Contém os métodos exclusivos de um Retângulo
class Rect(Forma):
    def __init__(self, cor, w, h):
        super().__init__(cor, TF_RECT)
        self.w = w
        self.h = h

# Contém os métodos exclusivos de uma Linha
class Linha(Forma):
    def __init__(self, cor, d, ang):
        super().__init__(cor, TF_LINHA)
        self.d = d
        self.ang = ang

# Contém os métodos exclusivos de um Polígono convexo
class Poligono(Forma):
    def __init__(self, cor, listaPontos):
        super().__init__(cor, TF_POLIGONO)
        self.listaPontos = listaPontos

# Contém os métodos exclusivos de um Ponto
class Ponto(Forma):
    def __init__(self, cor, tamanho):
        super().__init__(cor, TF_PONTO)
        self.tamanho = tamanho



# Contém os métodos gerais de um corpo rígido
class Objeto():
    def __init__(self, massa, forma):
        self.massa = massa
        self.forma = forma
        self.pos = Point(0, 0)
        self.vel = Point(0, 0)
        self.acel = Point(0, 0)
        self.ang = 0
        self.ang_vel = 0
        self.ang_acel = 0
        self.momento = Point(0, 0)

    def atualizarDinamica(self, fps):
        self.vel.add(self.acel).mult(1 - ARRASTO_UNIVERSAL/fps)
        self.pos.add(self.vel)
        self.ang_vel += self.ang_acel
        self.ang += self.ang_vel
        self.momento = PointMult(self.vel, self.massa)

# Contém os métodos exclusivos de um cilindro
class Cilindro(Objeto):
    def __init__(self, cor, diametro, altura, massa):
        self.massa = massa
        self.diametro = diametro
        self.altura = altura
        raio = diametro / 2
        self.volume = pi * raio ** 2 * altura
        self.densidade = self.massa / self.volume
        self.Iz = self.massa * raio ** 2 / 2
        forma = Circulo(cor, raio)
        super().__init__(massa, forma)

# Classe que contém os métodos exclusivos do robô
class Robo(Cilindro):
    def __init__(self, cor, diametro, altura, massa):
        super().__init__(cor, diametro, altura, massa)
