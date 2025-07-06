from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18, GLUT_BITMAP_TIMES_ROMAN_24
from math import sin, cos, pi
import random

# Window settings
window_width = 800
window_height = 600

# Paddle
paddle_width = 100
paddle_height = 15
paddle_x = window_width // 2
paddle_y = 30

# Ball
ball_radius = 10
ball_x = window_width // 2
ball_y = window_height // 2
ball_dx = 2
ball_dy = 2

# Game state
score = 0
game_over = False
ball_color = [1.0, 1.0, 1.0]
paddle_color = [0.5, 1.0, 0.5]

# Restart button
restart_btn = {
    "x": window_width // 2 - 60,
    "y": window_height // 2 - 100,
    "w": 120,
    "h": 40
}

# Bricks
brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 20
brick_gap = 10
bricks = []

def init_bricks():
    global bricks
    bricks.clear()
    
    total_width = brick_cols * brick_width + (brick_cols - 1) * brick_gap
    start_x = (window_width - total_width) // 2
    start_y = window_height - 80

    for row in range(brick_rows):
        row_bricks = []
        for col in range(brick_cols):
            x = start_x + col * (brick_width + brick_gap)
            y = start_y - row * (brick_height + brick_gap)
            color = [random.random(), random.random(), random.random()]
            row_bricks.append({"x": x, "y": y, "alive": True, "color": color})
        bricks.append(row_bricks)

def draw_text(x, y, text, size=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(size, ord(ch))

def draw_grid():
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_LINES)
    for x in range(0, window_width, 40):
        glVertex2f(x, 0)
        glVertex2f(x, window_height)
    for y in range(0, window_height, 40):
        glVertex2f(0, y)
        glVertex2f(window_width, y)
    glEnd()

def draw_paddle():
    glColor3f(*paddle_color)
    glBegin(GL_QUADS)
    glVertex2f(paddle_x - paddle_width / 2, paddle_y)
    glVertex2f(paddle_x + paddle_width / 2, paddle_y)
    glVertex2f(paddle_x + paddle_width / 2, paddle_y + paddle_height)
    glVertex2f(paddle_x - paddle_width / 2, paddle_y + paddle_height)
    glEnd()

def draw_ball():
    glColor3f(*ball_color)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(ball_x, ball_y)
    for angle in range(0, 361, 10):
        rad = angle * pi / 180
        glVertex2f(ball_x + ball_radius * cos(rad), ball_y + ball_radius * sin(rad))
    glEnd()

def draw_bricks():
    for row in bricks:
        for brick in row:
            if brick["alive"]:
                glColor3f(*brick["color"])
                x, y = brick["x"], brick["y"]
                glBegin(GL_QUADS)
                glVertex2f(x, y)
                glVertex2f(x + brick_width, y)
                glVertex2f(x + brick_width, y + brick_height)
                glVertex2f(x, y + brick_height)
                glEnd()

def draw_restart_button():
    glColor3f(0.2, 0.8, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(restart_btn["x"], restart_btn["y"])
    glVertex2f(restart_btn["x"] + restart_btn["w"], restart_btn["y"])
    glVertex2f(restart_btn["x"] + restart_btn["w"], restart_btn["y"] + restart_btn["h"])
    glVertex2f(restart_btn["x"], restart_btn["y"] + restart_btn["h"])
    glEnd()
    draw_text(restart_btn["x"] + 20, restart_btn["y"] + 12, "Restart", GLUT_BITMAP_HELVETICA_18, color=(0, 0, 0))

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_grid()

    if not game_over:
        draw_paddle()
        draw_ball()
        draw_bricks()
        draw_text(10, window_height - 30, f"Score: {score}")
    else:
        draw_text(window_width / 2 - 80, window_height / 2 + 40, "Game Over!", GLUT_BITMAP_TIMES_ROMAN_24, (1, 0.2, 0.2))
        draw_text(window_width / 2 - 100, window_height / 2 + 10, f"Final Score: {score}", color=(1, 1, 0))
        draw_restart_button()

    glutSwapBuffers()

def update(value):
    global ball_x, ball_y, ball_dx, ball_dy
    global paddle_x, paddle_y, score, game_over

    if not game_over:
        ball_x += ball_dx
        ball_y += ball_dy

        # Bounce off walls
        if ball_x <= ball_radius or ball_x >= window_width - ball_radius:
            ball_dx = -ball_dx
            change_ball_color()
        if ball_y >= window_height - ball_radius:
            ball_dy = -ball_dy
            change_ball_color()

        # Paddle collision
        if paddle_y <= ball_y - ball_radius <= paddle_y + paddle_height:
            if paddle_x - paddle_width / 2 <= ball_x <= paddle_x + paddle_width / 2:
                ball_dy = -ball_dy
                increase_speed()
                score += 1
                change_ball_color()
                change_paddle_color()

        # Brick collision
        for row in bricks:
            for brick in row:
                if brick["alive"]:
                    bx, by = brick["x"], brick["y"]
                    if (bx <= ball_x <= bx + brick_width and
                        by <= ball_y + ball_radius <= by + brick_height):
                        brick["alive"] = False
                        ball_dy = -ball_dy
                        score += 5
                        change_ball_color()
                        break

        # Game over if ball missed
        if ball_y < 0:
            game_over = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global paddle_x
    key = key.decode('utf-8')
    if key == 'a' and paddle_x - paddle_width / 2 > 0:
        paddle_x -= 25
    elif key == 'd' and paddle_x + paddle_width / 2 < window_width:
        paddle_x += 25
    elif key == '\x1b':
        glutLeaveMainLoop()

def mouse(button, state, x, y):
    global game_over
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and game_over:
        ogl_y = window_height - y
        if (restart_btn["x"] <= x <= restart_btn["x"] + restart_btn["w"] and
            restart_btn["y"] <= ogl_y <= restart_btn["y"] + restart_btn["h"]):
            restart_game()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def change_ball_color():
    global ball_color
    ball_color = [random.random() for _ in range(3)]

def change_paddle_color():
    global paddle_color
    paddle_color = [random.random() for _ in range(3)]

def increase_speed():
    global ball_dx, ball_dy
    ball_dx *= 1.05
    ball_dy *= 1.05

def restart_game():
    global ball_x, ball_y, ball_dx, ball_dy
    global score, game_over, paddle_x, ball_color, paddle_color
    ball_x = window_width // 2
    ball_y = window_height // 2
    ball_dx = random.choice([-4, 4])
    ball_dy = 4
    paddle_x = window_width // 2
    score = 0
    game_over = False
    ball_color = [1.0, 1.0, 1.0]
    paddle_color = [0.5, 1.0, 0.5]
    init_bricks()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Breakout Game - OpenGL + Python")

    glClearColor(0, 0, 0, 1)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutTimerFunc(0, update, 0)

    init_bricks()
    glutMainLoop()

if __name__ == "__main__":
    main()
