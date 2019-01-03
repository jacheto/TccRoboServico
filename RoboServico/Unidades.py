# Contem as definições do Sistema Internacional de Unidades, para a conversão os valores do computador para o mundo real


# Unidades padrão:

# Metro:
m = 1
# Segundo:
s = 1
# Kilograma:
kg = 1

# constantes
velocidade_som = 343 * m/s
vel_luz = 299792458 * m/s
pi = 3.141592654
e = 2.718281828

# O arrasto universal é uma constante tal que todas as velocidades serão multiplicadas por (1 - ARRASTO_UNIVERSAL) a cada segundo.
# Ou seja, se for 0.1, as velocidades irão diminuir naturalmente em uma taxa de 10% por segundo
ARRASTO_UNIVERSAL = 0.1

# unidades de distancia
um = 10 ** -6 * m
mm = 10 ** -3 * m
cm = 10 ** -2 * m
km = 10 ** 3 * m
pol = 2.54 * cm
ft = 30.48 * cm
milha = 1.60934 * km

rad = 1
deg = 180 / pi * rad

# unidades de tempo
us = 10 ** -6 * s
ms = 10 ** -3 * s
min = 60 * s
hora = 60 * min
dia = 24 * hora
semana = 7 * dia
ano = 365 * dia

# unidades de peso
g = 0.001 * kg
libra = 0.453592 * kg
