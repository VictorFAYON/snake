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
    return args
def snakeboard():
    args=boardsize()
    screen = pygame.display.set_mode( (args.w,args.l) )
    clock = pygame.time.Clock()
    while True:

        clock.tick(1)
        for event in pygame.event.get():
          pass
        screen.fill( (255, 255, 255) ) 
        pygame.display.update()

    pygame.quit()