import pygame, random
from load_image import *
from const import *

class menu():
    
    def __init__(self):
        pass
    
    def shiftList(self, list, dir):
        if dir == 'r':
            if len(list) > 1:
                return list[1:]+[list[0]]
            else: return list
        else:
            if len(list) > 1:
                return [list[len(list)-1]]+list[:len(list)-1]
            else: return list
    
    # Input:  screen, list of items to display in menu, list of images of items
    #         text to display for menu heading
    # Output: player's selection from menu
    def invMenu(self, screen, items, images, text):
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
            msgText = font.render( text, 1, white, yellow )
            msgBox.blit(msgText, (10,10) )
        
        #draw available items in window
        w = 10 #var to draw items across screen
        availableItems = []
        hPosList = [10]
        for item in range( len(items) ):
            if items[item] > 0:
                itemBox = pygame.Surface( (blocksize, blocksize) )
                itemBox.fill( black )
                itemBox.blit( images[item], (0, 0) )
                if pygame.font:
                    font = pygame.font.SysFont("arial", 8)
                    msgText = font.render( 'x'+str(items[item]), 1, white, black )
                    itemBox.blit(msgText, (20,20) )
                msgBox.blit( itemBox, (w, 30) )
                if w not in hPosList:
                    hPosList += [w]
                availableItems += [item]
                w += blocksize
        hPos = 10 #horizontal position of selection box
        #boxPoints = ( (hPos, blocksize), (hPos, 2*blocksize), (hPos+blocksize, 2*blocksize), (hPos+blocksize, blocksize) )
        boxPointsFn = lambda x: ( (x,blocksize), (x,2*blocksize), (x+blocksize, 2*blocksize), (x+blocksize, blocksize) )
        boxPoints = boxPointsFn(hPos)
        pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
        
        borderBox.blit( msgBox, (5, 5) )
        screen.blit(borderBox, (100, 100) )        
        pygame.display.flip()
        numItems = len(availableItems)
        print hPosList
        print availableItems
        # wait for selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.draw.lines( msgBox, yellow, True, boxPoints, 1 )
                    if event.key == pygame.K_RIGHT:
                        hPosList = self.shiftList(hPosList, 'r')
                        if len(availableItems) > 1:
                            availableItems = availableItems[1:] + [availableItems[0]]
                    if event.key == pygame.K_LEFT:
                        hPosList = self.shiftList(hPosList, 'l')
                        if len(availableItems) > 1:
                            availableItems = [availableItems[len(availableItems)-1]] + availableItems[:len(availableItems)-1]
                    if event.key == pygame.K_ESCAPE:
                        return None
                    if event.key == pygame.K_RETURN:
                        if availableItems == []: return None
                        else: return availableItems[0]
            hPos = hPosList[0]
            boxPoints = boxPointsFn(hPos)
            pygame.draw.lines( msgBox, white, True, boxPoints, 1 )
            borderBox.blit( msgBox, (5, 5) )
            screen.blit(borderBox, (100, 100) ) 
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass