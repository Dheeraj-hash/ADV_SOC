import pygame
from settings import *
from random import randint,choice
 
pygame.init()
clock=pygame.time.Clock()
num=0
gameover = False
score = 0
start_time=0

game_music = pygame.mixer.Sound("./sounds/music.wav")
game_music.set_volume(0.5)
game_music.play(loops= -1)

jump_music = pygame.mixer.Sound("./sounds/jump.wav")
jump_music.set_volume(0.5)

score_font = pygame.font.Font("./graphics/font/BD_Cartoon_Shout.ttf",45)
score_surf = score_font.render(f'Score : {score}',True,'black')
score_rect = score_surf.get_rect(center = (window_width/2,window_height/5))
replay_surf = score_font.render(f'Press space ',True,'black')
replay_rect = replay_surf.get_rect(center = (window_width/1.9,window_height/1.8))

obstacle_add = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_add,1700)
obstacle_list = []
display_surf = pygame.display.set_mode((window_width,window_height))
display_surf.fill((125,125,125)) 

sky_image = pygame.image.load("./graphics/environment/background.png")
scaling_fac = window_height/sky_image.get_height()

sky_size=sky_image.get_size()
sky_image=pygame.transform.scale(sky_image,(sky_size[0] *2,sky_size[1] *2))
sky_size=sky_image.get_size()

sky_surf = pygame.surface.Surface((sky_size[0] *2,sky_size[1] *2))
sky_rect_1 = sky_surf.get_rect(topleft=(0,0))
sky_rect_2 = sky_image.get_rect(topleft = (sky_size[0],0))
sky_surf.blit(sky_image,sky_rect_1)
sky_surf.blit(sky_image,sky_rect_2)
sky_rect=sky_surf.get_rect(topleft=(0,0))
display_surf.blit(sky_surf,sky_rect)

surf = pygame.image.load(f'./graphics/obstacles/{choice((0,1))}.png').convert_alpha()
image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * 1.6)
obstacle_image = [image]
surf_1 = pygame.image.load(f'./graphics/obstacles/{choice((0,1))}.png').convert_alpha()
image_1 = pygame.transform.scale(surf_1,pygame.math.Vector2(surf.get_size()) * 1.6)
image_1 = pygame.transform.flip(image_1,False,True)
obstacle_image.append(image_1)
obstacle_mask = [pygame.mask.from_surface(im) for im in obstacle_image]
# display_surf.blit(obstacle_image[0],obstacle_rect)

player_list = []
player_index =0
for i in range(3):
    player_image = pygame.image.load(f'./graphics/plane/red{i}.png')
    player_image = pygame.transform.rotozoom(player_image,0,1.2)
    player_list.append(player_image)

player_rec = player_list[0].get_rect(center=(window_width/2.5,window_height/2))
player_mask = pygame.mask.from_surface(player_image)
display_surf.blit(player_image,player_rec)

gravity=2

while True:
    
    for event in pygame.event.get():

        if gameover:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    gameover=False
                    index =0
                    gravity = 2
                    sky_rect.x =0
                    player_rec.center=(window_width/2,window_height/2)
                    obstacle_list.clear()
                    start_time = pygame.time.get_ticks()/1000
        else:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    gravity = -20 
                    jump_music.play()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                gravity = -20
                jump_music.play()
            elif event.type == obstacle_add:  
                index = choice([0,1])       
                if index:   
                    obstacle_list.append([obstacle_image[1],obstacle_image[1].get_rect(topleft = (randint(window_width + 50, window_width + 100),choice([-50,-100,-150 ]))),obstacle_mask[1]])
                # image_list.append(image_1)
                else:
                    obstacle_list.append([obstacle_image[0],obstacle_image[0].get_rect(bottomleft = (randint(window_width + 50, window_width + 100),choice([window_height+50,window_height+100,window_height+150 ]))),obstacle_mask[0]])
                # image_list.append(image)
        
        

    # print(obstacle_list)
    player_index += 1
    player_index %= 3    

    if gameover:
        display_surf.fill('grey')
        display_surf.blit(score_surf,score_surf.get_rect(center = (window_width/2,window_height/4)))
        display_surf.blit(player_list[player_index],(window_width/3,window_height/3))
        display_surf.blit(replay_surf,replay_rect)
    
    else:
        if player_rec.top < 0 or player_rec.bottom> window_height:
            gameover = True

        sky_rect.x -= 10
        if  sky_rect.centerx == 0:
          sky_rect.x = 0
        gravity += 1
        player_rec.y += gravity
        display_surf.fill((125,125,125))
        display_surf.blit(sky_surf,sky_rect)
    # display_surf.blit(image,image.get_rect(bottomleft= (window_width/2.5,window_height)))

        # if pygame.mouse.get_pos():
        #     player_rec.x = pygame.mouse.get_pos()[0]
        #     player_rec.y = pygame.mouse.get_pos()[1]

    # offset_x = window_width/2.5 - player_rec.x
    # offset_y = window_height - image.get_height() - player_rec.bottom

    # print(f'x:{offset_x} y:{offset_y}')
    # if player_mask.overlap(obstacle_mask[0],(offset_x,offset_y)):
    #     print("Game Ends") 
        for index in range(len(obstacle_list)):
        # print(index)
            obstacle_list[index][1].x -= 10
        # if obstacle_list[index][1].x > 0 and obstacle_list[index][1].x < window_width:
        #     print(f'x:{offset_x} y:{offset_y}')
            display_surf.blit(obstacle_list[index][0],obstacle_list[index][1])
            offset_x = obstacle_list[index][1].x - player_rec.x
            offset_y = obstacle_list[index][1].y - player_rec.y
            
            if player_mask.overlap(obstacle_list[index][2],(offset_x,offset_y)):
            # num+=1
            # print(num)
                gameover = True
        # print(obstacle_list[index].x,end= ",")
        # display_surf.blit(obstacle_image[0],obstacle_list[index])
        # if obstacle_list[index].x < -50:
        #     del(obstacle_list[index])
    # obstacle_list = [obstacle for obstacle in obstacle_list if obstacle[1].x > -200]

    # for index in range(len(obstacle_list)):
    #     display_surf.blit(obstacle_image[1],obstacle_list[index])
        # print(index)
        display_surf.blit(pygame.transform.rotate(player_list[player_index],-1*gravity/3),player_rec)

        score = pygame.time.get_ticks() / 1000
        net_score = int(score - start_time ) 
        score_surf = score_font.render(f'Score : {net_score}',True,'black')
        display_surf.blit(score_surf,score_rect)
    
    
    pygame.display.update()
    clock.tick(FPS)
    