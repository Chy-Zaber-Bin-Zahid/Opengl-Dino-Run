from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

speed = 0.1
left = 0
up = 0
jumping = False
jump_height = 85  # Adjust as needed
jump_duration = 250  # Adjust as needed
jump_timer = 0 
pressed = "n"
distance = 0 
game = "Stop"


class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    def collides_with(self, other):
        return (self.x < other.x + other.w and  # x_min_1 < x_max_2
                self.x + self.w > other.x and  # x_max_1 > m_min_2
                self.y < other.y + other.h and  # y_min_1 < y_max_2
                self.y + self.h > other.y)     # y_max_1 > y_min_2


# tank
box1 = AABB(87, 70, 46, 55)
box2 = AABB(835, 50, 40, 45)


collision = False


def show_score():
    global pressed
    if pressed == "n":
      glColor3f(1.0, 1.0, 1.0)
    else:
      glColor3f(0.0, 0.0, 0.0) 
    glRasterPos2f(10, WINDOW_HEIGHT - 40)
    distanceStore = f"Distance: {distance}"
    for char in distanceStore:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def draw_box(box):
    global pressed
    if pressed =="n":
        glColor3f(0.0, 0.0, 0.0)
    else:
        glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(box.x, box.y)
    glVertex2f(box.x + box.w, box.y)

    glVertex2f(box.x + box.w, box.y)
    glVertex2f(box.x + box.w, box.y + box.h)

    glVertex2f(box.x + box.w, box.y + box.h)
    glVertex2f(box.x, box.y + box.h)

    glVertex2f(box.x, box.y + box.h)
    glVertex2f(box.x, box.y)
    glEnd()

def check_collision():
    global box1, box2, collision

    if box1.collides_with(box2):
        collision = True
    else:
        collision = False


def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def midpoint(x1, y1, x2, y2, zone):
    dx = x2-x1
    dy = y2-y1
    d = (2*dy) - dx
    dE = 2*dy
    dNE = 2*(dy-dx)
    xInitial = x1
    yInitial = y2
    while (xInitial < x2):
        if d <= 0:
            d = d+dE
            xInitial += 1
        else:
            d = d+dNE
            xInitial += 1
            yInitial += 1
        cx, cy = convertOriginal(xInitial, yInitial, zone)
        glVertex2f(cx, cy)


def findZone(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    if dx >= dy:
        if x1 <= x2:
            if y1 <= y2:
                return 0
            else:
                return 7
        else:
            if y1 <= y2:
                return 3
            else:
                return 4
    else:
        if x1 <= x2:
            if y1 <= y2:
                return 1
            else:
                return 6
        else:
            if y1 <= y2:
                return 2
            else:
                return 5


def convertZone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        x, y = y, x
        return x, y
    elif zone == 2:
        x, y = y, -x
        return x, y
    elif zone == 3:
        x, y = -x, y
        return x, y
    elif zone == 4:
        x, y = -x, -y
        return x, y
    elif zone == 5:
        x, y = -y, -x
        return x, y
    elif zone == 6:
        x, y = -y, x
        return x, y
    else:
        x, y = x, -y
        return x, y


def convertOriginal(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        x, y = y, x
        return x, y
    elif zone == 2:
        x, y = -y, x
        return x, y
    elif zone == 3:
        x, y = -x, y
        return x, y
    elif zone == 4:
        x, y = -x, -y
        return x, y
    elif zone == 5:
        x, y = -y, -x
        return x, y
    elif zone == 6:
        x, y = y, -x
        return x, y
    else:
        x, y = x, -y
        return x, y


def drawLine(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2, y1, y2 = x2, x1, y2, y1
    zone = findZone(x1, y1, x2, y2)
    x1, y1 = convertZone(x1, y1, zone)
    x2, y2 = convertZone(x2, y2, zone)
    glBegin(GL_POINTS)
    midpoint(x1, y1, x2, y2, zone)
    glEnd()


def show_screen():
    global left, up, pressed
    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if pressed == "n":
      glColor3f(1, 1, 1)
    else:
      glColor3f(0, 0, 0) 

    if pressed == "n":
        glClearColor(0, 0, 0, 0)  # //color black
    else:
        glClearColor(1.0, 1.0, 1.0, 0.0)  # //color white

    # dino
    drawLine(80, 70 + up, 100, 120 + up)
    drawLine(120, 120 + up, 140, 120 + up)
    drawLine(140, 120 + up, 140, 110 + up)
    drawLine(130, 110 + up, 140, 110 + up)
    drawLine(130, 110 + up, 130, 70 + up)
    drawLine(100, 70 + up, 130, 70 + up)
    drawLine(80, 90 + up, 100, 80 + up)
    drawLine(80, 80 + up, 105, 80 + up)
    drawLine(105, 50 + up, 105, 70 + up)
    drawLine(110, 50 + up, 110, 70 + up)
    drawLine(120, 50 + up, 120, 70 + up)
    drawLine(125, 50 + up, 125, 70 + up)
    drawLine(130, 100 + up, 140, 100 + up)
    drawLine(130, 95 + up, 140, 95 + up)

    # cactas
    drawLine(500 + 350 + left, 50, 500 + 350 + left, 70)
    drawLine(485 + 350 + left, 70, 500 + 350 + left, 70)
    drawLine(485 + 350 + left, 70, 485 + 350 + left, 85)
    drawLine(485 + 350 + left, 85, 490 + 350 + left, 85)
    drawLine(490 + 350 + left, 75, 490 + 350 + left, 85)
    drawLine(490 + 350 + left, 75, 500 + 350 + left, 75)
    drawLine(500 + 350 + left, 75, 500 + 350 + left, 100)
    drawLine(500 + 350 + left, 100, 510 + 350 + left, 100)
    drawLine(510 + 350 + left, 80, 510 + 350 + left, 100)
    drawLine(510 + 350 + left, 80, 520 + 350 + left, 80)
    drawLine(520 + 350 + left, 80, 520 + 350 + left, 90)
    drawLine(520 + 350 + left, 90, 525 + 350 + left, 90)
    drawLine(525 + 350 + left, 75, 525 + 350 + left, 90)
    drawLine(510 + 350 + left, 75, 525 + 350 + left, 75)
    drawLine(510 + 350 + left, 50, 510 + 350 + left, 75)

    # drawLine(500 + left, 50, 500 + left, 70)
    # drawLine(485 + left, 70, 500 + left, 70)
    # drawLine(485 + left, 70, 485 + left, 85)
    # drawLine(485 + left, 85, 490 + left, 85)
    # drawLine(490 + left, 75, 490 + left, 85)
    # drawLine(490 + left, 75, 500 + left, 75)
    # drawLine(500 + left, 75, 500 + left, 100)
    # drawLine(500 + left, 100, 510 + left, 100)
    # drawLine(510 + left, 80, 510 + left, 100)
    # drawLine(510 + left, 80, 520 + left, 80)
    # drawLine(520 + left, 80, 520 + left, 90)
    # drawLine(520 + left, 90, 525 + left, 90)
    # drawLine(525 + left, 75, 525 + left, 90)
    # drawLine(510 + left, 75, 525 + left, 75)
    # drawLine(510 + left, 50, 510 + left, 75)

    # road
    drawLine(0, 50, 800, 50)
    show_score()
    draw_box(box1)
    draw_box(box2)

    glutSwapBuffers()


def keyboard_special_keys(key, _, __):
    global box1, jumping
    if key == GLUT_KEY_UP:
        jumping = True

    glutPostRedisplay()

def keyboardListener(key, x, y):
    global pressed, game, jumping
    if game == "Start":
        if key==b'd':
            pressed = "d"
            print("Day")
        if key==b'n':
            pressed = "n"
            print("Night")
    else:
        if key==b' ':
            game = "Start"
            jumping = True
    

    glutPostRedisplay()

def animation():
    global left, speed, box2, collision, jumping, jump_height, up, jump_duration, jump_timer, distance, game
    if game == "Start":
        check_collision()
        if collision == False:
          distance+=1
          left-=speed*5
          box2.x-=speed*5
          if left < -850:
              left = 0
              box2.x = 835
          if jumping:
            if jump_timer < jump_duration:  # Check if jump duration is not reached
                if up < jump_height:
                    up += speed * 7
                    box1.y += speed * 7
                jump_timer += 1  # Increment jump timer
            else:
                jumping = False  # Stop jumping and start descending
                jump_timer = 0  # Reset jump timer
          elif up > 0:  # Descend
            up -= speed * 7
            box1.y -= speed * 7
        else:
            print(f"Game Over Total Distance went: {distance}")
            game = "Stop"
    

    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catch the Diamonds!")

glutDisplayFunc(show_screen)
glutIdleFunc(animation)

# glutKeyboardFunc(keyboard_ordinary_keys)
glutSpecialFunc(keyboard_special_keys)
glutKeyboardFunc(keyboardListener)
# glutMouseFunc(mouse_click)


glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
