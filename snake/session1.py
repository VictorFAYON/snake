import pygame
import argparse
import random as rd

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

    position= initial_snake(lenth,width)
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

def quadrillage(s,w,l):#affiche une case sur deux noire
    color = (0, 0, 0) # black
    width=20
    height=20
#On va remplir à chaque ligen soit les cases paires soit les cases impaires
    for top in range(w):
        for left in [_ for _ in range(l)][::2]:
            rect = pygame.Rect((left+top%2)*20, top*20, width, height) 
            pygame.draw.rect(s, color, rect)
def printsnake(s,position):#affiche le serpent en fonction de sa position
    color = (9, 82, 40) # vert sapin
    width=20
    height=20
#On va remplir les position qui sont des tuples
    for pos in position:
            rect = pygame.Rect(pos[0]*20, pos[1]*20, width, height) 
            pygame.draw.rect(s, color, rect)
def initial_snake(lenth,width):#créé la position initiale aléatoire du serpent
    x=rd.randint(4,width-1)
    y=rd.randint(1,lenth-1)
    position=[(x,y),(x-1,y),(x-2,y)]
    return position

def rand_apple(position, l, w):#créé une position de pomme aléatoire
    x=rd.randint(1,w-1)
    y=rd.randint(1,l-1)
    while (x,y) in position:
        x=rd.randint(1,w-1)
        y=rd.randint(1,l-1)
    return (x,y)

def print_apple(apple,s):#affiche la pomme
    color = (228,124,110) # rouge clair
    width=20
    height=20
    rect = pygame.Rect(apple[0]*20, apple[1]*20, width, height) 
    pygame.draw.rect(s, color, rect)

