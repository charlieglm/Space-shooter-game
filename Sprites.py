from settings import *

class StarsBackground(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Assets','images','star.png'))
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),(randint(0,WINDOW_HEIGHT))))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Assets','images','meteor.png')).convert_alpha()
        self.surface = self.image
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2(uniform(-0.5,0.5),uniform(0.3,0.8))
        self.speed = randint(120,400)
        self.rotation = 0
        self.rotation_speed = randint(20,50)
    
    def update(self,dt):
        self.rect.center += self.direction * self.speed * dt
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.surface,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)

        #destroy asteroid if it reaches the bottom
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.frames = []

        for parent, subfolder, files in walk(join('Assets','images','explosion')):
            for file in files:
                self.frames.append(pygame.image.load(join(parent,file)).convert_alpha())

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        self.explosion_sound = pygame.mixer.Sound(join('Assets','audio','explosion.wav'))
        self.explosion_sound.set_volume(0.8)
        self.explosion_sound.play()

    def update(self,dt):
        self.frame_index += 30 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions(playerSprite, meteorSprites,laserSprite, allSprites,score,isLost):
    collisionSprite = pygame.sprite.spritecollide(playerSprite,meteorSprites,False,pygame.sprite.collide_mask)

    if collisionSprite:
        # lost the game
        isLost = True
        damage = pygame.mixer.Sound(join('Assets','audio','damage.ogg'))
        damage.set_volume(0.7)
        damage.play()
    
    for laser in laserSprite:
        collidedLaserSprites = pygame.sprite.spritecollide(laser,meteorSprites,True)

        if collidedLaserSprites:
            laser.kill()
            AnimatedExplosion(laser.rect.center,allSprites)
            score += 1

    return score, isLost


    
