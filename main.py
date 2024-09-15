from settings import *
from player import Player
from Sprites import *


class Game:

    def run():

        def get_score(points):
            font = pygame.font.Font(join('Assets','images','Oxanium-Bold.ttf'))
            text_surf = font.render(str(points),True,(240,240,240))
            text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80 ) )
            surfaceDisplay.blit(text_surf,text_rect)
            pygame.draw.rect(surfaceDisplay,(240,240,240), text_rect.inflate((20,10)).move((0,-3)),5,10)
        
        def isLostGame():
            font = pygame.font.Font(join('Assets','images','Oxanium-Bold.ttf'))
            lost_text_surf = font.render('You died!',True,(240,240,240))
            lost_text_rect = lost_text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2) )
            surfaceDisplay.blit(lost_text_surf,lost_text_rect)

        # setup
        pygame.init()
        surfaceDisplay = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption('2D shooter game')
        clock = pygame.Clock()
        running = True
        points = 0
        isLost = False
        music = pygame.mixer.Sound(join('Assets','audio','game_music.wav'))
        music.set_volume(0.5)
        music.play()

        # Creating sprite groups
        allSprites = pygame.sprite.Group()
        collisionSprites = pygame.sprite.Group()
        meteorSprites = pygame.sprite.Group()
        laserSprites = pygame.sprite.Group()

        # stars background        
        for i in range(25):
            StarsBackground(allSprites)
        player = Player((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),(allSprites,collisionSprites),laserSprites)

        # create custom events: asteroids
        asteroidEvent = pygame.event.custom_type()
        pygame.time.set_timer(asteroidEvent,400)

        while running:
            dt = clock.tick(60) / 1000
            # event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == asteroidEvent:
                    Asteroid((randint(0,WINDOW_WIDTH),0),(allSprites,collisionSprites,meteorSprites))
            
            # update
            allSprites.update(dt)
            # check for colisions
            points, isLost = collisions(player,meteorSprites,laserSprites,allSprites,points,isLost)

            # draw
            surfaceDisplay.fill('#3a2e3f')
            allSprites.draw(surfaceDisplay)
            get_score(points)
            
            # if lost restart the game after putting game to sleep for few secs
            if isLost:
                music.stop()
                isLostGame()
                pygame.display.update()
                sleep(2)
                Game.run()

            pygame.display.update()

        pygame.quit()
        quit()

Game.run()
