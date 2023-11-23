from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 600
move = 0
fall = 0
point = 0
speed = .1
game = "continue"
basketOver = False
play = "resume"
stop = "unfreeze"

diamondCornerZero = 0
diamondCornerFifteen = 15
diamondCornerThirty = 30
diamondCornerFourFive = 45

direction = "right"

class AABB:
    x = 0
    y = 0
    w = 0
    h = 0

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def collides_with(self, other):
        return (self.x < other.x + other.w and # x_min_1 < x_max_2
                self.x + self.w > other.x  and # x_max_1 > m_min_2
                self.y < other.y + other.h and # y_min_1 < y_max_2
                self.y + self.h > other.y)     # y_max_1 > y_min_2
    

#tank
box1 = AABB(230, 10, 42, 50)
#upper four space ship
box2 = AABB(0, 500, 47, 30)
box6 = AABB(100, 500, 47, 30)
box7 = AABB(200, 500, 47, 30)
box8 = AABB(300, 500, 47, 30)
#bottom four space ship
box9 = AABB(105, 450, 47, 30)
box10 = AABB(205, 450, 47, 30)
box11 = AABB(305, 450, 47, 30)
box12 = AABB(405, 450, 47, 30)
#three button
box3 = AABB(10, 549, 38, 31)
box4 = AABB(240, 545, 34, 35)
box5 = AABB(450, 545, 31, 35)
boxes = [box3, box4, box5]

box_speed = 7
collision = False

def draw_box(box):
    glColor3f(1.0, 0.0, 0.0)
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

# def mouse_click(button, state, x, y):
#     global boxes, point, move,fall,speed, box, game, basketOver, play, stop
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
#         mouse_x = x
#         mouse_y = WINDOW_HEIGHT - y

#         # Create a new AABB representing the clicked point
#         clicked_box = AABB(mouse_x, mouse_y, 1, 1)

#         # Check for collision with each box
#         for box in boxes:
#             if box.collides_with(clicked_box):
#                 if boxes.index(box) == 0:
#                     move = 0
#                     fall = 0
#                     point = 0
#                     speed = .1
#                     # box2.y = 500
#                     box1.x = 230
              
#                     box2.x = 0
#                     game = "continue"
#                     basketOver = False
#                     play = "resume"
#                     stop = "unfreeze"
#                     print("Starting Over!")
#                 elif boxes.index(box) == 2:
#                     print(f"Goodbye and your score is {point}!")
#                     glutLeaveMainLoop() #terminate window
#                 else:
#                     if play =="resume":
#                       stop = "freeze"
#                       play ="stop"
#                     else:
#                       stop = "unfreeze"
#                       play ="resume"
                        

def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def midpoint(x1,y1,x2,y2,zone):
    dx = x2-x1
    dy = y2-y1
    d = (2*dy) - dx
    dE = 2*dy
    dNE = 2*(dy-dx)
    xInitial = x1
    yInitial = y2
    while (xInitial<x2):
        if d<=0:
            d=d+dE
            xInitial+=1
        else:
            d=d+dNE
            xInitial+=1
            yInitial+=1
        cx,cy = convertOriginal(xInitial,yInitial,zone)
        glVertex2f(cx,cy)



def findZone(x1,y1,x2,y2):
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
        

def convertZone(x,y,zone):
    if zone == 0:
        return x,y
    elif zone == 1:
        x,y = y,x
        return x,y
    elif zone == 2:
        x,y = y,-x
        return x,y
    elif zone == 3:
        x,y = -x,y
        return x,y
    elif zone == 4:
        x,y = -x,-y
        return x,y
    elif zone == 5:
        x,y = -y,-x
        return x,y
    elif zone == 6:
        x,y = -y,x
        return x,y
    else:
        x,y = x,-y
        return x,y

def convertOriginal(x,y,zone):
    if zone == 0:
        return x,y
    elif zone == 1:
        x,y = y,x
        return x,y
    elif zone == 2:
        x,y = -y,x
        return x,y
    elif zone == 3:
        x,y = -x,y
        return x,y
    elif zone == 4:
        x,y = -x,-y
        return x,y
    elif zone == 5:
        x,y = -y,-x
        return x,y
    elif zone == 6:
        x,y = y,-x
        return x,y
    else:
        x,y = x,-y
        return x,y

def drawLine(x1,y1,x2,y2):
    if x1>x2:
        x1,x2,y1,y2 =x2,x1,y2,y1 
    zone = findZone(x1,y1,x2,y2)
    x1,y1 = convertZone(x1,y1,zone) 
    x2,y2 = convertZone(x2,y2,zone) 
    glBegin(GL_POINTS)
    midpoint(x1,y1,x2,y2,zone)
    glEnd()


def show_screen():
    global move,fall,diamondCornerZero,diamondCornerFifteen,diamondCornerThirty,r,g,b, basketOver, play,speed, direction
    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # #alien space ship
    # glColor3f(r, g, b)
    # drawLine(diamondCornerZero+,530+fall,diamondCornerFifteen+,550+fall)
    # drawLine(diamondCornerFifteen+,550+fall,diamondCornerThirty+,530+fall)
    # drawLine(diamondCornerZero+,532+fall,diamondCornerFifteen+,510+fall)
    # drawLine(diamondCornerFifteen+,510+fall,diamondCornerThirty+,529+fall)
    x = 0
    
    for i in range(4):
        glColor3f(1, 1, 1)
        #alien space ship head
        drawLine(diamondCornerFifteen + x - fall,530,diamondCornerThirty + x - fall,530)
        drawLine(diamondCornerFifteen + x - fall,520,diamondCornerThirty + x - fall,520)
        drawLine(diamondCornerFifteen + x - fall,520,diamondCornerFifteen + x - fall,530)
        drawLine(diamondCornerThirty + x - fall,520,diamondCornerThirty + x - fall,530)
        #alien space ship body
        drawLine(diamondCornerZero + x - fall,520,diamondCornerFourFive + x - fall,520)
        drawLine(diamondCornerZero + x - fall,500,diamondCornerFourFive + x - fall,500)
        drawLine(diamondCornerZero + x - fall,500,diamondCornerZero + x - fall,520)
        drawLine(diamondCornerFourFive + x - fall,500,diamondCornerFourFive + x - fall,520)
        

        # #alien space ship head
        # drawLine(120 + x + fall,480,135 + x + fall,480)
        # drawLine(120 + x + fall,470,135 + x + fall,470)
        # drawLine(120 + x + fall,470,120 + x + fall,480)
        # drawLine(135 + x + fall,470,135 + x + fall,480)
        # #alien space ship body
        # drawLine(105 + x + fall,450,150 + x + fall,450)
        # drawLine(105 + x + fall,470,150 + x + fall,470)
        # drawLine(105 + x + fall,470,105 + x + fall,450)
        # drawLine(150 + x + fall,470,150 + x + fall,450)
        # x+=100

    #tank body
    if basketOver == False: 
      glColor3f(1, 1, 1)
    else:
      glColor3f(1.0, 0.0, 0.0)
    drawLine(230+move,10,270+move,10)
    drawLine(230+move,60,270+move,60)
    drawLine(230+move,10,230+move,60)
    drawLine(270+move,60,270+move,10)
    #tank head
    drawLine(240+move,25,260+move,25)
    drawLine(240+move,45,260+move,45)
    drawLine(240+move,25,240+move,45)
    drawLine(260+move,45,260+move,25)
    #tank barrel
    drawLine(245+move,45,255+move,45)
    drawLine(245+move,80,255+move,80)
    drawLine(245+move,45,245+move,80)
    drawLine(255+move,80,255+move,45)

    #playAgain
    glColor3f(0.529, 0.808, 0.922)
    drawLine(10,565,45,565)
    drawLine(0,564,10,580)
    drawLine(0,565,10,550)

    if game != "finished":
        if play == "resume":
            #pause
            glColor3f(1.0, 0.647, 0.0)
            drawLine(247,545,247,580)
            drawLine(257,545,257,580)
        else:
            #play
            glColor3f(1.0, 0.647, 0.0)
            drawLine(240,545,240,580)
            drawLine(239,525,270,545)
            drawLine(240,594,270,579)
    


    #close
    glColor3f(1,0.0, 0.0)
    drawLine(420,545,450,580)
    drawLine(420,580,450,545)

    draw_box(box1)
    draw_box(box2)
    draw_box(box3)
    draw_box(box4)
    draw_box(box5)
    draw_box(box6)
    draw_box(box7)
    draw_box(box8)
    draw_box(box9)
    draw_box(box10)
    draw_box(box11)
    draw_box(box12)

    glutSwapBuffers()


def keyboard_special_keys(key, _, __):
    global move, box, game
    if stop == "unfreeze":
      if game == "continue":
          if key == GLUT_KEY_LEFT:
              if move != -182:
                  box1.x -= box_speed
                  move-=7
          elif key == GLUT_KEY_RIGHT:
              if move != 182:
                  box1.x += box_speed
                  move+=7
        

    glutPostRedisplay()

def animation():
    global fall, speed, direction
    check_collision()

    if stop == "unfreeze":
      if game == "continue":
          if fall == -155:
              fall = 152
              direction = "left"
              print("jeo")
          if direction == "right":
              fall-=speed
          else:
              fall+=speed

          




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
# glutMouseFunc(mouse_click)


glEnable(GL_DEPTH_TEST)
initialize()
glutMainLoop()
