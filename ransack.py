import pygame, game, random
from const import *
from load_image import *

# Set the height and width of the screen
screenSize=[600,600]
screen=pygame.display.set_mode(screenSize)

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

if not pygame.font: print 'Warning, fonts disabled'

pygame.display.set_caption("Ransack")

pygame.init()
clock = pygame.time.Clock()
random.seed()

def main():    
    titleScreen = pygame.Surface(screenSize)
    titleScreen.fill(black)
    titleImg, titleRect = load_image('titlescreen.bmp', -1)
    titleScreen.blit(titleImg, (50,50) )
    
    screen.blit(titleScreen, (0,0))
    while True:
        screen.blit(titleScreen, (0,0))
        clock.tick(20)
    
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    os.sys.exit()
                if event.key == pygame.K_SPACE:
                    newGame = game.game(screen, clock)
                    newGame.mainLoop(mapList)
        pygame.display.flip()
    
main()