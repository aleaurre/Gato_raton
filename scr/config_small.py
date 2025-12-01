import pygame
import random
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


# Imágenes
img_gato = pygame.image.load("./assets/gato.png")
img_raton = pygame.image.load("./assets/ratón.png")
img_queso = pygame.image.load("./assets/queso.png")

ESCALA = 0.15
img_gato = pygame.transform.smoothscale(img_gato, (int(250*ESCALA), int(250*ESCALA)))
img_raton = pygame.transform.smoothscale(img_raton, (int(250*ESCALA), int(250*ESCALA)))
img_queso = pygame.transform.smoothscale(img_queso, (int(200*ESCALA), int(200*ESCALA)))


# Tablero 11 nodos – Estructura más pequeña y simple
x0, y_mid = 150, 300
dx, dy = 100, 100

nodos = {
    0: (x0, y_mid),
    1: (x0+dx, y_mid-dy),
    2: (x0+dx, y_mid),
    3: (x0+dx, y_mid+dy),
    4: (x0+2*dx, y_mid-dy),
    5: (x0+2*dx, y_mid),
    6: (x0+2*dx, y_mid+dy),
    7: (x0+3*dx, y_mid-dy),
    8: (x0+3*dx, y_mid),
    9: (x0+3*dx, y_mid+dy),
    10: (x0+4*dx, y_mid),
}

conexiones = {
    0: [1, 2, 3],
    1: [0, 2, 4, 5],
    2: [0, 1, 3, 5],
    3: [0, 2, 5, 6],
    4: [1, 5, 7],
    5: [1, 2, 3, 4, 6, 7, 8, 9],
    6: [3, 5, 9],
    7: [4, 5, 8, 10],
    8: [5, 7, 9, 10],
    9: [5, 6, 8, 10],
    10: [7, 8, 9],
}
aristas = {tuple(sorted((i, j))) for i, vs in conexiones.items() for j in vs}


# Funciones de Dibujo
def dibujar_tablero(VENTANA, nodos, aristas, inicio, final, tiene_queso, queso):
    VENTANA.fill(COLOR_FONDO)
    for (i, j) in aristas:
        pygame.draw.line(VENTANA, COLOR_LINEAS, nodos[i], nodos[j], 3)

    for i, (x, y) in nodos.items():
        color = COLOR_NODO
        if i == inicio:
            color = COLOR_INICIO
        elif i == final and tiene_queso:
            color = COLOR_FINAL
        pygame.draw.circle(VENTANA, color, (x, y), 9)

    if not tiene_queso:
        qx, qy = nodos[queso]
        VENTANA.blit(img_queso, (qx - 15, qy - 15))


def dibujar_piezas(VENTANA, nodos, pos_gato, pos_raton):
    gx, gy = nodos[pos_gato]
    rx, ry = nodos[pos_raton]
    VENTANA.blit(img_gato, (gx - 15, gy - 15))
    VENTANA.blit(img_raton, (rx - 15, ry - 15))


def mover_pieza(pos_actual, tecla, nodos, conexiones):
    if tecla not in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                     pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_c]:
        return pos_actual

    x0, y0 = nodos[pos_actual]
    destino = pos_actual

    for v in conexiones[pos_actual]:
        x1, y1 = nodos[v]
        dx_, dy_ = x1 - x0, y1 - y0

        if tecla == pygame.K_LEFT and dx_ < 0 and abs(dy_) < 10:
            destino = v
        elif tecla == pygame.K_RIGHT and dx_ > 0 and abs(dy_) < 10:
            destino = v
        elif tecla == pygame.K_UP and dy_ < 0 and abs(dx_) < 10:
            destino = v
        elif tecla == pygame.K_DOWN and dy_ > 0 and abs(dx_) < 10:
            destino = v
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
    

