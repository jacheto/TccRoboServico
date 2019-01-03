# Essa classe irá conter a interpretação dos dados dos sensores do robô.
# Ela será responsável por fazer a ponte entre os dados dos sensores e o input para a simulação do modelo do robô

from Geometria import *
from Unidades import *
SENSOR_DISTANCIA = 1


class Sensor:
    def __init__(self, posicaoRobo, frequenciaMedicao, freqOffset = 0):
        self.tipoSensor = None
        self.posicaoRobo = posicaoRobo
        self.frequenciaMedicao = frequenciaMedicao
        self.frequenciaOffset = freqOffset

class SensorDistancia(Sensor):
    def __init__(self, posicaoRobo, frequenciaMedicao, freqOffset = 0):
        self.__init__(posicaoRobo, frequenciaMedicao, freqOffset)
        self.tipoSensor = SENSOR_DISTANCIA
        self.distanciaObtida = None

    def ObterDistancia(self):
        self.distanciaObtida = 10 * cm


