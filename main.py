from pygame import Rect
import pgzero
import pgzrun
from pgzero.builtins import Actor, keyboard, clock

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

# x, y, platform height, platform width    --mas por algum motivo height e width estão trocados na hora de fazer o rect
left_ground = Rect(0, 290, left_ground_width, left_ground_height)
right_ground = Rect(558, 305, right_ground_width, right_ground_height)

#PLAYER ANIMATIONS
player_walk = ['walking-thomas1.png', 'walking-thomas0.png']
player_idle = ['stopped-thomas0.png', 'stopped-thomas1.png']
player_breath = ['breathing-thomas0.png', 'breathing-thomas1.png']
player_jump = ['jumping-thomas0.png', 'jumping-thomas1.png', 'jumping-thomas2.png', 'jumping-thomas3.png', 'jumping-thomas4.png', 'jumping-thomas5.png', 'jumping-thomas6.png', 'jumping-thomas7.png']

player = Actor(player_idle[0])
player.pos = (50, 311 - player.height * 1.5)
player.height = 65
player.width = 25
player.x_previous = player.x

vellocityy = 0

def update_player(keyboard):
    if keyboard.left:
        player.x -= 3
    if keyboard.right:
        player.x += 3

platforms = [left_ground, right_ground]

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

    if not on_ground:
        vellocityy += GRAVITY * dt
    player.y += vellocityy

    for p in platforms:
        if player.colliderect(p):
            if vellocityy > 0:
                overlap_y = player.bottom - p.top
                if overlap_y < COLLISION_TOLERANCE:
                    player.bottom = p.top
                    vellocityy = 0
                    on_ground = True

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
    player.draw()

pgzrun.go()