# Esta classe será um dos centros da arquitetura do robô.
# Seu papel principal será simular o comportamento do robô no ambiente
# Todos os elementos de ambiente (inputs do sensor) serão modelados aqui e o robô
# Ela será responsável por simular o robô no ambiente, prevendo seu comportamento utilizando os inputs de todos os sensores e enviando para o output


from Unidades import *
from Geometria import *
import Render
import Cores as cor
import Objetos
import random

# Função principal do código até agora
def main():

    # Seta os parâmetros iniciais
    esc = 1 * cm
    # frames por segundo do modelo, essa será a unidade de tempo padrão da simulação
    fps = 30
    monitor = Render.Monitor(14 * pol, 1366, 768, esc, True)
    render = Render.render((800, 600), cor.darkSlateGray, fps, monitor)
    render.pontoZero = Point(400, 300)
    objectList = []

    # Cria alguns cilindros aleatoriamente na tela para testar
    for _ in range(1000):
        robo = Objetos.Cilindro((random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255)), random.randrange(1, 200) * cm, 2 * cm, 3 * kg)
        random.seed()
        robo.pos = Point(random.randrange(-10000, 10000)*cm, random.randrange(-10000, 10000)*cm)
        robo.vel = Point(random.randrange(-50, 50)*mm, random.randrange(-50, 50)*mm)
        objectList.append(robo)

    # Cria o robô
    robo = Objetos.Robo((0, 0, 0), 10 * cm, 2 * cm, 3 * kg)
    objectList.append(robo)

    t = 0
    running = True

    # Loop principal do modelo

    while running:
        for obj in objectList:
            obj.atualizarDinamica(fps)
            render.desenhar(obj)
        running = render.atualizar()
        t += 1/fps


# Primeira função a ser rodada, apenas redireciona para a main

if __name__ == "__main__":
    main()