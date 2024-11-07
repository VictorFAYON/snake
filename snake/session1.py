import pygame
import argparse
def boardsize():

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
def snakeboard():
    args=boardsize()
    screen = pygame.display.set_mode( (args.w,args.l) )
    clock = pygame.time.Clock()
    stay=True
    pygame.display.set_caption("SNAKE")
    while stay:

        clock.tick(1)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if event.type == pygame.QUIT:
                    stay=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    stay=False
        
        screen.fill( (255, 255, 255) ) 
        quadrillage(screen, args.w,args.l)
        pygame.display.update()
    pygame.quit()

def quadrillage(s,w,l):
    color = (0, 0, 0) # black
    width=20
    height=20
#On va remplir à chaque ligen soit les cases paires soit les cases impaires
    for top in range(w//20):
        for left in [_ for _ in range(l//20)][::2]:
            rect = pygame.Rect((left+top%2)*20, top*20, width, height) 
            pygame.draw.rect(s, color, rect)
def printsnake(s,position):
    color = (9, 82, 40) # vert sapin
    width=20
    height=20
#On va remplir les position qui sont des tuples
    for pos in position:
            rect = pygame.Rect(pos[0], pos[1], width, height) 
            pygame.draw.rect(s, color, rect)
    