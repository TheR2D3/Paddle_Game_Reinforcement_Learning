
import pygame
import random

class my_game():
    def __init__(self):       

        # Constants for pygame
        self.WIDTH = 700
        self.HEIGHT = 500
        self.SCREEN_AREA = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        self.paddle = pygame.Rect(350, 480, 100, 10)
        self.ball = pygame.Rect(10, 250, 15, 15)        
        self.ball_direction = (4, 4)
        self.balls = 3

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.mouse.set_visible(0)
        pygame.display.set_caption("Reinforcement Learning")
        self.clock = pygame.time.Clock()    
        self.font = pygame.font.SysFont("ubuntumono", 20)

        # Pygame Variables        
        self.ball_Xpos = 0
        self.ball_Ypos = 0                
        

        # RL Variables
        self.done = False
        self.hit = 0
        self.miss = 0
        self.reward = 0
        self.episode = 0
        

    # Paddle movement
    def move_right():
        if self.paddle.left < 630:
            self.paddle.left += 40               


    def move_left():
        if self.paddle.left > 0:
            self.paddle.left += -40
            
        
    def reset(self):
        self.paddle = pygame.Rect(350, 480, 100, 10)
        self.ball_Xpos = random.randint(50,650)
        self.ball_Ypos = random.randint(30,250)
        self.ball = pygame.Rect(self.ball_Xpos, self.ball_Ypos, 15, 15)                        
        return[(self.paddle.left)*0.01,(self.ball.left)*0.01,(self.ball.top)*0.01, self.ball_direction[0],self.ball_direction[1]]

    #0 - Left
    #1 - Stay
    #2 - Right

    def step(self, action):

        self.reward = 0
        self.done = 0        

        #Take one action at a time and get appropriate rewards.
        if action == 0:                        
            if self.paddle.left > 0:
                self.paddle.left += -30 
            self.reward -= 0.5

        if action == 2:                        
            if self.paddle.left < 600:
                self.paddle.left += 30 
            self.reward -= 0.5

        self.run_frame()       
        self.state = [(self.paddle.left)*0.01,(self.ball.left)*0.01,(self.ball.top)*0.01, self.ball_direction[0],self.ball_direction[1]]        
        return self.reward, self.state, self.done

    def run_frame(self):
        
        #Ball movement and collision detection
        self.ball.move_ip(*self.ball_direction)
        
        if self.ball.right > self.WIDTH or self.ball.left < 0:
            self.ball_direction = -self.ball_direction[0], self.ball_direction[1]
        elif self.ball.top < 0 or self.ball.bottom > self.HEIGHT or self.paddle.colliderect(self.ball):
            self.ball_direction = self.ball_direction[0], -self.ball_direction[1]

            if(self.paddle.colliderect(self.ball) or self.ball.bottom > self.HEIGHT):                        
                if(self.paddle.colliderect(self.ball)):
                    self.hit = self.hit + 1
                    self.reward = self.reward + 5                                

                if(self.ball.bottom > self.HEIGHT):
                    self.miss = self.miss + 1
                    self.reward = self.reward - 5
                    self.done = True

        self.ball.clamp_ip(self.SCREEN_AREA)   

        #Prepare reward to be displayed on the screen
        self.hit_string = "Hit: " + str(self.hit)
        self.miss_string = "Miss: " + str(self.miss)
        self.text_hit = self.font.render(self.hit_string, True, (0, 128, 0))
        self.text_miss =  self.font.render(self.miss_string, True, (0, 128, 0))    
        
                
        # Redraw screen
        self.screen.fill(self.BLACK)
        pygame.draw.rect(self.screen, self.WHITE, self.paddle)
        pygame.draw.rect(self.screen, self.WHITE, self.ball)

        self.screen.blit(self.text_hit,(10, 20))
        self.screen.blit(self.text_miss,(600, 20))
        

        pygame.display.flip()
        self.clock.tick(100)
        


            
    
                

        


