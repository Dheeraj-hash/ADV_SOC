import pygame
from settings import *
pygame.init()
clock = pygame.time.Clock()
display_surf = pygame.display.set_mode((window_width,window_height))
num=0
# track_surf = pygame.surface.Surface((window_width,window_height))
# track_surf.fill((0,0,0))

# pygame.draw.circle(track_surf,'white',(window_width/2,window_height/2),300)
# pygame.draw.circle(track_surf,'black',(window_width/2,window_height/2),200)

# track_surf.set_colorkey((0,0,0))

# track_arr = pygame.surfarray.array2d(track_surf)
# print(track_arr[10,10])
track_image = pygame.image.load('./environment/track.jpg').convert_alpha()
# track_image = pygame.transform.scale(track_image,(window_width,window_height))

car_image = pygame.image.load('./environment/car.webp').convert_alpha()
car_image = pygame.transform.scale(car_image,(70,70))
car_rect = car_image.get_rect(center=(0,0))
# for x in range(car_image.get_size()[0]):
#     for y in range(car_image.get_size()[1]):
#         if car_image.get_at((x,y))[0] == 255:
#             car_image.set_at((x,y),(0,0,0)) 
            


lawn_mask = pygame.mask.from_surface(track_image)
lawn_surf = lawn_mask.to_surface()
# lawn_surf.set_colorkey((0,0,0))
display_surf.blit(track_image,(0,0))

# display_surf.blit(car_image,(130,400))

while True:
    
    if pygame.mouse.get_pos():
        car_rect.center = pygame.mouse.get_pos()
        print(pygame.mouse.get_pos())
    # lawn_surf.set_colorkey((0,0,0))
    display_surf.blit(track_image,(0,0))
    display_surf.blit(car_image,car_rect)
    num+=1
    print(num)
    pygame.display.update()
    clock.tick(FPS)