from pygame import Rect
import pgzero
import pgzrun
from pgzero.builtins import Actor, keyboard

TITLE = 'THE MAZE RUNNER GAME'
WIDTH = 675
HEIGHT = 422

game_tittle = Actor('painel.png')
game_tittle.center = (WIDTH / 2, HEIGHT / 2.5)

play_btn = Actor('play-button.png')
play_btn.center = (WIDTH / 2, (HEIGHT / 2) + 100)
close_btn = Actor('close-button.png')
close_btn.center = (WIDTH / 2, (HEIGHT / 2) + 150)
sound_btn = Actor('sound-button-on.png')
sound_btn.center = (50, 50)

SOUND_ON = True
GRAVITY = 9.8
PLAYER_SPEED = 3
JUMP_FORCE = -5
COLLISION_TOLERANCE = 4
GAME_STATE = 'menu'
HAS_KEY = False
CURRENT_LEVEL = 1
PLATFORM_SPEED = 1

door = Actor("door.png")

left_ground_height = 132
left_ground_width = 106
right_ground_height = 117
right_ground_width = 116

game_over_frames = ['game_over0.png', 'game_over1.png', 'game_over2.png', 'game_over3.png']
game_over_animation = Actor(game_over_frames[0])
game_over_animation.center = (WIDTH / 2, HEIGHT / 2)

escaped = Actor('escaped.png')
escaped.center = (WIDTH / 2, HEIGHT / 2)

go_index = 0
go_timer = 0
GO_ANIMATION_SPEED = 0.3

#FIXED PLATFORMS 
# x, y, platform width, platform height
left_ground = Rect(0, 290, left_ground_width, left_ground_height)
right_ground = Rect(558, 305, right_ground_width, right_ground_height)

#KEY
key_frames = ['key0.png', 'key1.png', 'key2.png', 'key3.png']
key = Actor(key_frames[0])
key.is_collectable = True
key.is_on_platform = True
key.frame_index = 0
key.animation_time = 0
key.animation_delay = 0.15

#PLAYER ANIMATIONS
player_walk = ['walking-thomas1.png', 'walking-thomas0.png']
player_idle = ['stopped-thomas0.png', 'stopped-thomas1.png']
player_jump = ['jumping-thomas1.png', 'jumping-thomas2.png', 'jumping-thomas3.png', 'jumping-thomas4.png', 'jumping-thomas5.png', 'jumping-thomas6.png', 'jumping-thomas7.png']

player_walk_left = ['walking-thomas1-left.png', 'walking-thomas0-left.png']
player_idle_left = ['stopped-thomas0-left.png', 'stopped-thomas1-left.png']
player_jump_left = ['jumping-thomas1-left.png', 'jumping-thomas2-left.png', 'jumping-thomas3-left.png', 'jumping-thomas4-left.png', 'jumping-thomas5-left.png', 'jumping-thomas6-left.png', 'jumping-thomas7-left.png']

player = Actor(player_idle[0])
player.x_previous = player.x
facing_right = True

vellocityy = 1.0

newt_walk = ['infected_newt0.png', 'infected_newt1.png']
newt_walk_left = ['infected_newt0-left.png', 'infected_newt1-left.png']
ENEMY_SPEED = 1
enemies = []

def on_mouse_down(pos):
    global GAME_STATE, CURRENT_LEVEL, sound_btn, SOUND_ON

    if GAME_STATE == 'menu':
        if play_btn.collidepoint(pos):
            GAME_STATE = 'playing'
            CURRENT_LEVEL = 1
            load_level(CURRENT_LEVEL)
        elif close_btn.collidepoint(pos):
            raise SystemExit
        elif sound_btn.collidepoint(pos):
            SOUND_ON = not SOUND_ON
            if SOUND_ON:
                sound_btn.image = 'sound-button-on.png'
                try:
                    music.play('runboyrun_maze_runner_game.mp3')
                except:
                    pass
            else:
                sound_btn.image = 'sound-button-off.png'
                music.stop()
    elif GAME_STATE == 'victory' or GAME_STATE == 'game_over':
        if play_btn.collidepoint(pos):
            GAME_STATE = 'playing'
            CURRENT_LEVEL = 1
            load_level(CURRENT_LEVEL)
        elif close_btn.collidepoint(pos):
            raise SystemExit
        pass

def update_player(keyboard):
    global facing_right
    if keyboard.left:
        player.x -= 3
        facing_right = False
    if keyboard.right:
        player.x += 3
        facing_right = True

platforms = []
platform_visuals = []

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
    "jump": player_jump,

    "idle_left": player_idle_left,
    "walk_left": player_walk_left,
    "jump_left": player_jump_left
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

def animate_key(dt):
    if not key.is_collectable:
        return

    key.animation_time += dt

    if key.animation_time >= key.animation_delay:
        key.animation_time = 0
        key.frame_index = (key.frame_index + 1) % len(key_frames)
        key.image = key_frames[key.frame_index]

def load_level(level_number):
    global platforms, platform_visuals, player, moving_platform_data, key, game_over_animation, go_index, go_timer, vellocityy, GAME_STATE

    game_over_animation.image = game_over_frames[0]
    go_index = 0
    go_timer = 0
    
    platforms.clear()
    platform_visuals.clear()
    player.pos = (50, 311 - player.height * 1.5)
    vellocityy = 1

    if level_number == 1:
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
        p5 = Actor("platafforms3.png")
        p5.topleft = (286, 389)
        p5Rect = Rect(p5.topleft[0], p5.topleft[1], 33, 18)
        p6 = Actor("platafforms2.png")
        p6.topleft = (355, 335)
        p6Rect = Rect(p6.topleft[0], p6.topleft[1], 24, 24)
        p7 = Actor("platafforms2.png")
        p7.topleft = (421, 279)
        p7Rect = Rect(p7.topleft[0], p7.topleft[1], 24, 24)

        movingP = Actor("platafforms3.png")
        movingP.topleft = (30, 74)
        movingPRect = Rect(movingP.topleft[0], movingP.topleft[1], 33, 18)

        moving_platform_data = {
            'visual': movingP,
            'rect': movingPRect,
            'vx': PLATFORM_SPEED,
            'limit_left': 30,
            'limit_right': 130
        }
        
        key.topleft = (movingP.topleft[0] + 5, movingP.topleft[1] - key.height)
        key.is_collectable = True
        key.is_on_platform = True

        platforms.extend([left_ground, right_ground, p1Rect, p2Rect, p3Rect, p4Rect, moving_platform_data, p5Rect, p6Rect, p7Rect])
        platform_visuals.extend([p1, p2, p3, p4, movingP, key, p5, p6, p7])

        door.pos = (640, 271)
    
    elif level_number == 2:

        p_1 = Actor("platafforms0.png")
        p_1.topleft = (180, 292)
        p_1Rect = Rect(p_1.topleft[0], p_1.topleft[1], 84, 21)
        p_2 = Actor("platafforms1.png")
        p_2.topleft = (316, 230)
        p_2Rect = Rect(p_2.topleft[0], p_2.topleft[1], 33, 57)
        p_3 = Actor("platafforms3.png")
        p_3.topleft = (384, 230)
        p_3Rect = Rect(p_3.topleft[0], p_3.topleft[1], 33, 18)
        p_4 = Actor("platafforms1.png")
        p_4.topleft = (452, 170)
        p_4Rect = Rect(p_4.topleft[0], p_4.topleft[1], 33, 57)

        platforms.extend([left_ground, right_ground, p_1Rect, p_2Rect, p_3Rect, p_4Rect])
        platform_visuals.extend([p_1, p_2, p_3, p_4])

        monster = Actor(newt_walk[0])
        monster.topleft = (178, 292 - monster.height)
        monsterRect = Rect(monster.topleft[0], monster.topleft[1], monster.width-15, monster.height-15)

        monster_data = {
            'visual': monster,
            'rect': monsterRect,
            'vx': ENEMY_SPEED,
            'limit_left': 172,
            'limit_right': 264,
            'frames_right': newt_walk,
            'frames_left': newt_walk_left,
            'current_frame': newt_walk,
            'index': 0,
            'timer': 0,
            'anim_speed': 0.15
        }
        enemies.append(monster_data)

        door.pos = (640, 271)

    else:
        GAME_STATE = 'victory'

def update_enemies(dt):
    for e in enemies:
        e_rect = e['rect']
        e_visual = e['visual']
        e_rect.x += e['vx']
        if e['vx'] > 0:
            e['current_frame'] = e['frames_right']
        elif e['vx'] < 0:
            e['current_frame'] = e['frames_left']
        if e_rect.right > e['limit_right']:
            e['vx'] = -ENEMY_SPEED
        elif e_rect.left < e['limit_left']:
            e['vx'] = ENEMY_SPEED
        e['timer'] += dt
        if e['timer'] >= e['anim_speed']:
            e['timer'] = 0
            e['index'] = (e['index'] + 1) % len(e['current_frame'])
            e_visual.image = e['current_frame'][e['index']]
        e_visual.topleft = e_rect.topleft

on_ground = False

def update(dt):
    global vellocityy, on_ground, HAS_KEY, CURRENT_LEVEL, GAME_STATE, go_timer, go_index
    on_ground = False

    if GAME_STATE == 'victory':
        return

    if GAME_STATE == 'game_over':
        go_timer += dt
        if go_timer >= GO_ANIMATION_SPEED:
            go_timer = 0
            go_index = (go_index + 1) % len(game_over_frames)
            game_over_animation.image = game_over_frames[go_index]
        return
    if GAME_STATE == 'playing':
        update_platforms()
        update_enemies(dt)
        animate_key(dt)

        if key.is_collectable:
            if key.is_on_platform:
                key.x += moving_platform_data['vx']
            if player.colliderect(key):
                key.is_collectable = False
                key.is_on_platform = False
                HAS_KEY = True
                key.pos = (-100, -100)

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
        
        if facing_right:
            sufix = ""
        else:
            sufix = "_left"

        if not on_ground:
            animate(dt, "jump" + sufix)
        elif moving:
            animate(dt, "walk" + sufix)
        else:
            animate(dt, "idle" + sufix)

        half = player.width / 2

        if player.x < half:
            player.x = half
        elif player.x > WIDTH - half:
            player.x = WIDTH - half
        
        player.x_previous = player.x

        if player.colliderect(door):
            if HAS_KEY:
                CURRENT_LEVEL += 1
                load_level(CURRENT_LEVEL)
        
        for e in enemies:
            enemy_rect = e['rect']
            if player.colliderect(enemy_rect):
                GAME_STATE = 'game_over'
    
    if player.bottom > HEIGHT:
        GAME_STATE = 'game_over'


def draw():
    screen.clear()
    if GAME_STATE == 'menu':
        screen.blit('background_', (0,0))
        game_tittle.draw()
        play_btn.draw()
        close_btn.draw()
        sound_btn.draw()
    if GAME_STATE == 'playing':
        screen.blit('background_', (0,0))
        door.draw()
        for visual in platform_visuals:
            visual.draw()
        for e in enemies:
            e['visual'].draw()
        player.draw()
        if HAS_KEY:
            screen.blit('key.png', (10, 10))
    elif GAME_STATE == 'game_over':
        screen.blit('background_', (0,0))
        game_over_animation.draw()
    elif GAME_STATE == 'victory':
        screen.blit('background_', (0,0))
        play_btn.center = (WIDTH / 2, (HEIGHT / 2) + 50)
        close_btn.center = (WIDTH / 2, (HEIGHT / 2) + 109)
        escaped.draw()

if SOUND_ON:
    music.play('runboyrun_maze_runner_game.mp3')
    music.set_volume(0.5)

pgzrun.go()