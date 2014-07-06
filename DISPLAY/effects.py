import pygame

from UTIL import const, colors


class effects():
    def __init__(self, clock, screen):
        pass
        self.clock = clock
        self.screen = screen

    def fadeOut(self, size):
        fadeScreen = pygame.Surface((600 - 2 * size, 600 - 2 * size))
        fadeScreen.fill(colors.black)
        for i in range(0, 255, 5):
            fadeScreen.set_alpha(i)
            self.clock.tick(40)
            self.screen.blit(fadeScreen, (size, size))
            pygame.display.flip()

    def scrollFromCenter(self, screenOne, screenTwo):
        self.screen.blit(screenOne, (const.gameBoardOffset,
                                     const.gameBoardOffset))
        for i in range(screenTwo.get_width() / 2):
            screenOne.blit(screenTwo,
                            # source
                           ((screenOne.get_width() / 2) - i,
                            const.gameBoardOffset),
                            # dest
                           ((screenOne.get_width() / 2) - i,
                            const.gameBoardOffset, 2 * i, 300)
                           )
            #self.clock.tick(100)
            self.screen.blit(screenOne,
                (const.gameBoardOffset, const.gameBoardOffset))
            pygame.display.flip()
