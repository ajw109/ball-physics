# Basic collision in pygame
import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # tuple

fps = 60
timer = pygame.time.Clock()

# game variables
wall_thickness = 10
gravity = 0.5
bounce_stop = 0.3

# track positions of mouse to get movement vector
mouse_trajectory = []

# ball class
class Ball:
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention # between 0 and 1
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction

    def draw(self):
        self.circle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def check_gravity(self):

        if not self.selected: # if ball isn't being clicked
            if self.y_pos < HEIGHT - self.radius - (wall_thickness/2): # if ball is in air
                self.y_speed += gravity # increase speed
            else: # if we've hit the ground
                if self.y_speed > bounce_stop: # if speed is great enough that I want to continue bouncing
                    self.y_speed = self.y_speed * -1 * self.retention # flip direction and implement retention
                else:  # if bounces have become negligible
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0 # stop bouncing

            # handle wall collision
            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                    (self.x_pos > WIDTH - self.radius - (wall_thickness / 2) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention # flip direction and slow down

                if abs(self.x_speed) < bounce_stop: # if it's too slow to bounce off wall
                    self.x_speed = 0
                
                
            # if still moving in x direction but y has stopped bouncing
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction # slow ball down using friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction # slow ball down using friction
                    # every time the ball hits the wall
                    # we need to continually decrease speed to bring value closer to 0

        
        else: # if ball is being clicked
            self.x_speed = x_push
            self.y_speed = y_push

            # handle horizontal wall collisions 
            if self.x_pos < self.radius + (wall_thickness / 2):
                self.x_pos = self.radius + (wall_thickness / 2)

            if self.x_pos > WIDTH - self.radius - (wall_thickness / 2):
                self.x_pos = WIDTH - self.radius - (wall_thickness / 2)

            # handle vertical wall collisions
            if self.y_pos < self.radius + (wall_thickness / 2):
                self.y_pos = self.radius + (wall_thickness / 2)

            if self.y_pos > HEIGHT - self.radius - (wall_thickness / 2):
                self.y_pos = HEIGHT - self.radius - (wall_thickness / 2)


            # self.x_speed = 0 # just moves and drops the ball
            # self.y_speed = 0 # resets the downward speed after being clicked

        return self.y_speed
        # if you're going to update something inside these functions,
        # return it to remember what my previous speed was
    
    def update_pos(self, mouse):
        if not self.selected: # if not selected, keep doing these things
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else: # if we have been selected, drag ball around with us
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

    def check_select(self, pos):
        self.selected = False # not selected, force function to prove me wrong
        if self.circle.collidepoint(pos): # pygame built in collision detection
            self.selected = True
        return self.selected # either yes I have a ball or no I don't have a ball

# wall drawing functions
def draw_walls():
    left = pygame.draw.line(screen, 'white', (0,0), (0, HEIGHT), wall_thickness)
    right = pygame.draw.line(screen, 'white', (WIDTH, 0), (WIDTH, HEIGHT), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0,0), (WIDTH, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0, HEIGHT), (WIDTH, HEIGHT), wall_thickness)
    wall_list = [left, right, top, bottom]
    return wall_list

def calc_motion_vector(): # calculate x and y speed that the mouse was moving at when we throw the ball
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 19: # the list is fully populated
        # take pos the mouse was in at the first frame in the list
        # and pos the mouse was in at last frame in list
        # divide by 20
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)

    return x_speed, y_speed # same as push
 
# instance of ball class
ball1 = Ball(250, -100, 30, 'yellow', 100, .8, 0, 0, 1, 0.02)
ball2 = Ball(500, -100, 50, 'orange', 300, .9, 0, 0, 2, 0.03)
ball3 = Ball(750, -100, 40, 'red', 200, .8, 0, 0, 3, 0.04)
balls = [ball1, ball2, ball3] 

# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    mouse_coords = pygame.mouse.get_pos() 
    mouse_trajectory.append(mouse_coords) # get pos and add to mouse trajectory list
    if len(mouse_trajectory) > 20: # if list gets above 20, 1/3 of a second (we know what mouse did in last 1/3 of a second)
        mouse_trajectory.pop(0) # fifo mechanism
    x_push, y_push = calc_motion_vector()

    # draw walls
    walls = draw_walls()
    ball1.draw()
    ball2.draw()
    ball3.draw()
    ball1.update_pos(mouse_coords) # move the ball
    ball2.update_pos(mouse_coords)
    ball3.update_pos(mouse_coords)
    ball1.y_speed = ball1.check_gravity() # update pos based on y_speed
    ball2.y_speed = ball2.check_gravity()
    ball3.y_speed = ball3.check_gravity()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if player quits game
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN: # if player clicks mouse
            if event.button == 1: # left mouse click
                if ball1.check_select(event.pos) or ball2.check_select(event.pos) or ball3.check_select(event.pos): # pass in position of mouse when clicked
                    active_select = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)): # check all the balls
                    balls[i].check_select((-1000, -1000)) # impossible values

    pygame.display.flip() # draw onto screem
pygame.quit() # end program