import main
import pygame ,sys, random
from pygame.locals import *


# initialize game engine
pygame.init()

window_width = 840
window_height = 800
Color = (27, 225, 45)
display_surface = pygame.display.set_mode((window_width, window_height))

textY = 450.0
ALPHA = 0

music = pygame.mixer.Sound(random.choice(['./Sounds/music.mp3', './Sounds/music2.mp3']))
music.set_volume(0.45)


animation_increment = 10
clock_tick_rate = 60
UPDATE = pygame.USEREVENT
pygame.time.set_timer(UPDATE, int(1000/55))

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)


clock = pygame.time.Clock()
background_image = pygame.transform.scale(pygame.image.load("./Images/start_back.jpg").convert(), (window_width + 400, window_height + 1))

def write_text(surface, text, size, x, y, alpha=255, color=Color):
    font = pygame.font.Font("./Fonts/chintzy.ttf", size)
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(alpha)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def startScreen():
    screen.blit(background_image, [0, 0])  
    write_text(display_surface, "Welcome to OnComing Road!" , 50, 420,255, ALPHA)
    write_text(display_surface, 'High Score: ' + str(open("./Data/info.txt", "r").read()) , 39, 420,315, ALPHA)
    write_text(display_surface, "PRESS [SPACE] TO PLAY" , 43,420,textY, ALPHA )
    write_text(display_surface, "created by Davit Makaryan, Vardan Davtyan and Sevak Davtyan" , 24, 420, window_height - 40, ALPHA-15, (255, 255, 255) )

#switch the screens
def main_start():
    
    global textY, ALPHA
    #text animation arguments
    increment = 0
    axis = -1
    max = 40
    
    pygame.init()
    pygame.display.set_icon(pygame.image.load('./Images/icon.png'))
    pygame.display.set_caption('On Coming Road')
    pygame.mixer.Channel(0).play(music, -1)  
    
    while True:      
        for event in pygame.event.get():
            
            startScreen()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main.run() 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == UPDATE:
                #text animation
                if increment < max:
                    increment += 1
                    textY += axis*1.5
                elif increment == max:
                    increment = 0
                    axis *= -1
                if ALPHA <= 255:
                    ALPHA += 5
                    
        pygame.display.flip()
        clock.tick(clock_tick_rate)


                
