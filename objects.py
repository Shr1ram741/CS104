import pygame
import random

class bird(pygame.sprite.Sprite):
    def __init__(self,pos,bird_type,SCREEN_DIM,sling=1,size=(50,50)):
        super().__init__()
        self.type = bird_type
        self.size = size
        self.bird_types = ["red","chuck","blue","bomb"]
        for x in self.bird_types:
            if x==self.type:
                if sling==1:
                    self.image = pygame.transform.scale(pygame.image.load(f"./images/{x}.png").convert_alpha(),size)
                elif sling==2:
                    self.image = pygame.transform.scale(pygame.image.load(f"./images/{x}2.png").convert_alpha(),size)
        
        self.SCREEN_DIM = SCREEN_DIM

        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.GRAVITY = 0.5
        self.ground_y = self.SCREEN_DIM[1]*0.78
        self.dragging = False
        self.launched = False
        self.e = 0.6
    
    def update(self):
        if self.launched and not self.dragging:
            if (self.velocity.magnitude() < 0.5) and self.rect.y > (self.ground_y-5) and self.rect.y < self.ground_y:
                self.velocity.x=0
                self.velocity.y=0
            else:
                self.velocity.y+=self.GRAVITY
                self.rect.x+=self.velocity.x
                self.rect.y+=self.velocity.y

            if self.rect.collidepoint((self.rect.center[0],self.ground_y)):
                self.velocity.y = -(self.velocity.y*self.e)
                self.velocity.x = self.velocity.x*0.5
    
    def calculate_damage(self, block):
        if self.type == "red":
            return int(1.6*self.velocity.magnitude())
        elif self.type == "chuck":
            if block.type == "wood":
                return int(2.4*self.velocity.magnitude())
            return int(0.8*self.velocity.magnitude())
        elif self.type == "blue":
            if block.type == "ice":
                return int(2.4*self.velocity.magnitude())
            return int(0.8*self.velocity.magnitude())
        elif self.type == "bomb":
            if block.type == "stone":
                return int(2.4*self.velocity.magnitude())
            return int(0.8*self.velocity.magnitude())
        
    def predict_trajectory(self,sling_pos):
        points=[]
        sling_pos = pygame.math.Vector2(sling_pos)
        launch_vector = pygame.math.Vector2(sling_pos - self.rect.center)
        temp_pos = pygame.math.Vector2(self.rect.center)
        temp_velocity = launch_vector*0.5

        for i in range(30):
            temp_velocity.y += self.GRAVITY
            temp_pos += temp_velocity
            points.append((int(temp_pos.x),int(temp_pos.y)))
        return points

class brick(pygame.sprite.Sprite):
    def __init__(self,brick_type,pos=[50,422],size=(50,50),SCREEN_DIM=(1200,600),ground_y=468):
        super().__init__()
        self.type = brick_type
        self.health = 100
        self.size = size
        self.pos = [pos[0],ground_y-self.size[1]]

        if self.type == "ice":
            self.image = pygame.transform.scale(pygame.image.load("./images/ice.png").convert_alpha(),size)
            self.image.set_colorkey((255,255,255))
        elif self.type == "wood":
            self.image = pygame.transform.scale(pygame.image.load("./images/wood1.png").convert_alpha(),size)
            self.image.set_colorkey((0,0,0))
        elif self.type == "stone":
            self.image = pygame.transform.scale(pygame.image.load("./images/stone.png").convert_alpha(),size)
            self.image.set_colorkey((255,255,255))

        self.SCREEN_DIM = SCREEN_DIM
        self.rect = self.image.get_rect(center=self.pos)
    
    def take_damage(self, damage):
        self.health -= damage
        
    def update(self):
        if self.health <= 0:
            self.kill()