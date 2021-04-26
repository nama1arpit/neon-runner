import pygame, sys, random
from pygame.locals import *
import data.engine as e

pygame.mixer.pre_init(44100, -16, 2, 100)
pygame.init()
pygame.mixer.set_num_channels(64)
e.set_global_colorkey((0,0,0))
clock = pygame.time.Clock()
pygame.display.set_caption("Neon-Runner")

title_font = pygame.font.Font("data/font/Hippauf-G01O.ttf", 40)
subtitle_font = pygame.font.Font("data/font/Hippauf-G01O.ttf", 25)
small_font = pygame.font.Font("data/font/Hippauf-G01O.ttf", 20)
smaller_font = pygame.font.Font("data/font/Hippauf-G01O.ttf", 15)

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
    f = open(path + '.csv','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(row.split(','))
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
        
        display.blit(title_font.render("Neon Runner", 0, (39, 13, 52)), (160,50))
        display.blit(subtitle_font.render("start", 0, (134, 40, 107)), (265, 170))
        display.blit(subtitle_font.render("quit", 0, (134, 40, 107)), (275, 230))
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
    pause_menu_arrow = pygame.image.load('data/images/pause_arrow.png')
    arrow_position = 0

    menu_arrow_sound = pygame.mixer.Sound("data/audio/menu_arrow.wav")

    while running:
        display.blit(pause_menu_background, (0,0))
        
        display.blit(title_font.render("Neon Runner", 0, (1,0,246)), (160, 50))
        display.blit(subtitle_font.render("continue", 0, (0,147,240)), (235, 170))
        display.blit(subtitle_font.render("restart", 0, (0,147,240)), (245, 230))
        display.blit(subtitle_font.render("quit", 0, (0,147,240)), (270, 290))

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

def lose(coins_collected):
    running = True
    menu_background = pygame.image.load('data/images/finish_menu.png')
    finish_arrow = pygame.image.load('data/images/finish_arrow.png')
    arrow_position = 0

    menu_arrow_sound = pygame.mixer.Sound("data/audio/menu_arrow.wav")
    lose_music = pygame.mixer.Sound("data/audio/lose_music.wav")
    # lose_music.set_volume(0.5)
    lose_music.play(-1)

    score = coins_collected*20

    while running:
        display.blit(menu_background, (0,0))
        
        display.blit(title_font.render("You Lost!", 0, (172,21,68)), (190, 50))
        display.blit(subtitle_font.render(f"score: {score}", 0, (210,34,70)), (230, 170))
        display.blit(subtitle_font.render("restart", 0, (210,34,70)), (245, 230))
        display.blit(subtitle_font.render("quit", 0, (210,34,70)), (270, 290))

        arrow_x_pad = 30 if arrow_position in [0] else 0
        display.blit(finish_arrow, (220 - arrow_x_pad, 230 + arrow_position*60))

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
                        lose_music.stop()
                        return 1
            if event.type == KEYUP:
                pass
        
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)
    lose_music.stop()

def win(coins_collected):
    running = True
    menu_background = pygame.image.load('data/images/finish_menu.png')
    finish_arrow = pygame.image.load('data/images/finish_arrow.png')
    arrow_position = 0

    menu_arrow_sound = pygame.mixer.Sound("data/audio/menu_arrow.wav")
    win_music = pygame.mixer.Sound("data/audio/win_music.wav")
    # win_music.set_volume()
    win_music.play(-1)

    score = coins_collected*20

    while running:
        display.blit(menu_background, (0,0))
        
        display.blit(title_font.render("You Won!", 0, (172,21,68)), (190, 50))
        display.blit(subtitle_font.render(f"score: {score}", 0, (210,34,70)), (230, 170))
        display.blit(subtitle_font.render("restart", 0, (210,34,70)), (245, 230))
        display.blit(subtitle_font.render("quit", 0, (210,34,70)), (270, 290))

        arrow_x_pad = 30 if arrow_position in [0] else 0
        display.blit(finish_arrow, (220 - arrow_x_pad, 230 + arrow_position*60))

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
                        win_music.stop()
                        return 1
            if event.type == KEYUP:
                pass
        
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)
    win_music.stop()

def get_coordinates_from_map(game_map, tile_id, tile_size):
    
    coord_list = []
    for y, row in enumerate(game_map):
        for x, tile_code in enumerate(row):
            if int(tile_code) == tile_id:  
                coord_list.append((x*tile_size, y*tile_size))

    return coord_list


def gameplay(display, init_player_x = 100, init_player_y = 200):

    moving_right = False
    moving_left = False
    moving_fast = False
    dash_timer = 0
    player_y_momentum = 0
    air_timer = 0
    dash_timer = 0
    hurt = False
    no_hurt_timer = 0
    player_health = 5
    coins_collected = 0
    bolts_collected = 0
    boss_started = False

    screen_shake = 0
    true_scroll = [0,0]

    blue_tile_0 = pygame.image.load("data/images/blue_tile_0.png")
    blue_tile_1 = pygame.image.load("data/images/blue_tile_1.png")
    blue_tile_2 = pygame.image.load("data/images/blue_tile_2.png")
    blue_tile_4 = pygame.image.load("data/images/blue_tile_4.png")

    TILE_SIZE = blue_tile_0.get_width()
    TILE_SIZE = TILE_SIZE*6//10

    h_bar_image = pygame.image.load("data/images/blue_tile_3.png")
    h_bar_image = pygame.transform.scale(h_bar_image, (TILE_SIZE, TILE_SIZE))
    villain_h_bar_image = pygame.image.load("data/images/villain_heart.png")
    villain_h_bar_image = pygame.transform.scale(villain_h_bar_image, (TILE_SIZE//2, TILE_SIZE//2))

    blue_coin_count = pygame.image.load("data/images/blue_coin_count.png")
    blue_coin_count = pygame.transform.scale(blue_coin_count, (TILE_SIZE, TILE_SIZE))

    blue_bolt_count = pygame.image.load("data/images/bolt_count.png")
    blue_bolt_count = pygame.transform.scale(blue_bolt_count, (TILE_SIZE, TILE_SIZE))
    
    tile_index = {
        0: blue_tile_0,
        1: blue_tile_1,
        2: blue_tile_2,
        4: blue_tile_4,
        7: pygame.image.load("data/images/entities/blue_coin/idle/idle_0.png"),
        8: pygame.image.load("data/images/entities/blue_bolt/idle/idle_0.png")
    }

    for tile in tile_index.keys():
        tile_index[tile] = pygame.transform.scale(tile_index[tile], (TILE_SIZE, TILE_SIZE))

    jump_sound = pygame.mixer.Sound("data/audio/jump.wav")
    hurt_sound = pygame.mixer.Sound("data/audio/hurt.wav")
    villain_dash_sound = pygame.mixer.Sound("data/audio/villain_dash.wav")
    pickup_sound = pygame.mixer.Sound("data/audio/coin_pickup.wav")
    bolt_pickup_sound = pygame.mixer.Sound("data/audio/bolt_pickup.wav")
    boss_music = pygame.mixer.Sound("data/audio/boss_music.wav")
    dash_sound = pygame.mixer.Sound("data/audio/player_dash.wav")
    jump_sound.set_volume(0.3)
    hurt_sound.set_volume(0.3)


    game_map = load_map('data/maps/level1')
    e.load_animations('data/images/entities/')

    player = e.entity(init_player_x, init_player_y, 32, 32, 'player')
    villain = {
        'entity': e.entity(2500, 400, 64, 64, 'villain'),
        'movement': [0,0],
        'y_momentum': 0,
        'dash_timer': 0,
        'collision_types': {},
        'hurt': True,
        'no_hurt_timer': 0,
        'health': 5,
        'hurt_sound': pygame.mixer.Sound('data/audio/villain_hurt.wav'),
        'dash_move': 0,
        'jump': False,
        'move_direction': ''
    }

    anti_blue_coords = [(450,200), (800,200), (1000,250)]
    # anti_blue_list = [e.entity(x[0], x[1], 51, 58, 'anti_blue') for x in anti_blue_coords]
    anti_blue_list = []

    blue_coin_coords = get_coordinates_from_map(game_map, 7, TILE_SIZE) #[(1400, 350)]
    blue_coin_coords = [(x, y+8) for (x,y) in blue_coin_coords]
    blue_coin_list = [e.entity(x[0], x[1], 51, 58, 'blue_coin') for x in blue_coin_coords]

    blue_bolt_coords = get_coordinates_from_map(game_map, 8, TILE_SIZE) #[(300, 400), (600, 650)]
    blue_bolt_list = [e.entity(x[0], x[1], 32, 32, 'blue_bolt') for x in blue_bolt_coords]

    running = True
    while running:
        display.fill((0,0,0))

        pygame.draw.rect(display, (0,0,0),pygame.Rect(200, 0, 400, 400))

        true_scroll[0] += (player.x - true_scroll[0] - 316)/20
        true_scroll[1] += (player.y - true_scroll[1] - 216)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        if screen_shake > 0:
            screen_shake -= 1

        if screen_shake:
            scroll[0] += random.randint(0,8) - 4
            scroll[1] += random.randint(0,8) - 4
        

        tile_rects = []

        if player.x > 2150 and boss_started == False:
            pygame.mixer.music.stop()
            boss_music.set_volume(0.5)
            boss_music.play()
            boss_started = True

        for y, row in enumerate(game_map):
            for x, tile_code in enumerate(row):
                if int(tile_code) not in [-1, 1, 4, 7, 8]:
                    display.blit(tile_index[int(tile_code)], (x*TILE_SIZE - scroll[0],y*TILE_SIZE - scroll[1]))
                    tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                if int(tile_code) not in [-1, 7, 8]:
                    display.blit(tile_index[int(tile_code)], (x*TILE_SIZE - scroll[0],y*TILE_SIZE - scroll[1]))

        for h_bar in range(player_health):
            display.blit(h_bar_image, (10 + 23*h_bar, 10))
        # for h_bar in range(villain['health']):
        #     display.blit(villain_h_bar_image, (500 + 23*h_bar, 10))
        display.blit(villain_h_bar_image, (villain['entity'].x - scroll[0], villain['entity'].y - scroll[1] - 15))
        display.blit(smaller_font.render(f'{villain["health"]}', False, (248, 64, 78)), (villain['entity'].x - scroll[0] + 30, villain['entity'].y - scroll[1] - 15))

        display.blit(blue_coin_count, (200, 10))
        display.blit(small_font.render(f'x {coins_collected}', False, (1,146,240)), (240, 25))

        display.blit(blue_bolt_count, (300, 10))
        display.blit(small_font.render(f'x {bolts_collected}', False, (1,146,240)), (340, 25))

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

        dash_timer -= 0.1
        villain['dash_timer'] += 0.1
        villain['no_hurt_timer'] -=0.2


        if villain["dash_timer"] < 1:
            if villain['entity'].x > player.x + 2:
                villain['move_direction'] = 'left'
            else:
                villain['move_direction'] = 'right'
            villain['dash_move'] = abs(villain['entity'].x - player.x - 2)

        if villain["move_direction"] == 'left' and player.x > 2100:
            if villain['dash_timer'] > 10:
                villain['movement'][0] = 0
                villain["dash_timer"] = 0
                villain['jump'] = True

            elif villain['dash_timer'] > 8:
                villain['movement'][0] = -18 #speed
                if villain['jump']:
                    villain['y_momentum'] = -1.8
                    villain['jump'] = False

            elif villain['dash_timer'] > 7:
                villain['jump'] = True

            elif villain['dash_timer'] > 3:
                villain['movement'][0] = -5
                if villain['jump']:
                    villain['y_momentum'] = -1.8
                    villain['jump'] = False
            
            elif villain['dash_timer'] > 1:
                villain['movement'][0] = 0

        if villain["move_direction"] == 'right' and player.x > 2100:
            if villain['dash_timer'] > 10:
                villain['movement'][0] = 0
                villain["dash_timer"] = 0
                villain['jump'] = True

            elif villain['dash_timer'] > 8:
                villain['movement'][0] = 18
                if villain['jump']:
                    villain['y_momentum'] = -1.8
                    villain['jump'] = False

            elif villain['dash_timer'] > 7:
                villain['jump'] = True
            
            elif villain['dash_timer'] > 3:
                villain['movement'][0] = 5
                if villain['jump']:
                    villain['y_momentum'] = -1.8
                    villain['jump'] = False
            
            elif villain['dash_timer'] > 1:
                villain['movement'][0] = 0

        # if random.randint(0,100) == 0:
        #     villain['y_momentum'] = -1.8

        villain['movement'][1] += villain['y_momentum']

        villain['y_momentum'] += 0.2
        villain['collision_types'] = villain['entity'].move(villain['movement'], tile_rects)
        if villain['collision_types']['bottom']:
            villain['y_momentum'] = 0
            villain['movement'][1] = 0
            # pass
        if villain['collision_types']['top']:
            villain['y_momentum'] = 5
            # pass
        if villain['y_momentum'] > 5:
            villain['y_momentum'] = 5
        
        if villain['no_hurt_timer'] < 0:
            villain['no_hurt_timer'] = 0
        if villain['no_hurt_timer'] == 0:
            villain['hurt'] = False
        if villain['hurt'] == False:
            villain['entity'].set_action("idle")


        if no_hurt_timer < 0:
            no_hurt_timer = 0
        if dash_timer < 0:
            dash_timer = 0
        if dash_timer == 0:
            moving_fast = False
        if player_y_momentum > 5:
            player_y_momentum = 5
        if e.collision_test(player, [x.rect() for x in anti_blue_list]) and no_hurt_timer == 0:
            no_hurt_timer = 10
            hurt = True
            hurt_sound.play()
            player_health -= 1
        if e.collision_test(player, [villain['entity'].rect()]) and no_hurt_timer == 0:
            
            if player.y + 16 < villain['entity'].y and villain['no_hurt_timer'] == 0:
                player_y_momentum = -5
                no_hurt_timer = 10
                coins_collected +=1
                pickup_sound.play()

                villain['no_hurt_timer'] = 10
                villain['hurt'] = True
                villain['hurt_sound'].play()
                villain['health'] -= 1

                if villain['hurt'] and villain['movement'][0] > 0:
                    villain['entity'].set_action('hurt')
                    villain['entity'].set_flip(False)
                elif villain['hurt'] and villain['movement'][0] > 0:
                    villain['entity'].set_action('hurt')
                    villain['entity'].set_flip(True)
                elif villain['hurt'] and villain['movement'][0] == 0:
                    villain['entity'].set_action('hurt')
            else:            
                no_hurt_timer = 10
                hurt = True
                hurt_sound.play()
                player_health -= 1
            
            if villain['health'] <= 0:
                # You win
                pass

            if villain['health'] <= 0:
                boss_music.stop()
                return 3, coins_collected
            if player_health <= 0:
                boss_music.stop()
                return 2, coins_collected
        elif true_scroll[1] > 800 and no_hurt_timer == 0:
            no_hurt_timer = 10
            hurt = True
            hurt_sound.play()
            player_health -= 2
            if player_health <= 0:
                return 2, coins_collected
        elif no_hurt_timer == 0:
            hurt = False
        
        for coin in blue_coin_list:
            if e.collision_test(player, [coin.rect()]) and coin.action == 'idle':
                pickup_sound.play()
                coin.set_action('active')
                coins_collected += 1

        for bolt in blue_bolt_list:
            if e.collision_test(player, [bolt.rect()]) and bolt.action == 'idle':
                bolt_pickup_sound.play()
                bolt.set_action('active')
                bolts_collected += 1

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

        villain['entity'].change_frame(1)
        villain['entity'].display(display, scroll)
        
        for x in anti_blue_list:
            x.change_frame(1)
            x.display(display, scroll)
            pass

        for x in blue_coin_list:
            x.change_frame(1)
            x.display(display, scroll)

        for x in blue_bolt_list:
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
                if event.key == K_LSHIFT and dash_timer == 0:
                    if bolts_collected > 0:
                        moving_fast = True
                        dash_sound.set_volume(0.4)
                        dash_sound.play()
                        dash_timer = 15
                        bolts_collected -= 1
                        screen_shake = 150

                # if event.key == K_k:
                #     villain['y_momentum'] = -1.5
                if event.key == K_ESCAPE:
                    pygame.mixer.music.set_volume(0.3)
                    pause_ret = pause()
                    if pause_ret == 1:
                        return 1, coins_collected

                    pygame.mixer.music.set_volume(1)
            
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))


        pygame.display.update()
        clock.tick(60)

menu()



while True:
    pygame.mixer.music.play(-1)
    return_val, coins_collected = gameplay(display)
    if return_val == 2:
        return_val = lose(coins_collected)
    if return_val == 3:
        return_val = win(coins_collected)
    if return_val != 1:
        break

