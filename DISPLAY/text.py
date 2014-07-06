import pygame
import math

from UTIL import const, colors


def Text(message, font, fontsize, fgc=colors.white, bgc=colors.gold,
        transparent=False):
    """ returns a nicely formatted text box
    """
    if pygame.font:
        font = pygame.font.Font(font, fontsize)
        if len(message) < const.maxLineWidth:
            msgText = pygame.Surface((len(message) * math.ceil(0.5 * fontsize),
                math.ceil(1.5 * fontsize)))
            msgText.fill(bgc)
            msgText.blit(font.render(message, 1, fgc, bgc), (0, 0))
        else:
            msgText = pygame.Surface((const.maxLineWidth *
                math.ceil(0.5 * fontsize), ((len(message) /
                const.maxLineWidth) + 1) * math.ceil(font.render('A', 1,
                colors.white, colors.gold).get_height() * 1.75)))
            msgText.fill(colors.gold)
            hPos = 0
            words = message.split(' ')
            while words:
                line = ''
                while words and len(
                        line + ' ' + words[0]) < const.maxLineWidth:
                    line = line + words[0] + ' '
                    words = words[1:]
                lineText = font.render(line, 1, fgc, bgc)
                msgText.blit(lineText, ((msgText.get_width() / 2)
                    - (lineText.get_width() / 2), hPos))
                hPos += math.ceil(fontsize * 1.5)
        if transparent:
            msgText.set_colorkey(bgc)
    return msgText
