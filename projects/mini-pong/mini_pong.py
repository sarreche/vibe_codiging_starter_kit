# Mini Pong - Vibe Coding Kit
# Requisitos: pygame (pip install pygame)
# Controles: Flechas Arriba/Abajo para mover la barra. ESC para salir.
# Tips para jugar/editar:
#   - Cambia 'BALL_SPEED' y 'PADDLE_SPEED' para ajustar la dificultad.
#   - Cambia colores (RGB) y tamaños.
#   - Reemplaza la pelota por una imagen en 'pong_assets/ball.png'.

import pygame
import sys
import os

# ---- Config ----
WIDTH, HEIGHT = 640, 400
BG_COLOR = (20, 24, 28)
PADDLE_COLOR = (240, 240, 240)
BALL_COLOR = (80, 200, 120)
PADDLE_W, PADDLE_H = 12, 80
BALL_SIZE = 12
PADDLE_SPEED = 5
BALL_SPEED = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Pong - Vibe Coding Kit")
clock = pygame.time.Clock()

# ---- Sonido opcional ----
bounce_sound = None
try:
    bounce_path = os.path.join("pong_assets", "bounce.wav")
    if os.path.exists(bounce_path):
        bounce_sound = pygame.mixer.Sound(bounce_path)
except Exception:
    bounce_sound = None

# ---- Pelota como imagen opcional ----
ball_img = None
ball_rect = None
try:
    img_path = os.path.join("pong_assets", "ball.png")
    if os.path.exists(img_path):
        ball_img = pygame.image.load(img_path).convert_alpha()
        ball_img = pygame.transform.smoothscale(ball_img, (BALL_SIZE, BALL_SIZE))
        ball_rect = ball_img.get_rect()
except Exception:
    ball_img = None

# ---- Paddle (jugador) ----
paddle = pygame.Rect(20, HEIGHT//2 - PADDLE_H//2, PADDLE_W, PADDLE_H)

# ---- Pelota ----
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_vel = [BALL_SPEED, BALL_SPEED]

score = 0
font = pygame.font.SysFont("arial", 20)

def reset_ball():
    global ball_vel
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_vel = [BALL_SPEED, BALL_SPEED]

def play_bounce():
    if bounce_sound is not None:
        try:
            bounce_sound.play()
        except Exception:
            pass

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        paddle.y += PADDLE_SPEED

    # Limitar paddle a la pantalla
    paddle.y = max(0, min(HEIGHT - PADDLE_H, paddle.y))

    # Mover pelota
    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    # Colisiones con paredes superior/inferior
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1
        play_bounce()

    # Colisión con paddle
    if ball.colliderect(paddle):
        ball.left = paddle.right  # evita quedar pegada
        # Añade variación al ángulo según donde golpee la pelota en el paddle
        relative_intersect_y = (paddle.centery - ball.centery) / (PADDLE_H/2)
        ball_vel[1] = -BALL_SPEED * relative_intersect_y
        ball_vel[0] *= -1
        score += 1
        play_bounce()

    # Se fue por la izquierda (punto fallido)
    if ball.left <= 0:
        reset_ball()
        score = 0
    
    # Rebote en la pared derecha
    if ball.right >= WIDTH:
        ball.right = WIDTH
        ball_vel[0] *= -1
        play_bounce()

    # Dibujar
    screen.fill(BG_COLOR)
    # Paddle
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    # Ball (imagen opcional o círculo)
    if ball_img is not None:
        ball_rect = ball_img.get_rect(topleft=(ball.x, ball.y))
        screen.blit(ball_img, ball_rect)
    else:
        pygame.draw.ellipse(screen, BALL_COLOR, ball)

    # UI
    text = font.render(f"Score: {score}  (UP/DOWN to move)", True, (200, 200, 200))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
