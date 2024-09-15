from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,laserGroup):
        super().__init__(groups)
        self.image = pygame.image.load(join('Assets','images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.direction = pygame.Vector2()
        self.speed = 400
        self.Groups = groups
        self.canshoot = True
        self.laserCooldown = 300
        self.lastTimeShot = 0
        self.laserGroup = laserGroup

    def fire_laser(self):
        recent_keys = pygame.key.get_just_pressed()
        self.fire_cooldown()
        if recent_keys[pygame.K_SPACE] and self.canshoot:
            Laser((self.rect.midtop),(self.Groups,self.laserGroup))
            self.canshoot = False
            self.lastTimeShot = pygame.time.get_ticks()

    def collisions(self):
        #set screen boundaries
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
        

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        self.fire_laser()
        self.collisions()

    def fire_cooldown(self):
        self.canshoot = True if (pygame.time.get_ticks() - self.lastTimeShot) >= self.laserCooldown else False


class Laser(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Assets','images','laser.png'))
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 500

    def update(self,dt):
        self.rect.centery -= self.speed * dt

        # destroy laser if it reaches top
        if self.rect.bottom < 0:
            self.kill()
