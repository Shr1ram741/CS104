import pygame
import random
import sys

from objects import bird, brick
from interface import Button

pygame.init()

#Constants
SCREEN_DIM = (1200,600)
ground_y = SCREEN_DIM[1]*0.78
GRAVITY = 0.5
screen = pygame.display.set_mode(SCREEN_DIM,pygame.RESIZABLE)

#User Interface functions
def main_menu():
    menu_bg = pygame.transform.scale(pygame.image.load("./images/background2.png").convert_alpha(),SCREEN_DIM)
    pygame.display.set_caption("Main Menu - Angry Birds")
    
    while True:
        screen.blit(menu_bg,(0,0))
        MOUSE_POS = pygame.mouse.get_pos()
        MENU_FONT = pygame.font.SysFont("Cambria",100,bold=True)
        MENU_TEXT = (MENU_FONT).render("MAIN MENU",True,"blue")
        menu_rect = MENU_TEXT.get_rect(center=(600,100))

        play_img = pygame.transform.scale(pygame.image.load("./images/play.png").convert_alpha(),(50,50))
        play_button = Button((600,250),play_img,"Play","Calibri",25,(128,128,0))
        exit_img = pygame.transform.scale(pygame.image.load("./images/exit.png").convert_alpha(),(50,50))
        instructions_img = pygame.transform.scale(pygame.image.load("./images/instructions.png").convert_alpha(),(50,50))
        instructions_button = Button((600,350),instructions_img,"Instructions","Calibri",25,(128,128,0))
        exit_button = Button((600,450),exit_img,"Exit","Calibri",25,(128,128,0))

        screen.blit(MENU_TEXT,menu_rect)

        for button in [play_button,instructions_button,exit_button]:
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.clicked(MOUSE_POS):
                    game=Game()
                    game.run()
                elif instructions_button.clicked(MOUSE_POS):
                    instruct()
                elif exit_button.clicked(MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        
        pygame.display.flip()

def instruct():
    menu_bg = pygame.transform.scale(pygame.image.load("./images/background2.png").convert_alpha(),SCREEN_DIM)
    pygame.display.set_caption("Instructions")

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(menu_bg,(0,0))
        head_font = pygame.font.SysFont("Cambria",100,bold=True)
        head_text = head_font.render("Instructions",True,"blue")
        head_rect = head_text.get_rect(center=(600,50))
        
        inst_font = pygame.font.SysFont("Times New Roman",10,bold=True)
        with open("./instructions.txt","r") as file:
            for i in range(15):
                line = (file.readline().strip("\n"))
                text = inst_font.render(line,True,"red")
                rect = text.get_rect(center = (600,175+i*20))
                screen.blit(text,rect)

        screen.blit(head_text,head_rect)

        back_img = pygame.transform.scale(pygame.image.load("./images/back.png").convert_alpha(),(50,50))
        back = Button((600,530),back_img,"Back to Main Menu","Calibri",25,(0,0,255))

        back.update(screen)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type==pygame.MOUSEBUTTONDOWN:
                if back.clicked(MOUSE_POS):
                    main_menu()
        
        pygame.display.flip()

def game_over(winner: int):
    menu_bg = pygame.transform.scale(pygame.image.load("./images/background2.png").convert_alpha(),SCREEN_DIM)
    pygame.display.set_caption("Game Over")

    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(menu_bg,(0,0))
        end_font = pygame.font.SysFont("Calibri",100,bold=True)
        if winner==0:
            end_text = end_font.render("Game Drawn",True,(200,128,0))
        elif winner==1 or winner==2:
            end_text = end_font.render(f"Player {winner} wins!",True,(0,128,0))
        end_rect = end_text.get_rect(center = (600,100))

        play_again_img = pygame.transform.scale(pygame.image.load("./images/play_again.png").convert_alpha(),(50,50))
        play_again = Button((600,300),play_again_img,"Play Again","Calibri",25,(128,128,0))
        exit_img = pygame.transform.scale(pygame.image.load("./images/exit.png").convert_alpha(),(50,50))
        exit = Button((600,450),exit_img,"Exit","Calibri",25,(128,128,0))

        screen.blit(end_text,end_rect)

        for button in [play_again,exit]:
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again.clicked(MOUSE_POS):
                    game=Game()
                    game.run()
                elif exit.clicked(MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                    
        
        pygame.display.flip()

#Main Game Class
class Game:
    def __init__(self):
        self.turn = 1
        self.clock = pygame.time.Clock()
        self.SCREEN_DIM = SCREEN_DIM
        self.screen = screen
        pygame.display.set_caption("Angry Birds")
        self.background = pygame.image.load("./images/background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background,self.SCREEN_DIM)

        self.sample_block = brick("wood",SCREEN_DIM=self.SCREEN_DIM)

        #Initialising Slingshots
        self.catapult1 = pygame.image.load("./images/sling.png").convert_alpha()
        self.catapult2 = pygame.image.load("./images/sling2.png").convert_alpha()
        self.cat1_rect = self.catapult1.get_rect(topleft = (3*self.sample_block.size[0]+2*self.sample_block.pos[0],ground_y-self.catapult1.get_height()))
        self.cat2_rect = self.catapult2.get_rect(topleft = (self.SCREEN_DIM[0]-2*self.sample_block.pos[0]-3*self.sample_block.size[0]-self.catapult2.get_width(),ground_y-self.catapult2.get_height()))
        self.sling1_pos = (self.cat1_rect.centerx-10,self.cat1_rect.centery-50)
        self.sling2_pos = (self.cat2_rect.centerx,self.cat2_rect.centery-50)

        #Initialising Birds and Blocks
        self.birds1 = pygame.sprite.Group()
        self.birds2 = pygame.sprite.Group()
        self.blocks1 = pygame.sprite.Group()
        self.blocks2 = pygame.sprite.Group()

        self.generate_bird()
        self.generate_blocks()
    
    #Creating new bird
    def generate_bird(self):
        self.bird_types = ["red","chuck","blue","bomb"]
        if self.turn==1:
            self.bird1 = bird(pos=self.sling1_pos,bird_type=random.choice(self.bird_types),SCREEN_DIM=self.SCREEN_DIM)
            self.birds1.add(self.bird1)
        elif self.turn==2:
            self.bird2 = bird(pos=self.sling2_pos,bird_type=random.choice(self.bird_types),SCREEN_DIM=self.SCREEN_DIM,sling=2)
            self.birds1.add(self.bird1)

    #Setting up the fortress
    def generate_blocks(self):
            block_types = ["ice","wood","stone"]
            random.seed(64)
            for i in range(3):
                for j in range(5):
                    type = random.choice(block_types)
                    block = brick(type,SCREEN_DIM=self.SCREEN_DIM)
                    block.pos = [block.pos[0]+i*block.size[0],block.pos[1]-j*block.size[1]]
                    block.rect.topleft = block.pos
                    self.blocks1.add(block)
            
            random.seed(41)
            for i in range(3):
                for j in range(5):
                    type = random.choice(block_types)
                    block = brick(type,SCREEN_DIM=self.SCREEN_DIM)
                    block.pos = [self.SCREEN_DIM[0]-4*block.pos[0]+i*block.size[0],block.pos[1]-j*block.size[1]]
                    block.rect.topleft = block.pos
                    self.blocks2.add(block)

        
    def run(self): 
        running = True
        while running:

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    

            #Handling dragging and launching of bird
                if self.turn==1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.bird1.rect.collidepoint(event.pos) and not self.bird1.launched:
                            self.bird1.dragging=True

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.bird1.rect.collidepoint(event.pos) and self.bird1.dragging:
                            self.bird1.dragging=False
                            self.bird1.launched=True
                            self.bird1.velocity = (pygame.math.Vector2(self.sling1_pos)-pygame.math.Vector2(self.bird1.rect.center))*0.5
                
                elif self.turn==2:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.bird2.rect.collidepoint(event.pos) and not self.bird2.launched:
                                self.bird2.dragging=True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if self.bird2.rect.collidepoint(event.pos) and self.bird2.dragging:
                            self.bird2.dragging=False
                            self.bird2.launched=True
                            self.bird2.velocity = (pygame.math.Vector2(self.sling2_pos)-pygame.math.Vector2(self.bird2.rect.center))*0.5

            #Setting up game environment        
            self.screen.blit(self.background,(0,0))
            pygame.draw.line(self.screen,(0,0,0),(0,ground_y),(self.SCREEN_DIM[0],ground_y))
            
            self.screen.blit(self.catapult1,self.cat1_rect.topleft)
            self.screen.blit(self.catapult2,self.cat2_rect.topleft)

            #Trajectory predictor
            mouse_pos = pygame.mouse.get_pos()
            if self.turn==1:
                if self.bird1.dragging:
                    self.bird1.rect.center = mouse_pos
                    bird_cent=pygame.math.Vector2(self.bird1.rect.center)
                    sling_cent=pygame.math.Vector2(self.sling1_pos)
                    if bird_cent.distance_to(sling_cent)>75:
                        stretch = ((bird_cent-sling_cent).normalize())*75
                        bird_cent = sling_cent + stretch
                    self.bird1.rect.center = tuple(bird_cent)
                    points = self.bird1.predict_trajectory(self.sling1_pos)
                    for point in points:
                        pygame.draw.circle(self.screen,(255,0,0),point,2)
                    pygame.draw.line(self.screen, (0, 0, 0), self.bird1.rect.center, self.sling1_pos, 5)
            
            elif self.turn==2:
                if self.bird2.dragging:
                    self.bird2.rect.center = mouse_pos
                    bird_cent=pygame.math.Vector2(self.bird2.rect.center)
                    sling_cent=pygame.math.Vector2(self.sling2_pos)
                    if bird_cent.distance_to(sling_cent)>75:
                        stretch = ((bird_cent-sling_cent).normalize())*75
                        bird_cent = sling_cent + stretch
                    self.bird2.rect.center = tuple(bird_cent)
                    points = self.bird2.predict_trajectory(self.sling2_pos)
                    for point in points:
                        pygame.draw.circle(self.screen,(255,0,0),point,2)
                    pygame.draw.line(self.screen, (0, 0, 0), self.bird2.rect.center, self.sling2_pos, 5)

            #Bird Motion and Collisions
            if self.turn==1:
                current_bird = self.bird1
            else:
                current_bird = self.bird2

            if current_bird.launched:
                if ((current_bird.rect.right < 0 or current_bird.rect.left > self.SCREEN_DIM[0] or current_bird.rect.bottom < 0) or (current_bird.velocity.magnitude() < 0.5)):
                    current_bird.kill()
                    if self.turn==1:
                        self.turn=2
                    else:
                        self.turn=1
                    self.generate_bird()
            
            if self.turn==1:
                collided_blocks = pygame.sprite.spritecollide(current_bird,self.blocks2,dokill=False)
                for block in collided_blocks:
                    block.take_damage(current_bird.calculate_damage(block))
                if len(collided_blocks)!=0:
                    current_bird.kill()
                    if self.turn==1:
                        self.turn=2
                    else:
                        self.turn=1
                    self.generate_bird()

            else:
                collided_blocks = pygame.sprite.spritecollide(current_bird,self.blocks1,dokill=False)
                for block in collided_blocks:
                    block.take_damage(current_bird.calculate_damage(block))
                if len(collided_blocks)!=0:
                    current_bird.kill()
                    if self.turn==1:
                        self.turn=2
                    else:
                        self.turn=1
                    self.generate_bird()


            #Checking for end
            if self.turn==1:
                if not self.blocks1 and self.blocks2:
                    pygame.time.delay(1000)
                    game_over(2)
                elif not self.blocks2 and self.blocks1:
                    pygame.time.delay(1000)
                    game_over(1)
                elif not self.blocks1 and not self.blocks2:
                    pygame.time.delay(1000)
                    game_over(0)      

            #Frame by frame update of objects
            current_bird.update()
            for block in self.blocks1:
                block.update()
            for block in self.blocks2:
                block.update()

            self.screen.blit(current_bird.image,current_bird.rect)
            self.blocks1.draw(self.screen)
            self.blocks2.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

main_menu()