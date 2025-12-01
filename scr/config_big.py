import pygame
import random


# Configuración General de Pygame
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Gato y Ratón – Tablero 11 nodos con queso y meta oculta")

FPS = 60
RELOJ = pygame.time.Clock()
COLOR_FONDO = (175, 195, 120)
COLOR_LINEAS = (80, 50, 20)
COLOR_NODO = (130, 100, 70)
COLOR_INICIO = (100, 150, 70)
COLOR_FINAL = (200, 180, 60)
FUENTE = pygame.font.SysFont("arial", 22)

# Imágenes de las piezas
img_gato = pygame.image.load("./assets/gato.png")
img_raton = pygame.image.load("./assets/ratón.png")
img_queso = pygame.image.load("./assets/queso.png")

ESCALA = 0.12
img_gato = pygame.transform.smoothscale(img_gato, (int(250*ESCALA), int(250*ESCALA)))
img_raton = pygame.transform.smoothscale(img_raton, (int(250*ESCALA), int(250*ESCALA)))
img_queso = pygame.transform.smoothscale(img_queso, (int(200*ESCALA), int(200*ESCALA)))


# Tablero Grande: 25 nodos en una malla cuadrada con diagonales
x0, y0 = 150, 150
dx, dy = 100, 100

# Matriz tipo rejilla 5x5
nodos = {}
id_nodo = 0
for fila in range(5):
    for col in range(5):
        nodos[id_nodo] = (x0 + col * dx, y0 + fila * dy)
        id_nodo += 1

# Conexiones (tipo malla cuadrada)
conexiones = {}
for i in range(25):
    fila, col = divmod(i, 5)
    vecinos = []
    if fila > 0: vecinos.append(i - 5)        # arriba
    if fila < 4: vecinos.append(i + 5)        # abajo
    if col > 0: vecinos.append(i - 1)         # izquierda
    if col < 4: vecinos.append(i + 1)         # derecha
    # diagonales
    if fila > 0 and col > 0: vecinos.append(i - 6)
    if fila > 0 and col < 4: vecinos.append(i - 4)
    if fila < 4 and col > 0: vecinos.append(i + 4)
    if fila < 4 and col < 4: vecinos.append(i + 6)
    conexiones[i] = vecinos

aristas = {tuple(sorted((i, j))) for i, vs in conexiones.items() for j in vs}



# Funciones de Dibujo
def dibujar_tablero(VENTANA, nodos, aristas, inicio, final, tiene_queso, queso):
    VENTANA.fill(COLOR_FONDO)
    for (i, j) in aristas:
        pygame.draw.line(VENTANA, COLOR_LINEAS, nodos[i], nodos[j], 2)

    for i, (x, y) in nodos.items():
        color = COLOR_NODO
        if i == inicio:
            color = COLOR_INICIO
        elif i == final and tiene_queso:
            color = COLOR_FINAL
        pygame.draw.circle(VENTANA, color, (x, y), 8)

    if not tiene_queso:
        qx, qy = nodos[queso]
        VENTANA.blit(img_queso, (qx - 10, qy - 10))


def dibujar_piezas(VENTANA, nodos, pos_gato, pos_raton):
    gx, gy = nodos[pos_gato]
    rx, ry = nodos[pos_raton]
    VENTANA.blit(img_gato, (gx - 12, gy - 12))
    VENTANA.blit(img_raton, (rx - 12, ry - 12))


def mover_pieza(pos_actual, tecla, nodos, conexiones):
    if tecla not in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                     pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_c]:
        return pos_actual

    x0, y0 = nodos[pos_actual]
    destino = pos_actual

    for v in conexiones[pos_actual]:
        x1, y1 = nodos[v]
        dx_, dy_ = x1 - x0, y1 - y0

        # Flechas
        if tecla == pygame.K_LEFT and dx_ < 0 and abs(dy_) < 10:
            destino = v
        elif tecla == pygame.K_RIGHT and dx_ > 0 and abs(dy_) < 10:
            destino = v
        elif tecla == pygame.K_UP and dy_ < 0 and abs(dx_) < 10:
            destino = v
        elif tecla == pygame.K_DOWN and dy_ > 0 and abs(dx_) < 10:
            destino = v
        # Diagonales
        elif tecla == pygame.K_q and dx_ < 0 and dy_ < 0:
            destino = v
        elif tecla == pygame.K_e and dx_ > 0 and dy_ < 0:
            destino = v
        elif tecla == pygame.K_z and dx_ < 0 and dy_ > 0:
            destino = v
        elif tecla == pygame.K_c and dx_ > 0 and dy_ > 0:
            destino = v

    return destino


def mostrar_texto(txt, y=20):
    VENTANA.blit(FUENTE.render(txt, True, (0, 0, 0)), (20, y))


def cartel(texto, color=(255, 200, 200)):
    VENTANA.fill(color)
    render = FUENTE.render(texto, True, (0, 0, 0))
    VENTANA.blit(render, (ANCHO//2 - render.get_width()//2, ALTO//2))
    pygame.display.flip()
    pygame.time.wait(2000)
