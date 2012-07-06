import pygame
from load_image import *
from const import *
import random

class menu():
    
    def __init__(self):
        pass
    
    def openSpellMenu(self, screen):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 60) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 50 ) )
            msgBox.fill( yellow )
            borderBox.blit(msgBox, (5, 5) )
            screen.blit(borderBox, (188-i, 200) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 60 ) )
        borderBox.fill( grey )
        if pygame.font:
            font = pygame.font.SysFont("arial", 18)
            msgText = font.render( "Spell menu:", 1, white, yellow )
            msgBox.blit(msgText, (10,10) )
        borderBox.blit( msgBox, (5, 5) )
        screen.blit(borderBox, (100, 200) )
        pygame.display.flip()
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
        
    def invMenu(self, screen, items, images):
        for i in range(88):
            borderBox = pygame.Surface( ( ((i*2)+5 ), 120) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, 110 ) )
            msgBox.fill( yellow )
            borderBox.blit(msgBox, (5, 5) )
            screen.blit(borderBox, (188-i, 100) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 120 ) )
        borderBox.fill( grey )
                
        if pygame.font:
            font = pygame.font.SysFont("arial", 18)
            msgText = font.render( "Inventory:", 1, white, yellow )
            msgBox.blit(msgText, (10,10) )
        
        #draw available items in window
        w = 10 #var to draw items across screen
        #hPosList = []
        for item in items:
            if item == 'hp':
                itemBox = pygame.Surface( (blocksize, blocksize) )
                itemBox.fill( black )
                itemBox.blit( images[6], (0, 0) )
                
            msgBox.blit( itemBox, (w, 30) )
            w += blocksize
            #hPosList += [w]
        hPos = 10 #horizontal position of selection box
        hPosList = [10, 40, 70]
        boxPoints = ( (hPos, blocksize), (hPos, 2*blocksize), (hPos+blocksize, 2*blocksize), (hPos+blocksize, blocksize) )
        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
        
        borderBox.blit( msgBox, (5, 5) )
        screen.blit(borderBox, (100, 100) )        
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        pygame.draw.lines( msgBox, yellow, True, boxPoints, 1 )
                        hPosList = hPosList[1:]+[hPosList[0]]
                        hPos = hPosList[0]
                        boxPoints = ( (hPos, blocksize), (hPos, 2*blocksize), (hPos+blocksize, 2*blocksize), (hPos+blocksize, blocksize) )
                        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
                    if event.key == pygame.K_LEFT:
                        pygame.draw.lines( msgBox, yellow, True, boxPoints, 1 )
                        hPosList = [hPosList[2]]+hPosList[:2]
                        hPos = hPosList[0]
                        boxPoints = ( (hPos, blocksize), (hPos, 2*blocksize), (hPos+blocksize, 2*blocksize), (hPos+blocksize, blocksize) )
                        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
                    if event.key == pygame.K_ESCAPE:
                        return
            borderBox.blit( msgBox, (5, 5) )
            screen.blit(borderBox, (100, 100) ) 
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass