import pygame, sys, random
from pygame.locals import *

def run():
    
    pygame.init() 
   
    sizeX = 840
    sizeY = 800
    DISPLAYSURF = pygame.display.set_mode((sizeX, sizeY))
    pygame.display.set_icon(pygame.image.load('./Images/icon.png'))
    pygame.display.set_caption('On Coming Road')
    
    #Update
    clock = pygame.time.Clock()
    UPDATE = pygame.USEREVENT
    pygame.time.set_timer(UPDATE, int(1000/60))
    
    #Asphalt
    bgY = 0;
    bgY_2 = 0 - bgY
    backgroundSpeed = 7.0
    backgroundImage = pygame.transform.scale(pygame.image.load(r'./Images/background.png'), (sizeX, sizeY))
    
    #game hard mode parameters
    triggered = True
    hardIndex = 25
    
    #Player
    isAlive = True
    carScaleX, carScaleY = 75, 170
    X = int(sizeX/2 - carScaleX/2)
    Y = int(sizeY - carScaleY - 2)
    playerImg = pygame.image.load(r'./Images/Audi.png')
    player = pygame.transform.scale(playerImg, (carScaleX, carScaleY))
    forwardSpeed, sideSpeed, bottomSpeed = 15, 18, 9
    rideSound = pygame.mixer.Sound('./Sounds/riding1.ogg')
    rideSound.set_volume(0.25)
    
    music = pygame.mixer.Sound('./Sounds/music.mp3')
    music.set_volume(0.45)
    
    
    #Enemies
    carImages = [ './Images/Car.png', './Images/Ambulance.png', './Images/Police.png', './Images/Black_viper.png', './Images/Mini_truck.png' ]
    enemyLength = 3
    enemySpeed = backgroundSpeed + 1
    enemies = []
    crashSound = pygame.mixer.Sound('./Sounds/NFF-car-hit.wav')
    crashSound.set_volume(0.4)

    #Coins
    f = open("./Data/info.txt", "r")
    HighScore = int(f.read())
    Score = 0
    
    coinSpeed = backgroundSpeed
    coinCount = 8
    coins = []
    coinPicking = pygame.mixer.Sound('./Sounds/coin.wav')
    coinPicking.set_volume(0.3)

    #Colors
    RED=(255,0,0)
    GREEN=(0,230,0)
    
    #animation arguments
    increment = 0
    axis = -1
    max = 50
    textY = 420
    ALPHA = 0
    
    def gameOver():
        
        crashSound.play()
        pygame.mixer.Channel(1).stop()
        
        global forwardSpeed, sideSpeed, bottomSpeed, backgroundSpeed, enemySpeed, coinSpeed, isAlive
        isAlive = False
        forwardSpeed = 0
        sideSpeed = 0
        bottomSpeed = 0
        backgroundSpeed = 0
        enemySpeed = 0
        coinSpeed = 0
    
    class GameObject:
    
        def __init__(self, x, y, scaleX, scaleY, image):
            self.X = x
            self.Y = y
            self.scaleX = scaleX
            self.scaleY = scaleY
            self.setImageTransform(image)
            self.updateColliderPosition()
            self.alive = True
        
        def updateColliderPosition(self):
            self.collider = pygame.Rect(self.X, self.Y, self.scaleX, self.scaleY)
        
        def setImageTransform(self, image):
            self.image = pygame.image.load(image)      
            self.image = pygame.transform.scale (self.image, (self.scaleX, self.scaleY))
    
    class Enemy(GameObject):    
        def setImageTransform(self, image):
            super().setImageTransform(image)
            self.image = pygame.transform.rotate (self.image, 180)
            
    
    class Coin(GameObject):     
        def setImageTransform(self, image):
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale (self.image, (self.scaleX, self.scaleY))
            
            
    
    def generateEnemy():
        return Enemy( random.randint(143, sizeX-135-75), random.randint(-700, -171), 75, 170, random.choice(carImages) )
    def generateCoin():
        return Coin( random.randint(143, sizeX-135-75), random.randint(-800, -171), 50, 50, './Images/Coin.png' )
    
    def write_text(surface, text, size, x, y,color=GREEN, alpha=255):
        font = pygame.font.Font("./Fonts/chintzy.ttf", size)
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        #pygame.draw.rect(text_surface, (170,139,0) , text_rect, 1, border_radius=1)
        surface.blit(text_surface, text_rect)
        #surface.blit(text_surface, (x//2,y//2))

        
    def GameOverScreen():
        write_text(DISPLAYSURF, 'GAME OVER!', 72, sizeX/2, 100, RED, ALPHA)
        write_text(DISPLAYSURF, 'Your Score: ' + str(Score), 50, sizeX/2, 180, GREEN, ALPHA)
        write_text(DISPLAYSURF, 'High Score: ' + str(HighScore), 50, sizeX/2, 260, GREEN, ALPHA)
        write_text(DISPLAYSURF, 'PRESS [R] TO RESTART', 55, sizeX/2, textY, GREEN, ALPHA)

    #Enemy not repeating algorithm
    for i in range(enemyLength):
        enemies.append( generateEnemy() )
    for i in range(enemyLength):
        for j in range(enemyLength):
            while i != j and enemies[i].collider.colliderect(enemies[j].collider):
                enemies[i] = generateEnemy()
              
    for i in range(coinCount):
        coins.append( generateCoin() )
    
    pygame.mixer.Channel(0).play(music, -1)
    pygame.mixer.Channel(1).play(rideSound, -1)
    
    while True:    
        for event in pygame.event.get():

            DISPLAYSURF.blit(backgroundImage, (0, bgY))
            DISPLAYSURF.blit(backgroundImage, (0, bgY_2))
            DISPLAYSURF.blit(player, (X, Y))
            for i in range(enemyLength):
                DISPLAYSURF.blit(enemies[i].image, (enemies[i].X, enemies[i].Y))
            for i in range(coinCount):
                DISPLAYSURF.blit(coins[i].image, (coins[i].X, coins[i].Y))          
            if isAlive == False:
                DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load('./Images/crash.png'), (300, 200)), (X - 100, Y - 75))
             
            #Score text
            if isAlive:
                write_text(DISPLAYSURF, 'Score: ' + str(Score), 45, 125, 30)
                write_text(DISPLAYSURF, 'High Score: ' + str(HighScore), 45, 625, 30)
            else: GameOverScreen()
            
            if event.type == pygame.KEYDOWN:
                
                #player movement
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and Y > 0:
                    Y -= forwardSpeed
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and Y < sizeY - carScaleY:
                    Y += bottomSpeed
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and X <= sizeX - carScaleX - 140:
                    X += sideSpeed
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and X > 0 + 147:
                    X -= sideSpeed
                
                #options
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_r:       
                    pygame.quit()
                    pygame.init()
                    run()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == UPDATE:
                
                if isAlive: 
                    enemySpeed = backgroundSpeed + 1
                coinSpeed = backgroundSpeed
                
                #game hard
                if Score >= hardIndex and Score % hardIndex == 0 and triggered:
                    backgroundSpeed += 0.25
                    triggered = False 

                elif Score >= hardIndex and Score % hardIndex != 0:
                    triggered = True
                
                #text animation
                if increment < max:
                    increment += 1
                    textY += axis*1.5
                elif increment == max:
                    increment = 0
                    axis *= -1
                    
                if ALPHA <= 255 and not isAlive:
                    ALPHA += 2.5
                
                if (Score > HighScore):
                    HighScore = Score
                    file = open("./Data/info.txt", "a")
                    file.truncate(0)
                    file.write(str(HighScore))
                    file.close()
                
                #background images positions
                bgY += backgroundSpeed
                bgY_2 = bgY - sizeY
                if bgY >= sizeY:
                    bgY = 0
                
                #Enemy collision detection and Position changing
                for i in range(enemyLength):
                    enemies[i].updateColliderPosition()
                    enemies[i].Y += enemySpeed 
                    
                    #collide
                    if isAlive and pygame.Rect(X, Y, carScaleX, carScaleY).colliderect(enemies[i].collider):
                        crashSound.play()
                        pygame.mixer.Channel(1).stop()        
                        isAlive = False
                        forwardSpeed = 0
                        sideSpeed = 0
                        bottomSpeed = 0
                        backgroundSpeed = 0
                        enemySpeed = 0
                        coinSpeed = 0
                    
                    #enemie end
                    if enemies[i].Y > sizeY + 20:
                        enemy = generateEnemy()
                        enemy.updateColliderPosition()
                        for j in range(enemyLength):
                            while enemies[j].collider.colliderect(enemy.collider):
                                enemy = generateEnemy()
                        enemies[i] = enemy
                
                for i in range(coinCount):
                    coins[i].updateColliderPosition()
                    coins[i].Y += coinSpeed
                    
                    #collide
                    if pygame.Rect(X, Y, carScaleX, carScaleY).colliderect(coins[i].collider) and coins[i].alive:
                         Score += 1
                         coins[i].alive = False 
                         coins[i].image.fill((0, 0, 0, 0)) 
                         coinPicking.play() 
                    
                    for j in range(enemyLength):
                        if coins[i].collider.colliderect(enemies[j].collider):
                            coins[i].alive = False 
                            coins[i].image.fill((0, 0, 0, 0)) 
                    
                    #coin end
                    if coins[i].Y > sizeY + 20:
                        coins[i] = generateCoin()
                    
        pygame.display.update()
        clock.tick(120)
        
    
    