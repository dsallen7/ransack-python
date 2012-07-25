import pygame, random
from load_image import *
from const import *

from IMG import images

class menu():
    
    def __init__(self, screen):
        self.images = images.mapImages
        self.screen = screen
        self.title = ''
    
    def shiftList(self, list, dir):
        if dir == 'r':
            if len(list) > 1:
                return list[1:]+[list[0]]
            else: return list
        else:
            if len(list) > 1:
                return [list[len(list)-1]]+list[:len(list)-1]
            else: return list
    
    def openWindow(self, xDim, yDim):
        for i in range(xDim/2):
            borderBox = pygame.Surface( ( ((i*2)+5 ), yDim) )
            borderBox.fill( grey )
            msgBox = pygame.Surface( (i*2, yDim-5 ) )
            msgBox.fill( yellow )
            borderBox.blit(msgBox, (5, 5) )
            self.screen.blit(borderBox, ( (self.screen.get_size()[0]/2)-i, 100) )
            pygame.display.flip()
            
        borderBox = pygame.Surface( ( 186, 120 ) )
        borderBox.fill( grey )
        return borderBox
    
    def displayChest(self, chest):
        menuBox = self.openWindow(188, 120)
        if pygame.font:
            font = pygame.font.SysFont("URW Chancery L", 18)
            msgText = font.render( 'Chest', 1, white, yellow )
            menuBox.blit(msgText, (10,10) )
        #draw available items in window
        w = 10 #var to draw items across screen
        availableItems = []
        hPosList = [10]
        for item in chest:
            (img, qty) = item
            itemBox = pygame.Surface( (blocksize, blocksize) )
            itemBox.fill( black )
            itemBox.blit( images.mapImages[img+86], (0, 0) )
            if pygame.font:
                font = pygame.font.SysFont("URW Chancery L", 8)
                msgText = font.render( 'x'+str(qty), 1, white, black )
                itemBox.blit(msgText, (20,20) )
            menuBox.blit( itemBox, (w, 30) )
            if w not in hPosList:
                hPosList += [w]
            availableItems += [img]
            w += blocksize
        hPos = 10 #horizontal position of selection box
        boxPointsFn = lambda x: ( (x,blocksize), (x,2*blocksize), (x+blocksize, 2*blocksize), (x+blocksize, blocksize) )
        boxPoints = boxPointsFn(hPos)
        pygame.draw.lines( menuBox, white, True, boxPoints, 1 )
        
        self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(188/2), 100) )        
        pygame.display.flip()
        numItems = len(availableItems)
        while (pygame.event.wait().type != pygame.KEYDOWN): pass
        return availableItems
    
    # Input:  list of items to display in menu, text to display for menu heading
    # Output: player's selection from menu
    def invMenu(self, items, text):
        menuBox = self.openWindow(188, 120)
                
        if pygame.font:
            font = pygame.font.SysFont("URW Chancery L", 18)
            msgText = font.render( text, 1, white, yellow )
            menuBox.blit(msgText, (10,10) )
        
        #draw available items in window
        w = 10 #var to draw items across screen
        availableItems = []
        hPosList = [10]
        for i in range( len(items) ):
            item = items[i]
            
            if item in availableItems:
                pass
            else:
                itemBox = pygame.Surface( (blocksize, blocksize) )
                itemBox.fill( black )
                itemBox.blit( images.mapImages[item.getImg()], (0, 0) )
                if pygame.font:
                    font = pygame.font.SysFont("URW Chancery L", 8)
                    if item.name == 'item':
                        msgText = font.render( 'x'+str(item.qty), 1, white, black )
                    else: msgText = font.render( 'x'+str(item.getLevel()), 1, white, black )
                    itemBox.blit(msgText, (20,20) )
                menuBox.blit( itemBox, (w, 30) )
                if w not in hPosList:
                    hPosList += [w]
                w += blocksize
                availableItems.append(item)
        hPos = 10 #horizontal position of selection box
        boxPointsFn = lambda x: ( (x,blocksize), (x,2*blocksize), (x+blocksize, 2*blocksize), (x+blocksize, blocksize) )
        boxPoints = boxPointsFn(hPos)
        pygame.draw.lines( menuBox, white, True, boxPoints, 1 )
        
        self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(188/2), 100) )    
        pygame.display.flip()
        numItems = len(availableItems)
        # wait for selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.draw.lines( menuBox, yellow, True, boxPoints, 1 )
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
            pygame.draw.lines( menuBox, white, True, boxPoints, 1 )
            self.screen.blit(menuBox, ( (self.screen.get_size()[0]/2)-(188/2), 100) )  
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass
        
    def storeMenu(self, items, text):
        menuBox = self.openWindow(188, 120)
                
        if pygame.font:
            font = pygame.font.SysFont("URW Chancery L", 14)
            msgText = font.render( text, 1, white, yellow )
            menuBox.blit(msgText, (10,10) )
        
        #draw available items in window
        w = 10 #var to draw items across screen
        availableItems = []
        hPosList = [10]
        for i in range( len(items) ):
            item = items[i]
            
            if item in availableItems:
                pass
            else:
                itemBox = pygame.Surface( (blocksize, blocksize) )
                itemBox.fill( black )
                itemBox.blit( images.mapImages[item.getImg()], (0, 0) )
                if pygame.font:
                    font = pygame.font.SysFont("URW Chancery L", 8)
                    if item.name == 'item':
                        msgText = font.render( 'x'+str(item.qty), 1, white, black )
                    else: msgText = font.render( 'L'+str(item.getLevel()), 1, white, black )
                    itemBox.blit(msgText, (20,20) )
                menuBox.blit( itemBox, (w, 30) )
                if w not in hPosList:
                    hPosList += [w]
                w += blocksize
                availableItems.append(item)
        hPos = 10 #horizontal position of selection box
        boxPointsFn = lambda x: ( (x,blocksize), (x,2*blocksize), (x+blocksize, 2*blocksize), (x+blocksize, blocksize) )
        boxPoints = boxPointsFn(hPos)
        pygame.draw.lines( menuBox, white, True, boxPoints, 1 )
        
        borderBox.blit( menuBox, (5, 5) )
        self.screen.blit(borderBox, (100, 100) )        
        pygame.display.flip()
        numItems = len(availableItems)
        # wait for selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.draw.lines( menuBox, yellow, True, boxPoints, 1 )
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
            pygame.draw.lines( menuBox, white, True, boxPoints, 1 )
            borderBox.blit( menuBox, (5, 5) )
            self.screen.blit(borderBox, (100, 100) ) 
            pygame.display.flip()
        #while (pygame.event.wait().type != pygame.KEYDOWN): pass