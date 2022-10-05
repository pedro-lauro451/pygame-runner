import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk) : player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = True
start_time = 0
level_music = pygame.mixer.Sound('audio/music.wav')
level_music.set_volume(0.1)
level_music.play(loops = -1)


sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# score_surf = test_font.render('Text',False,(64,64,64))
# score = score_surf.get_rect(center = (400,50))

gameover_surf = test_font.render('Ops!',False,(64,64,64))
gameover = gameover_surf.get_rect(center = (400,100))

final_score = 0

#Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frame_index = 0
snail_frames = [snail_frame_1,snail_frame_2]
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frame_index = 0
fly_frames = [fly_frame_1,fly_frame_2]
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

#Player
player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_walk1.get_rect(midbottom = (80,300))
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.1)

player_grav = 0

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1000)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer,500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer,300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint((event.pos)):
                player_grav = -20
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                player_grav = -20
                jump_sound.play()
        if event.type == pygame.KEYDOWN and game_active == False:
            game_active = True
        if event.type == obstacle_timer and game_active == True:
            if randint(0,2):
                obstacle_rect_list.append(snail_frame_1.get_rect(bottomright = (randint(900,1000), 300))) 
            else:
                obstacle_rect_list.append(fly_frame_1.get_rect(bottomright = (randint(900,1000), 200))) 
        if event.type == snail_timer and game_active == True:
            if snail_frame_index == 0 : snail_frame_index = 1
            else: snail_frame_index = 0
            snail_surf = snail_frames[snail_frame_index]

        if event.type == fly_timer and game_active == True:
            if fly_frame_index == 0 : fly_frame_index = 1
            else: fly_frame_index = 0
            fly_surf = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf,score_rect)
        final_score = display_score()

        # snail_rect.right -= 6
        # if snail_rect.right < -100 : snail_rect.right = 900
        # screen.blit(snail_frame_1,snail_rect)

        #Gravity
        player_grav += 1
        player_rect.y += player_grav

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Stand
        player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        player_stand = pygame.transform.scale(player_stand,(120,150))
        player_stand_rect = player_stand.get_rect(center = (400,200))

        # Quicksand if player_rect.bottom >= 300 : player_grav = 0
        if player_rect.bottom >= 300 : player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

        if collisions(player_rect,obstacle_rect_list) == False: 
            game_active = False
            obstacle_rect_list = []
        
    else:
        screen.fill('#c0e8ec')
        
        pygame.draw.rect(screen,'#c0e8ec',gameover)
        screen.blit(gameover_surf,gameover)

        screen.blit(player_stand,player_stand_rect)

        final_score_surf = test_font.render(f'Final score: {final_score}',False,(64,64,64))
        final_score_rect = final_score_surf.get_rect(center = (400,320))
        screen.blit(final_score_surf,final_score_rect)

        start_time = int(pygame.time.get_ticks() / 1000)
   
    pygame.display.update()
    clock.tick(60)