import pygame, sys, random
from pygame.locals import *
import data.engine as e

pygame.mixer.pre_init(44100, -16, 2, 200)
pygame.init()
pygame.mixer.set_num_channels(64)
e.set_global_colorkey((0,0,0))
clock = pygame.time.Clock()
pygame.display.set_caption("Neon-Runner")

WINDOW_SIZE = (1200, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((600, 400))

pygame.mixer.music.load("data/audio/music.wav")

CHUNK_SIZE = 8
def generate_chunk(x, y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        for x_pos in range(CHUNK_SIZE):
            target_x = x*CHUNK_SIZE + x_pos
            target_y = y*CHUNK_SIZE + y_pos
            tile_type = 0 # air
            if target_y > 10:
                tile_type = 1 # dirt
            elif  target_y == 10:
                tile_type = 2 # grass
            elif target_y == 9:
                if random.randint(1,5) == 1:
                    tile_type = 3 # plant
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def menu():
    running = True
    menu_background = pygame.image.load('data/images/blue_menu.png')
    game_name = pygame.image.load('data/images/neon_runner.png')
    start_option = pygame.image.load('data/images/start_option.png')
    quit_option = pygame.image.load('data/images/quit_option.png')
    menu_arrow = pygame.image.load('data/images/menu_arrow.png')
    arrow_position = 0


    menu_arrow_sound = pygame.mixer.Sound("data/audio/menu_arrow.wav")
    menu_music = pygame.mixer.Sound("data/audio/menu_music.wav")
    menu_music.set_volume(0.7)
    menu_music.play(-1)

    while running:
        
        display.blit(menu_background, (0,0))
        
        display.blit(game_name, (170, 50))
        display.blit(start_option, (260, 170))
        display.blit(quit_option, (270, 230))

        display.blit(menu_arrow, (220, 170 + arrow_position*60))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if arrow_position != 1:
                        arrow_position = 1
                        menu_arrow_sound.play()
                if event.key == K_UP:
                    if arrow_position != 0:
                        arrow_position = 0
                        menu_arrow_sound.play()
                if event.key == K_RETURN:
                    if arrow_position:
                        pygame.quit()
                        sys.exit()
                    else:
                        running = False
            if event.type == KEYUP:
                pass
        
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)

    menu_music.fadeout(5)

def pause():
    running = True
    pause_menu_background = pygame.image.load('data/images/pause_menu_background.png')
    game_name = pygame.image.load('data/images/neon_runner_pause.png')
    continue_pause = pygame.image.load('data/images/continue_pause.png')
    quit_pause = pygame.image.load('data/images/quit_pause.png')
    restart_option = pygame.image.load('data/images/restart_option.png')
    pause_menu_arrow = pygame.image.load('data/images/pause_arrow.png')
    arrow_position = 0

    menu_arrow_sound = pygame.mixer.Sound("data/audio/menu_arrow.wav")

    while running:
        display.blit(pause_menu_background, (0,0))
        
        display.blit(game_name, (170, 50))
        display.blit(continue_pause, (230, 170))
        display.blit(restart_option, (235, 230))
        display.blit(quit_pause, (270, 290))

        arrow_x_pad = 30 if arrow_position in [0,1] else 0
        display.blit(pause_menu_arrow, (220 - arrow_x_pad, 170 + arrow_position*60))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if arrow_position != 2:
                        arrow_position += 1
                        menu_arrow_sound.play()
                if event.key == K_UP:
                    if arrow_position != 0:
                        arrow_position -= 1
                        menu_arrow_sound.play()
                if event.key == K_RETURN:
                    if arrow_position == 2:
                        pygame.quit()
                        sys.exit()
                    elif arrow_position == 0:
                        running = False
                    elif arrow_position == 1:
                        return 1
                if event.key == K_ESCAPE:
                    running = False
            if event.type == KEYUP:
                pass
        
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)

def lose():
    running = True
    menu_background = pygame.image.load('data/images/finish_menu.png')
    restart_option = pygame.image.load('data/images/restart_finish.png')
    quit_option = pygame.image.load('data/images/quit_finish.png')
    finish_arrow = pygame.image.load('data/images/finish_arrow.png')
    finish_msg = pygame.image.load('data/images/finish_msg.png')
    arrow_position = 0

    menu_arrow_sound = pygame.mixer.Sound("data/audio/menu_arrow.wav")

    while running:
        display.blit(menu_background, (0,0))
        
        display.blit(finish_msg, (200, 50))
        display.blit(restart_option, (235, 170))
        display.blit(quit_option, (270, 230))

        arrow_x_pad = 30 if arrow_position in [0] else 0
        display.blit(finish_arrow, (220 - arrow_x_pad, 170 + arrow_position*60))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if arrow_position != 1:
                        arrow_position += 1
                        menu_arrow_sound.play()
                if event.key == K_UP:
                    if arrow_position != 0:
                        arrow_position -= 1
                        menu_arrow_sound.play()
                if event.key == K_RETURN:
                    if arrow_position == 1:
                        pygame.quit()
                        sys.exit()
                    elif arrow_position == 0:
                        running = False
                        return 1
            if event.type == KEYUP:
                pass
        
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)


def gameplay(display, init_player_x = 100, init_player_y = 100):
    

    moving_right = False
    moving_left = False
    moving_fast = False
    dash_timer = 0
    player_y_momentum = 0
    air_timer = 0
    hurt = False
    no_hurt_timer = 0
    player_health = 5
    coins_collected = 0

    true_scroll = [0,0]

    my_font = pygame.font.SysFont('Comic Sans MS', 30)


    blue_tile_0 = pygame.image.load("data/images/blue_tile_0.png")
    blue_tile_1 = pygame.image.load("data/images/blue_tile_1.png")
    blue_tile_2 = pygame.image.load("data/images/blue_tile_2.png")
    blue_tile_4 = pygame.image.load("data/images/blue_tile_4.png")

    TILE_SIZE = blue_tile_0.get_width()
    TILE_SIZE = TILE_SIZE*2//3

    h_bar_image = pygame.image.load("data/images/blue_tile_3.png")
    h_bar_image = pygame.transform.scale(h_bar_image, (TILE_SIZE, TILE_SIZE))

    blue_coin_count = pygame.image.load("data/images/blue_coin_count.png")
    blue_coin_count = pygame.transform.scale(blue_coin_count, (TILE_SIZE, TILE_SIZE))

    tile_index = {
        0:blue_tile_0,
        1:blue_tile_1,
        2:blue_tile_2,
        4:blue_tile_4
    }

    for tile in tile_index.keys():
        tile_index[tile] = pygame.transform.scale(tile_index[tile], (TILE_SIZE, TILE_SIZE))

    jump_sound = pygame.mixer.Sound("data/audio/jump.wav")
    hurt_sound = pygame.mixer.Sound("data/audio/hurt.wav")
    pickup_sound = pygame.mixer.Sound("data/audio/coin_pickup.wav")
    jump_sound.set_volume(0.5)
    hurt_sound.set_volume(0.3)

    game_map = load_map('data/maps/01')
    e.load_animations('data/images/entities/')

    player = e.entity(init_player_x, init_player_y, 32, 32, 'player')

    anti_blue_coords = [(450,200), (800,200), (1000,250)]
    anti_blue_list = [e.entity(x[0], x[1], 51, 58, 'anti_blue') for x in anti_blue_coords]

    blue_coin_coords = [(1400, 350)]
    blue_coin_list = [e.entity(x[0], x[1], 51, 58, 'blue_coin') for x in blue_coin_coords]

    running = True
    while running:
        display.fill((0,0,0))

        pygame.draw.rect(display, (0,0,0),pygame.Rect(200, 0, 400, 400))

        true_scroll[0] += (player.x - true_scroll[0] - 316)/20
        true_scroll[1] += (player.y - true_scroll[1] - 216)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        tile_rects = []

        for y, row in enumerate(game_map):
            for x, tile_code in enumerate(row):
                if int(tile_code) not in [1, 3, 4]:
                    display.blit(tile_index[int(tile_code)], (x*TILE_SIZE - scroll[0],y*TILE_SIZE - scroll[1]))
                    tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if int(tile_code) not in [3]:
                    display.blit(tile_index[int(tile_code)], (x*TILE_SIZE - scroll[0],y*TILE_SIZE - scroll[1]))

        for h_bar in range(player_health):
            display.blit(h_bar_image, (10 + 23*h_bar, 10))

        display.blit(blue_coin_count, (250, 10))
        display.blit(my_font.render('x ' + str(coins_collected), False, (1,146,240)), (290, 30))

        # Setting speed according to key presses
        player_movement = [0,0]
        if moving_right:
            player_movement[0] += 3
        elif moving_left:
            player_movement[0] -= 3
        if moving_fast:
            player_movement[0] *= 2

        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        no_hurt_timer -= 0.2
        
        if no_hurt_timer < 0:
            no_hurt_timer = 0
        if player_y_momentum > 5:
            player_y_momentum = 5
        if e.collision_test(player, [x.rect() for x in anti_blue_list]) and no_hurt_timer == 0:
            no_hurt_timer = 10
            hurt = True
            hurt_sound.play(loops=3, fade_ms=5)
            player_health -= 1
            
            if player_health <= 0:
                return 2
        elif true_scroll[1] > 200 and no_hurt_timer == 0:
            no_hurt_timer = 10
            hurt = True
            hurt_sound.play(loops=3, fade_ms=5)
            player_health -= 2
            if player_health <= 0:
                return 2
        elif no_hurt_timer == 0:
            hurt = False
        
        for coin in blue_coin_list:
            if e.collision_test(player, [coin.rect()]) and coin.action == 'idle':
                pickup_sound.play()
                coin.set_action('active')
                coins_collected += 1

        if hurt and player_movement[0] > 0:
            player.set_action('hurt')
            player.set_flip(False)
        elif hurt and player_movement[0] < 0:
            player.set_action('hurt')
            player.set_flip(True)
        elif hurt and player_movement[0] == 0:
            player.set_action('hurt')
        elif player_movement[0] > 0 and moving_fast:
            player.set_action('dash')
            player.set_flip(False)
        elif player_movement[0] < 0 and moving_fast:
            player.set_action('dash')
            player.set_flip(True)
        elif player_movement[0] > 0:
            player.set_action('run')
            player.set_flip(False)
        elif player_movement[0] < 0:
            player.set_action('run')
            player.set_flip(True)
        elif player_movement[0] == 0:
            player.set_action('idle')


        collision_types = player.move(player_movement, tile_rects)

        if collision_types['bottom']:
            player_y_momentum = 0
            air_timer = 0

        else:
            air_timer += 1
        if collision_types['top']:
            player_y_momentum = 0

        player.change_frame(1)
        player.display(display, scroll)
        
        for x in anti_blue_list:
            x.change_frame(1)
            x.display(display, scroll)

        for x in blue_coin_list:
            x.change_frame(1)
            x.display(display, scroll)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_SPACE:
                    if air_timer < 6:
                        player_y_momentum = -6
                        jump_sound.play()
                if event.key == K_LSHIFT:
                    moving_fast = True
                if event.key == K_ESCAPE:
                    pygame.mixer.music.set_volume(0.3)
                    pause_ret = pause()
                    if pause_ret == 1:
                        return 1

                    pygame.mixer.music.set_volume(1)
            
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
                if event.key == K_LSHIFT:
                    moving_fast = False

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))


        pygame.display.update()
        clock.tick(60)

menu()

pygame.mixer.music.play(-1)

while True:
    return_val = gameplay(display)
    if return_val == 2:
        return_val = lose()
    if return_val != 1:
        break

