import pygame
import sys


# Configuración
pygame.init()
ANCHO, ALTO = 900, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Gato y Ratón – Tablero 11 nodos con queso y meta oculta")

FPS = 60
RELOJ = pygame.time.Clock()
COLOR_FONDO = (245, 240, 230)
COLOR_LINEAS = (40, 40, 40)
COLOR_NODO = (180, 180, 180)
COLOR_INICIO = (120, 220, 120)
COLOR_FINAL = (250, 150, 150)
FUENTE = pygame.font.SysFont("arial", 22)

# Imágenes
img_gato = pygame.image.load("./assets/gato.png")
img_raton = pygame.image.load("./assets/ratón.png")
img_queso = pygame.image.load("./assets/queso.png")

ESCALA = 0.15
img_gato = pygame.transform.smoothscale(img_gato, (int(250*ESCALA), int(250*ESCALA)))
img_raton = pygame.transform.smoothscale(img_raton, (int(250*ESCALA), int(250*ESCALA)))
img_queso = pygame.transform.smoothscale(img_queso, (int(200*ESCALA), int(200*ESCALA)))


# Tablero
x0, y_mid = 150, 300
dx, dy = 100, 100

nodos = {
    0: (x0, y_mid),                # ala izquierda (medio)
    1: (x0+dx, y_mid-dy),          # col1 arriba
    2: (x0+dx, y_mid),             # col1 medio
    3: (x0+dx, y_mid+dy),          # col1 abajo
    4: (x0+2*dx, y_mid-dy),        # col2 arriba
    5: (x0+2*dx, y_mid),           # col2 medio
    6: (x0+2*dx, y_mid+dy),        # col2 abajo
    7: (x0+3*dx, y_mid-dy),        # col3 arriba
    8: (x0+3*dx, y_mid),           # col3 medio
    9: (x0+3*dx, y_mid+dy),        # col3 abajo
    10: (x0+4*dx, y_mid),          # ala derecha (medio)
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


# Estados del Juego
pos_gato = 1      # Gato empieza arriba izq
pos_raton = 0     # Ratón empieza en el ala izq
inicio = 0        # Nodo de inicio del ratón
final = 10        # Nodo meta (se oculta al inicio)
queso = 5         # Nodo del queso (centro)
tiene_queso = False
turno = "raton"
game_over = False
victoria = False


# Funciones
def dibujar_tablero():
    """Dibuja el grafo con el queso visible y la meta oculta hasta tener el queso."""
    VENTANA.fill(COLOR_FONDO)
    for (i, j) in aristas:
        pygame.draw.line(VENTANA, COLOR_LINEAS, nodos[i], nodos[j], 3)

    for i, (x, y) in nodos.items():
        color = COLOR_NODO
        if i == inicio:
            color = COLOR_INICIO
        # Solo mostrar el final cuando se tenga el queso
        elif i == final and tiene_queso:
            color = COLOR_FINAL
        pygame.draw.circle(VENTANA, color, (x, y), 9)

    # Mostrar queso si no fue recogido
    if not tiene_queso:
        qx, qy = nodos[queso]
        VENTANA.blit(img_queso, (qx - 15, qy - 15))


def dibujar_piezas():
    """Dibuja el gato y el ratón"""
    gx, gy = nodos[pos_gato]
    rx, ry = nodos[pos_raton]
    VENTANA.blit(img_gato, (gx - 15, gy - 15))
    VENTANA.blit(img_raton, (rx - 15, ry - 15))


def mover_pieza(pos_actual, tecla, ocupados):
    """Permite moverse a nodos conectados según dirección de tecla."""

    # En la versión automatizada, esta función podría recibir un parámetro
    # "accion" generado por un algoritmo (por ejemplo, el próximo nodo a visitar)
    # en lugar de depender de una tecla. 
    # Entonces podrías eliminar los if de pygame.K_* y hacer:
    # return mejor_vecino(pos_actual, objetivo, ocupados)
    # usando una búsqueda como BFS o A*.

    if tecla not in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                     pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_c]:
        return pos_actual

    x0, y0 = nodos[pos_actual]
    destino = pos_actual

    for v in conexiones[pos_actual]:
        x1, y1 = nodos[v]
        dx_, dy_ = x1 - x0, y1 - y0

        # Movimiento horizontal y vertical (FLECHAS)
        if tecla == pygame.K_LEFT and dx_ < 0 and abs(dy_) < 10:
            destino = v
        elif tecla == pygame.K_RIGHT and dx_ > 0 and abs(dy_) < 10:
            destino = v
        elif tecla == pygame.K_UP and dy_ < 0 and abs(dx_) < 10:
            destino = v
        elif tecla == pygame.K_DOWN and dy_ > 0 and abs(dx_) < 10:
            destino = v

        # Movimiento diagonal (Q, E, Z, C)
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


# -----------------------------------------
# BUCLE PRINCIPAL
# -----------------------------------------
while True:
    RELOJ.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            # aquí se reemplazan las decisiones humanas por inteligencia artificial
            if not (game_over or victoria):
                if turno == "raton":
                    pos_raton = mover_pieza(pos_raton, event.key, [pos_gato])
                    turno = "gato"
                else:
                    pos_gato = mover_pieza(pos_gato, event.key, [pos_raton])
                    turno = "raton"

    # --------------------------
    # LÓGICA DEL JUEGO
    # --------------------------
    if not game_over and not victoria:
        # Si el gato atrapa al ratón
        if pos_gato == pos_raton:
            cartel("¡GAME OVER! El gato atrapó al ratón.")
            pos_gato, pos_raton, turno = 1, 0, "raton"
            tiene_queso = False
            game_over = True

        # Si el ratón agarra el queso
        if pos_raton == queso and not tiene_queso:
            tiene_queso = True

        # Si el ratón llega al final con el queso
        if pos_raton == final and tiene_queso:
            cartel("¡Ganaste! El ratón llegó con el queso ", (200, 255, 200))
            pos_gato, pos_raton, turno = 1, 0, "raton"
            tiene_queso = False
            victoria = True

    # Redibujar
    dibujar_tablero()
    dibujar_piezas()
    if game_over:
        mostrar_texto("Presiona cualquier tecla para reiniciar...", 50)
    elif victoria:
        mostrar_texto("Presiona cualquier tecla para volver a jugar...", 50)
    else:
        mostrar_texto(f"Turno: {turno.upper()} | Flechas + Q/E/Z/C (diagonales)")
        if not tiene_queso:
            mostrar_texto("Busca el queso para revelar la meta", 50)
        else:
            mostrar_texto("La meta se ha revelado, ¡llega al final!", 50)

    pygame.display.flip()

    # Reinicio si se presiona algo después de fin
    keys = pygame.key.get_pressed()
    if (game_over or victoria) and any(keys):
        pos_gato, pos_raton, turno = 1, 0, "raton"
        tiene_queso = False
        game_over = False
        victoria = False
