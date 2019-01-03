# Essa biblioteca irá conter funções e classes fundamentais de algebra linear úteis para
# todos os outros módulos



import math
from Unidades import *

# Classe ponto, muito utilizada nos outro módulos
class Point:
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y
    # Permite tranformar uma tupla em ponto
    def setFromTuple(self, tup):
        self.x = tup[0]
        self.y = tup[1]
        return self
    # Adiciona outro ponto, equivalente a somar dois vetores que começam na origem.
    def add(self, p):
        self.x += p.x
        self.y += p.y
        return self
    # Subtrai outro ponto, equivalente a somar dois vetores que começam na origem.
    def sub(self, p):
        self.x -= p.x
        self.y -= p.y
        return self
    # Subtrai o ponto por um valor escalar.
    def mult(self, k):
        self.x *= k
        self.y *= k
        return self
    # Converte os valores do ponto (x, y) nos números inteiros mais próximos.
    def cint(self):
        self.x = int(self.x)
        self.y = int(self.y)
        return self
    # Converte o ponto em tupla.
    def tuple(self):
        return (self.x, self.y)
    # retorna a hipotenusa do ponto
    def dist(self):
        return math.hypot(self.x, self.y)

# O vetor é constituido por dois pontos
class Vector:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    # Altera o vetor, deslocando-o para a origem
    def abs(self):
        self.p2.sub(self.p1)
        self.p1 = Point(0, 0)
        return self
    # Soma com outro vetor.
    def add(self, v):
        self.p2.add(v.abs().pi)
    # Subtrai com outro vetor.
    def sub(self, v):
        self.p2.sub(v.abs().pi)

# Função calcula se dois segmentos se intersectam no espaço
# Parâmetros: dois vetores
# Retorno:  Se intersecta, retorna o ponto de intersecção
#           Se não intersecta, retorna Falso

def intersect(v1, v2):
    r = Point(v1.pf.x - v1.pi.x, v1.pf.y - v1.pi.y)
    s = Point(v2.pf.x - v2.pi.x, v2.pf.y - v2.pi.y)
    g = Point(v2.pi.x - v1.pi.x, v2.pi.y - v1.pi.y)
    a1 = cross(g, s)
    a2 = cross(g, r)
    a3 = cross(r, s)
    if(a3 != 0):
        ta = a1 / a3
        tb = a2 / a3
    else:
        return False
    if 0 < ta < 1 and 0 < tb < 1:
        return Point(v1.pi.x + ta * r.x, v1.pi.y + ta * r.y)
    else:
        return False

# Função para adicionar pontos (sem alterá-los)
def PointAdd(p1, p2):
    return Point(p1.x + p2.x, p1.y + p2.y)

# Função para subtrair pontos (sem alterá-los)
def PointSub(p1, p2):
    return Point(p1.x - p2.x, p1.y - p2.y)

# Função para multiplicar pontos (sem alterá-los)
def PointMult(p1, k):
    return Point(p1.x * k, p1.y * k)

# Retorna o ponto P2 ao deslocar o vetor de modo que P1 fique na origem
def VectorAbs(v1):
    return PointSub(v1.p2, v1.p1)

# Função para adicionar vetores (sem alterá-los)
def VectorAdd(v1, v2):
    return Vector(v1.p1, PointAdd(v1.p2, v2.abs().p2))

# Função para subtrair vetores (sem alterá-los)
def VectorAdd(v1, v2):
    return Vector(v1.p1, PointSub(v1.p2, v2.abs().p2))

# calcula a distância entre 2 pontos
def dist(p1, p2):
    return math.hypot(p2.x - p1.x, p2.y - p1.y)

# faz o produto vetorial entre dois pontos (considerando que são vetores que começam em (0, 0))
def cross(p1, p2):
    return p1.x * p2.y - p1.y * p2.x

# faz o produto escalar entre dois pontos (considerando que são vetores que começam em (0, 0))
def dot(p1, p2):
    return p1.x * p2.x + p1.y * p2.y

# retorna o ponto normalizado, ou seja, um ponto com a mesma direção porém com módulo 1
def norm(p):
    nx = p.x/p.d if p.d!=0 else 0
    ny = p.y/p.d if p.d!=0 else 0
    return Point(nx, ny)