import pygame
import argparse
import random as rd

def add(a,b):
        return [a[0]+b[0],a[1]+b[1]]

class tile:

    def __init__(self, color, x,y):
        self._color = color
        self.x=x
        self.y=y

    def drawtile(self,s,x,y):
        rect = pygame.Rect(self.x*20, self.y*20, 20, 20) 
        pygame.draw.rect(s, self._color, rect)
        
    
class checkerboard:

    def __init__(self, width,lenth,color1,color2):
        self.width=width
        self.lenth=lenth
        self._color1= color1
        self._color2= color2

    def draw(self,s):
        for top in range(self.lenth):
            for left in range(self.width):
                rect = pygame.Rect((left+top%2)*20, top*20, 20, 20) 
                if (left+top%2)%2==0:
                    tile(self._color1,top,left).drawtile(s,top,left)
                else:
                    tile(self._color2,top,left).drawtile(s,top,left)


class serpent:
    def __init__(self,position: list,direction,colorserpent):
        self.colorserpent=colorserpent
        self.position=position
        self.direction=direction
        self.stay=True
    
    def printserpent(self,s):
        for vertebre in self.position:
            tile(self.colorserpent,vertebre[0],vertebre[1]).drawtile(s,vertebre[0],vertebre[1])
    
    def eat(self,dir):
        self.position.append(self.position[-1])
        for i in range(1,len(self.position)):
            self.position[len(self.position)-i]=self.position[len(self.position)-1-i]
        self.position[0]=add(dir,self.position[0])

    def limite(self,w,l,dir):
        nexttile=add(self.position[0],dir)
        if nexttile[0] >l or nexttile[0]<0 or  nexttile[1] >w or nexttile[1]<0 or nexttile in self.position[:len(self.position)-1]:
            return True
        return False

    def avancer(self,apple,w,l,score,dir):

        if serpent.limite(self,w,l,dir):
            self.stay=False

        if add(self.position[0], dir)==apple.position:
            serpent.eat(self,dir)
            score.win()
            apple.new(self.position,w,l)
        else:   
            for i in range(1,len(self.position)):
                self.position[len(self.position)-i][0]=self.position[len(self.position)-1-i][0]
                self.position[len(self.position)-i][1]=self.position[len(self.position)-1-i][1]
            self.position[0]=add(dir,self.position[0])


class direction:
    def __init__(self,dir):
        self.dir=dir
    def print(self):
        return self.dir
    def change(self,dir):
        self.dir=dir

class apple:
    def __init__(self,color,serp,w,l):
        self.color=color
        self.position=apple.new(self,serp,w,l)

    def new(self,position,w,l):
        x=rd.randint(1,w-1)
        y=rd.randint(1,l-1)
        while (x,y) in position:
            x=rd.randint(1,w-1)
            y=rd.randint(1,l-1)
        self.position=[x,y]
        return [x,y]
    def print(self,s):
        width=20
        height=20
        rect = pygame.Rect(self.position[0]*20, self.position[1]*20, width, height) 
        pygame.draw.rect(s, self.color, rect)

class point:
    def __init__(self):
        self.pt=0
    def win(self):
        self.pt+=1
    def give(self):
        return self.pt


class snake:
    def boardsize(self):
        MIN_WIDTH = 300
        MIN_LENTH = 300

        parser = argparse.ArgumentParser(description='Set the resolution')
        parser.add_argument('-w', type=int, help="width")
        parser.add_argument('-l', type=int, help="lenth")
        parser.set_defaults(w=300)
        parser.set_defaults(l=300)
        args = parser.parse_args()

        if args.w < MIN_WIDTH:
            raise ValueError("The size (-w argument) must be greater or equal to %d." % MIN_WIDTH)
            pygame.init()
        if args.l < MIN_LENTH:
            raise ValueError("The size (-l argument) must be greater or equal to %d." % MIN_WIDTH)
            pygame.init()
        
        args.w=(args.w//20)*20
        args.l=(args.l//20)*20
        return args
    def endgame(self):
        self.stay=False

    def game(self):
        args=snake().boardsize()
        lenth=args.l//20
        width=args.l//20
        screen = pygame.display.set_mode( (args.w,args.l) )
        clock = pygame.time.Clock()
        score=point()
        pygame.display.set_caption(f"SNAKE Score:{score.pt}")

        #serpent
        initialdirection=(1,0)
        dir=direction(initialdirection)
        colorserpent=(9, 82, 40)
        initialsserpent=[[10,7],[10,6],[10,5]]
        serp=serpent(initialsserpent,dir.print(),colorserpent)

        #pomme
        colorapple=(228,124,110)
        pom=apple(colorapple,serp.position,width,lenth)

        #checkerboard
        black=(0,0,0)
        white=(255,255,255)
        check=checkerboard(width,lenth,black,white)

        #Boucle d'action en Jeu
        while serp.stay:
            check.draw(screen)
            serp.printserpent(screen)
            pom.print(screen)
            clock.tick(1)
            pygame.display.set_caption(f"SNAKE Score:{score.pt}")
            pygame.display.update()

            for event in pygame.event.get():
                #On créé la porte de sortie
                if event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        self.stay=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.stay=False
                    if event.key == pygame.K_UP:
                        dir.change((0,-1))
                    if event.key == pygame.K_DOWN:
                        dir.change((0,1))
                    if event.key == pygame.K_LEFT:
                        dir.change((-1,0))
                    if event.key == pygame.K_RIGHT:
                        dir.change((1,0))

            serp.avancer(pom,width,lenth,score,dir.dir)
            #on créé l'affichage de tous les éléments
        pygame.quit()

def snakegame():
    snake().game()







'''
def boardsize():#on créé les dimensions, l'utilisateur peut donne les dimensions, on les redimentionne si besoin 

    MIN_WIDTH = 200
    MIN_LENTH = 200

    parser = argparse.ArgumentParser(description='Set the resolution')
    parser.add_argument('-w', type=int, help="width")
    parser.add_argument('-l', type=int, help="lenth")
    parser.set_defaults(w=200)
    parser.set_defaults(l=200)
    args = parser.parse_args()

    if args.w < MIN_WIDTH:
        raise ValueError("The size (-w argument) must be greater or equal to %d." % MIN_WIDTH)
        pygame.init()
    if args.l < MIN_LENTH:
        raise ValueError("The size (-l argument) must be greater or equal to %d." % MIN_WIDTH)
        pygame.init()
    
    args.w=(args.w//20)*20
    args.l=(args.l//20)*20
    return args

def snake(): #le jeu en lui-même
    #Paramètres
    args=boardsize()
    lenth=args.l//20
    width=args.l//20
    screen = pygame.display.set_mode( (args.w,args.l) )
    clock = pygame.time.Clock()
    stay=True
    pygame.display.set_caption("SNAKE")

    position= initial_snake()
    apple = rand_apple(position, lenth, width)
    #Boucle d'action en Jeu
    while stay:

        clock.tick(1)
        for event in pygame.event.get():
            #On créé la porte de sortie
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    stay=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    stay=False
        
        #on créé l'affichage de tous les éléments
        screen.fill( (255, 255, 255) ) 
        quadrillage(screen, width,lenth)
        printsnake(screen,position)
        print_apple(apple,screen)
        pygame.display.update()
    pygame.quit()

#def quadrillage(s,w,l):#affiche une case sur deux noire
    color = (0, 0, 0) # black
    width=20
    height=20
#On va remplir à chaque ligen soit les cases paires soit les cases impaires
    for top in range(w):
        for left in [_ for _ in range(l)][::2]:
            rect = pygame.Rect((left+top%2)*20, top*20, width, height) 
            pygame.draw.rect(s, color, rect)
#def printsnake(s,position):#affiche le serpent en fonction de sa position
    color = (9, 82, 40) # vert sapin
    width=20
    height=20
#On va remplir les position qui sont des tuples
    for pos in position:
            rect = pygame.Rect(pos[1]*20, pos[0]*20, width, height) 
            pygame.draw.rect(s, color, rect)
#def random_snake(lenth,width):#créé la position initiale aléatoire du serpent
    x=rd.randint(4,width-1)
    y=rd.randint(1,lenth-1)
    position=[(x,y),(x-1,y),(x-2,y)]
    return position

#def initial_snake():
    return [(10,5),(10,6),(10,7)]

#def rand_apple(position, l, w):#créé une position de pomme aléatoire
    x=rd.randint(1,w-1)
    y=rd.randint(1,l-1)
    while (x,y) in position:
        x=rd.randint(1,w-1)
        y=rd.randint(1,l-1)
    return (x,y)

#def print_apple(apple,s):#affiche la pomme
    color = (228,124,110) # rouge clair
    width=20
    height=20
    rect = pygame.Rect(apple[1]*20, apple[0]*20, width, height) 
    pygame.draw.rect(s, color, rect)

#def snakeclass():

    args=boardsize()
    lenth=args.l//20
    width=args.l//20
    screen = pygame.display.set_mode( (args.w,args.l) )
    clock = pygame.time.Clock()
    stay=True
    color1=(0,0,0)
    color2=(255,255,255)
    pygame.display.set_caption("SNAKE")

    position= initial_snake()
    apple = rand_apple(position, lenth, width)
    #Boucle d'action en Jeu
    while stay:

        clock.tick(1)
        for event in pygame.event.get():
            #On créé la porte de sortie
            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    stay=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    stay=False
        
        #on créé l'affichage de tous les éléments
#        printsnake(screen,position)
#        print_apple(apple,screen)
        checkerboard(width,lenth,color1,color2).draw(screen)
        pygame.display.update()
    pygame.quit()
'''
