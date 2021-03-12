from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from random import random,randint,choice

def randomBorderCoord():
    '''Makes a random coordinate on the border
        of the screen. screen coords are (0,0) to (1,1)'''
    
    #Decide if it should choose bottom/top or left/right
    if randint(0,1):

        #Bottom or top
        #       0 or 1 # 0 thru 1
        return random(),randint(0,1)
    
    else:

        #Left or right
        #       0 thru 1   # 0 or 1
        return randint(0,1),random()


Builder.load_file('ZergRush.kv')

class ZergRushLayout(BoxLayout):

    words = open('allwords.txt','r').read().split(' ')

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.sinceLastSpawn = 1
        self.spawnFrequency = 2
        self.allSpawns = []
        self.timeToCenter = 20

        self.start()
        

    def start(self):
        self.ids.endButton.text = 'Die Now'
        self.ids.endButton.on_release = self.death
        self.ids.beginInstructions.text = ''
        self.changeButtonDisabledPropertyForDifficultyButtons(True)
        Clock.schedule_interval(self.update, .5)
        
    def update(self,dt):
        self.sinceLastSpawn += 1
        if self.sinceLastSpawn == self.spawnFrequency:
            self.sinceLastSpawn = 0
            self.spawnNew()
        pass

    def spawnNew(self):
        word = choice(self.words)
        x,y = randomBorderCoord()
        label = Label(text=word,size_hint=[.2,.2],pos_hint={'x':x-.1,'y':y-.1})
        self.ids.gameScreen.add_widget(label)
        movement = Animation(
            pos_hint={'x':.4,'y':.4},
            duration=self.timeToCenter)
        movement.bind(on_complete=self.spawnReachedCenter)
        movement.start(label)
        self.allSpawns+=[label]

    def spawnReachedCenter(self,var1,var2):
        print(var1,var2)

    def chgDif(self, newDifficulty):
        print('new: {0} | old: doesn\'t matter'.format(newDifficulty))

    def changeButtonDisabledPropertyForDifficultyButtons(self, abool):
        self.ids.diff1.disabled = abool
        self.ids.diff2.disabled = abool
        self.ids.diff3.disabled = abool
        self.ids.diff4.disabled = abool
        self.ids.diff5.disabled = abool

    def death(self):
        print('you died')
        self.Exit()

    def Exit(self):
        self.get_root_window().close()

class Root(App):
    def build(self):
        return ZergRushLayout()

root = Root()
root.run()
