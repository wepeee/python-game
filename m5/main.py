import random
import sys
import pygame
from pygame.locals import *
FPS = 32

frame_size_x = 289
frame_size_y = 511
window_screen = pygame.display.set_mode((frame_size_x, frame_size_y))
high_score = 0
game_sprites = {}
game_sounds = {}

player = 'gallery/sprites/astro.png'
background = 'gallery/sprites/bg.jpg'
base = 'gallery/sprites/base.jpg'
pipe = 'gallery/sprites/pipe.png'
ground_by = frame_size_y * 0.8

pygame.init()
fps_controller = pygame.time.Clock()
pygame.display.set_caption('astro man')

def main_game():
    player_x = int(frame_size_x/5)
    player_y = int(frame_size_x/2)
    global high_score
    base_x = 0
    player_jump = False
    player_jump_acc = -8
    player_vel_y = -9
    player_max_vel_y = 10
    player_acc_y = 1
    pipe_vel_x = -4
    score = 0
    new_pipe_1 = get_random_pipe()
    new_pipe_2 = get_random_pipe()
    
    upper_pipes = [
        {'x': frame_size_x + 200, 'y': new_pipe_1[0]['y']},
        {'x': frame_size_x + 200 + (frame_size_x / 2), 
        'y': new_pipe_2[0]['y']},
    ]

    lower_pipes = [
        {'x': frame_size_x + 200, 'y': new_pipe_1[1]['y']},
        {'x': frame_size_x + 200 + (frame_size_x / 2),
         'y': new_pipe_2[1]['y']},
    ]
    
    while True:
        for event in pygame.event.get():
            
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_jump_acc
                    player_jump = True
                    game_sounds['jump'].play()
        
        crash_test= is_collide(player_x, player_y, upper_pipes, lower_pipes)
        if crash_test:
            if score > high_score :
                high_score = score
            return score            
        
        player_mid_pos = player_x + game_sprites['player'].get_width()/2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipe_mid_pos<= player_mid_pos < pipe_mid_pos +4:
                score +=1
                print(f"Your score is {score}")
                game_sounds['point'].play()            
        
        if player_vel_y < player_max_vel_y and not player_jump:
            player_vel_y += player_acc_y
            
        if player_jump:
            player_jump = False
            
        player_height = game_sprites['player'].get_height()
        player_y = player_y + min(player_vel_y, ground_by - player_y - player_height)
        window_screen.blit(game_sprites['background'], (0, 0))
        
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            window_screen.blit(game_sprites['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            window_screen.blit(game_sprites['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
            
        window_screen.blit(game_sprites['base'], (base_x, ground_by))
        window_screen.blit(game_sprites['player'], (player_x, player_y))
        
        for upper_pipe , lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x
            
        if 0<upper_pipes[0]['x']<5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])
            
        if upper_pipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)
            
        score_font = pygame.font.SysFont('Impact', 32)
        score_surface = score_font.render(str(score), True,(255,255,255))
        score_rect = score_surface.get_rect()
        score_rect.midtop = (frame_size_x/2, 32)
        window_screen.blit(score_surface, score_rect)
        
        pygame.display.update()
        fps_controller.tick(FPS)
        
def game_over_screen(score):
    global high_score
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_UP):
                return
            else:
                window_screen.blit(game_sprites['background'], (0, 0))
                text_font = pygame.font.SysFont('Impact', 24)
                game_over_surface = text_font.render("Game Over !", True, (255,255,255))
                score_surface = text_font.render("Score : " + str(score), True, (255,255,255))
                continue_surface = text_font.render("Press 'ENTER' To Continue !", True, (255,255,255))
                high_score_surface = text_font.render("High Score : " + str(high_score), True, (255,255,255))
                high_score_surface = text_font.render("High Score : " + str(high_score), True, (255,255,255))
                window_screen.blit(game_over_surface, (80, 100))
                window_screen.blit(score_surface, (100, 170))
                window_screen.blit(continue_surface, (20, 230))
                window_screen.blit(high_score_surface, (80, 430) )
                pygame.display.update()
                fps_controller.tick(FPS)        

def welcome_screen():
    player_x = int(frame_size_x/5)
    player_y = int((frame_size_y - game_sprites['player'].get_height())/2)
    base_x = 0
    player_jump_acc = -8
    
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                return
            else:
                window_screen.blit(game_sprites['background'], (0, 0))
                window_screen.blit(game_sprites['player'], (player_x, player_y))
                welcome_text = pygame.font.SysFont('Impact', 32)
                welcome_surface = welcome_text.render("Astro Man", True, (255,255,255))
                welcome_rect = welcome_surface.get_rect()
                welcome_rect.midtop = (frame_size_x/2, 32)
                window_screen.blit(welcome_surface, welcome_rect)
                window_screen.blit(game_sprites['base'], (base_x, ground_by))
                pygame.display.update()
                fps_controller.tick(FPS)
                
def is_collide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > frame_size_y * 0.7 or player_y <0: 
        game_sounds['hit'].play()
        return True
    
    for pipe in upper_pipes:
        pipe_height = game_sprites['pipe'][0].get_height()
        if(player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True


    for pipe in lower_pipes:
        if (player_y + game_sprites['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True
    
    return False

def get_random_pipe():
    pipe_height = game_sprites['pipe'][0].get_height()
    offset = frame_size_y/3
    y2 = offset + random.randrange(0, int(frame_size_y - game_sprites['base'].get_height()  - 1.2 *offset))
    pipe_x = frame_size_x + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2} 
    ]
    return pipe

game_sprites['base'] = pygame.image.load(base).convert_alpha()
game_sprites['background'] = pygame.image.load(background).convert()
game_sprites['player'] = pygame.image.load(player).convert_alpha()
game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),pygame.image.load(pipe).convert_alpha())
game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
game_sounds['jump'] = pygame.mixer.Sound('gallery/audio/point.wav')

while True:
    welcome_screen()
    score = main_game()
    game_over_screen(score)

