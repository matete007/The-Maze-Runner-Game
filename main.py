from pygame import Rect
import pgzero
import pgzrun
import math
from pgzero.builtins import Actor, keyboard

TITLE = 'THE MAZE RUNNER GAME'
WIDTH = 675
HEIGHT = 422

GRAVITY = 9.8
PLAYER_SPEED = 3
JUMP_FORCE = -5
COLLISION_TOLERANCE = 4
GAME_STATE = 'playing'

left_ground_height = 132
left_ground_width = 106
right_ground_height = 117
right_ground_width = 116

#PLATFORMS5
# x, y, platform width, platform height
left_ground = Rect(0, 290, left_ground_width, left_ground_height)
right_ground = Rect(558, 305, right_ground_width, right_ground_height)

p1 = Actor("platafforms2.png")
p1.topleft = (158, 293)
p1Rect = Rect(p1.topleft[0], p1.topleft[1], 24, 24)
p2 = Actor("platafforms2.png")
p2.topleft = (222, 226)
p2Rect = Rect(p2.topleft[0], p2.topleft[1], 24, 24)
p3 = Actor("platafforms2.png")
p3.topleft = (158, 172)
p3Rect = Rect(p3.topleft[0], p3.topleft[1], 24, 24)
p4 = Actor("platafforms2.png")
p4.topleft = (235, 111)
p4Rect = Rect(p4.topleft[0], p4.topleft[1], 24, 24)

#MOVING PLATFORM
movingP = Actor("platafforms3.png")
movingP.topleft = (30, 74)
movingPRect = Rect(movingP.topleft[0], movingP.topleft[1], 33, 18)
PLATFORM_SPEED = 1

moving_platform_data = {
    'visual': movingP,
    'rect': movingPRect,
    'vx': PLATFORM_SPEED,
    'limit_left': 30,
    'limit_right': 130
}

#KEY
key = Actor("key0.png")
key.topleft = (movingP.topleft[0] + 5, movingP.topleft[1] - key.height)


#PLAYER ANIMATIONS
player_walk = ['walking-thomas1.png', 'walking-thomas0.png']
player_idle = ['stopped-thomas0.png', 'stopped-thomas1.png']
player_jump = ['jumping-thomas1.png', 'jumping-thomas2.png', 'jumping-thomas3.png', 'jumping-thomas4.png', 'jumping-thomas5.png', 'jumping-thomas6.png', 'jumping-thomas7.png']

player = Actor(player_idle[0])
player.pos = (50, 311 - player.height * 1.5)
player.x_previous = player.x

vellocityy = 1.0

def on_mouse_move(pos):
    x, y = pos
    print(f"Mouse X: {x}, Y: {y}")

def update_player(keyboard):
    if keyboard.left:
        player.x -= 3
    if keyboard.right:
        player.x += 3

platforms = [left_ground, right_ground, p1Rect, p2Rect, p3Rect, p4Rect, moving_platform_data]
platform_visuals = [p1, p2, p3, p4, movingP]

def update_platforms():
    for pt in platforms:
        if isinstance(pt, dict) and 'vx' in pt:
            p_rect = pt['rect']
            p_visual = pt['visual']
            p_rect.x += pt['vx']
            if p_rect.right > pt['limit_right']:
                pt['vx'] = -PLATFORM_SPEED
            elif p_rect.left < pt['limit_left']:
                pt['vx'] = PLATFORM_SPEED
            p_visual.topleft = p_rect.topleft

def set_image_midbottom(image):
    mb = player.midbottom
    player.image = image
    player.midbottom = mb
        
animations = {
    "idle": player_idle,
    "walk": player_walk,
    "jump": player_jump
}
current_animation = "idle"
animation_delay = 0.25
animation_timer = 0
index = 0
MAX_DT = 0.05

def animate(dt, animation):
    global index, animation_timer, current_animation

    if animation != current_animation:
        current_animation = animation
        index = 0
        animation_timer = 0
        set_image_midbottom(animations[animation][0])
        return

    animation_timer += dt

    if animation_timer >= animation_delay:
        animation_timer = 0
        index = (index + 1) % len(animations[animation])
        set_image_midbottom(animations[animation][index])

#player_is_alive = True
on_ground = False

def update(dt):
    global vellocityy, on_ground
    on_ground = False
    update_platforms()

    player.y_previous = player.y 
    player.bottom_previous = player.bottom

    if dt > MAX_DT:
        dt = MAX_DT


    if not on_ground:
        vellocityy += GRAVITY * dt
    player.y += vellocityy

    for p in platforms:
        if isinstance(p, dict):
            p_rect = p['rect']
        else:
            p_rect = p
        if player.colliderect(p_rect):
            if vellocityy > 0:
                if player.bottom_previous <= p_rect.top:
                    player.bottom = p_rect.top
                    vellocityy = 0
                    on_ground = True
                    if on_ground and isinstance(p, dict) and 'vx' in p:
                        player.x += p['vx']
            elif vellocityy < 0:
                if player.y_previous >= p_rect.bottom: 
                     vellocityy = 0

    if keyboard.up and on_ground:
        vellocityy = JUMP_FORCE
        on_ground = False

    moving = keyboard.left or keyboard.right
    if moving:
        update_player(keyboard)

    if not on_ground:
        animate(dt, "jump")
    elif moving:
        animate(dt, "walk")
    else:
        animate(dt, "idle")

    half = player.width / 2

    if player.x < half:
        player.x = half
    elif player.x > WIDTH - half:
        player.x = WIDTH - half
    
    player.x_previous = player.x


def draw():
    screen.clear()
    screen.blit('background_', (0,0))
    for visual in platform_visuals:
        visual.draw()
    player.draw()


pgzrun.go()