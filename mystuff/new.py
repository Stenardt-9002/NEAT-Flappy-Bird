import pygame
import neat 
import os 
import random 
import time 
pygame.font.init()


win_WIDTH = 500
win_HEIGHT = 800



BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))) ,pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

STAT_FOINT = pygame.font.SysFont("comicsans",50)



class Bird:
    IMGS = BIRD_IMGS
    mAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5 #time of on screen

    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.tilt = 0 
        self.tick_count1 = 0
        self.vel = 0 
        self.height = self.y 
        self.img_count = 0 
        self.img = self.IMGS[0]
        pass 
    def jump(self):
        self.vel = -10.5
        self.tick_count1 = 0 #last save 
        self.height = self.y #where started

    def move(self):
        self.tick_count1+=1
        d = self.vel*self.tick_count1 + (1.5*self.tick_count1**2) #(ut+(1/2at^2))

        # bkup restriction for d
        if d>=16:
            d = 16

        if d<0 :
            d -=2 
            
        self.y = self.y+d #go up or go down

        if d<0 or self.y < self.height +50:#still upwards
            if self.tilt<self.mAX_ROTATION:
                self.tilt = self.mAX_ROTATION
                pass 
        #tilt upwards
        else:
            if self.tilt>-90:
                self.tilt -= self.ROT_VEL #go up tilt
                pass
    
    def draw(self,win):
        self.img_count+=1 #no of loops
        # which image to blit
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count<self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]

        elif self.img_count<self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        
        elif self.img_count<self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]

        elif self.img_count==self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # elif self.img_count==self.ANIMATION_TIME*3:
        #     self.img = self.IMGS[2]
        
        #dont flap when its going down
        if self.tilt<=-80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2 #dont skip its raotion
        
        #rotate it about centre
        rotated_image = pygame.transform.rotate(self.img,self.tilt)

        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)

        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):#collision
        return pygame.mask.from_surface(self.img) #2d list


class Pipe(object):
    GAP = 200 #space bw pipes
    VEL = 5 
    def __init__(self,x):
        self.x = x 
        self.height = 0 
        # self.gap = 100 
        #top of pipe
        self.top = 0 
        #bottom of pip
        self.bottom = 0 
        # two pipes
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False

        self.set_height()

    def set_height(self) :
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP 


    def move(self):
        self.x -= self.VEL
        #moving pipe towards left
        pass 

    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
        pass 


    

    def collide(self,birdobj):
        bird_mask = birdobj.get_mask()
        top_mask_pipe = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask_pipe = pygame.mask.from_surface(self.PIPE_BOTTOM)
        #pygame is gonna check pixel collision

        top_offset = (self.x - birdobj.x,self.top - round(birdobj.y))
        bottom_offset = (self.x - birdobj.x,self.bottom-round(birdobj.y))


        #collsion of mast (find pt of collsion)
        b_point = bird_mask.overlap(bottom_mask_pipe,bottom_offset)
        #top collision 
        t_point = bird_mask.overlap(top_mask_pipe,top_offset)
        pass 


        if t_point or b_point:
            return True #collsion
        return False




class Base:#base ground image short keep moving
    VEL = 5 
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    # x moves to left
    def __init__(self,y):
        self.y = y 
        self.x1 = 0
        self.x2 = self.WIDTH
    # def move 

    #very frame
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH <0:
            self.x1 = self.x2 + self.WIDTH #start new images
            pass 
        if self.x2 + self.WIDTH<0:
            self.x2 = self.x1 + self.WIDTH
            pass 
        
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
        pass 

    







def draw_window(win,birdobj,pipeobj,baseobj,score):
    win.blit(BG_IMG,(0,0))
    #pipes
    # pipeobj.draw()
    texttoblit = STAT_FOINT.render("Score : "+str(score),1,(255,255,255))
    baseobj.draw(win)
    for pip in pipeobj:
        pip.draw(win)

    



    birdobj.draw(win)
    win.blit(texttoblit,(10,10))
    pygame.display.update()
    pass 

def main():
    # birdobj = Bird(200,200)
    birdobj = Bird((int)(0.23*win_WIDTH*2),(int)(0.35*win_HEIGHT *1000/800))
    baseobj = Base(0.73*win_HEIGHT*1000/800)
    pipeobj = [Pipe(750)]
    win = pygame.display.set_mode((win_WIDTH,win_HEIGHT))
    score = 0
#movement of bird 
    clock = pygame.time.Clock()#tick rate


    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # birdobj.move()  
        add_pipe = False
        removal_list_piep = []
        for pip in pipeobj:
            if pip.collide(birdobj): #collision
                print("HITHITHIHTI\n\n")
                pass 

            #pipes pass 
            if pip.x+pip.PIPE_TOP.get_width()<0:
                #pipe gone
                removal_list_piep.append(pip)
            
            if not pip.passed and pip.x < birdobj.x-100:#bird has crossed pipe continue game
                pip.passed = True 
                add_pipe = True
                pass
            pip.move()
        if add_pipe:
            #opening add pipe
            score+=1 
            pipeobj.append(Pipe(750))
        for r in removal_list_piep:
            pipeobj.remove(r)

        if birdobj.y + birdobj.img.get_height()>=730:
            #collision with god sky
            pass
        
        
        baseobj.move()
        # draw_window(win,birdobj)
        draw_window(win,birdobj,pipeobj,baseobj,score)

            
    pygame.quit()
    quit()

main()





# while True:

#     pass





