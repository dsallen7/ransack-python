import pygame, os

try:
    import android
except ImportError as e:
    print "No android in sfx",e
    android = False

class sfx():
    
    def __init__(self, mixer):
        # 0 : 
        # 1 : 
        # 2 : 
        self.mixer = mixer
        soundFiles= ['camera.wav','sword1.wav','miss.wav','dialog.wav','select1.wav','select2.wav']
        self.sounds = range(len(soundFiles))
        for i in range(len(soundFiles)):
            pass
            #self.sounds[i] = self.load( soundFiles[i] )

    def load(self, filename):
        if android:
            fileobj = android.assets.open(os.path.join('SND', filename ) )
            return self.mixer.Sound( fileobj )
        else: return self.mixer.Sound( os.path.join('../assets/SND', filename ) )
    
    def play(self, n):
        pass
        #self.sounds[n].play()