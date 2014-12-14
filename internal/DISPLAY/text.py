import pygame, math

from UTIL import const, colors

from math import floor, ceil

def Text(message, font, fontsize, fgc=colors.white, bgc=colors.gold, transparent=False, width=const.maxLineWidth):
    # returns a nicely formatted text box
    fontsize = int( ceil( fontsize*const.scaleFactor ) )
    if pygame.font:
        font = pygame.font.Font(font, fontsize)
        #print len(message), width
        if len(message) < width:
            # one liner
            scrapBox = font.render( message, 1, fgc, bgc )
            #len(message)*math.ceil(0.57*fontsize) math.ceil(1.5*fontsize)
            msgText = pygame.Surface( ( scrapBox.get_width(), scrapBox.get_height() ) )
            msgText.fill(bgc)
            msgText.blit( font.render( message, 1, fgc, bgc ), (0,0) )
        else:
            # multi-line
            msgText = pygame.Surface( ( width*math.ceil(font.render( 'A', 
                                                                     1, 
                                                                     colors.white, 
                                                                     colors.gold ).get_width() / 1.5 ), 
                                        ((len(message)/width)+1)*math.ceil(font.render( 'A', 
                                                                                        1, 
                                                                                        colors.white, 
                                                                                        colors.gold ).get_height() * 1.6) 
                                        ) 
                                     )
            msgText.fill(colors.gold)
            hPos = 0
            words = message.split(' ')
            while words:
                line = ''
                while words and len(line+' '+words[0]) < width:
                    line = line + words[0] + ' '
                    words = words[1:]
                lineText = font.render( line, 1, fgc, bgc )
                msgText.blit( lineText, ((msgText.get_width()/2)-(lineText.get_width()/2), hPos) )
                hPos += math.ceil( fontsize * 1.5 )
        if transparent:
            msgText.set_colorkey(bgc)
    return msgText