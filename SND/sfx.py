import pygame, os

class sfx():
    
    def __init__(self):
        # 0 : camera
        # 1 : sword
        # 2 : miss
        self.sounds = range(3)
        self.sounds[0] = pygame.mixer.Sound(os.path.join('SND', 'camera.wav' ))
        self.sounds[1] = pygame.mixer.Sound(os.path.join('SND', 'sword1.wav' ))
        self.sounds[2] = pygame.mixer.Sound(os.path.join('SND', 'miss.wav' ))
    
    def play(self, n):
        self.sounds[n].play()