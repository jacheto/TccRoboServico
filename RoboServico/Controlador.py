# Contém a programação de controle das partes mecânicas e elétricas do robô de maneira que o input do Modelo seja alcançado na vida real
# Serve como ponte da comunicação dos sinais do modelo para os comandos dos motores

DIR_FRENTE = 1
DIR_TRAS = -1


class Motor:
    def __init__(self):
        self.velocidade = 0
        self.aceleracao = 0
        self.contadorEncoder = 0

def main():
    MotorE = Motor()
    MotorD = Motor()

def Avancar(metros):
    pass

def Girar(graus):
    pass

def Parar():
    pass

def SeguirCaminho(posicao):
    pass
