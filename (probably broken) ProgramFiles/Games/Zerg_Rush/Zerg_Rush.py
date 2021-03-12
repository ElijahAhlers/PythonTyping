from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from random import random,randint,choice

person = ' o \n\\|/\n | \n/ \\'

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

Builder.load_file('Games/Zerg_Rush/Zerg_Rush.kv')

class Zerg_Rush_Layout(BoxLayout):

    diff1 = ObjectProperty(None)
    diff2 = ObjectProperty(None)
    diff3 = ObjectProperty(None)
    diff4 = ObjectProperty(None)
    diff5 = ObjectProperty(None)
    score = ObjectProperty(None)
    endButton = ObjectProperty(None)
    gameScreen = ObjectProperty(None)
    beginInstructions = ObjectProperty(None)
    startButton = ObjectProperty(None)
    userInput = ObjectProperty(None)
    
    words = open('Games/Zerg_Rush/allwords.txt','r').read().split(' ')
    currentDifficulty = 'Easy'
    started = False
    timeToCenter = 20
    
    difficultyLookUp = {
        'Easy':{
            'Frequency': 20,
            'Ramping'  : .05
            },
        'Medium':{
            'Frequency': 15,
            'Ramping'  : .05
            },
        'Hard':{
            'Frequency': 15,
            'Ramping'  : .10
            },
        'Very Hard':{
            'Frequency': 10,
            'Ramping'  : .10
            },
        'Good Luck':{
            'Frequency': 0,
            'Ramping'  : 0
            },
        }

    def __init__(self,manager,**kwargs):
        super().__init__(**kwargs)

        self.manager = manager
        self.chgDif(self.currentDifficulty)

        self.allSpawns = []
        self.wordSpawns = []
        self.userInput.bind(text=self.checkSpacebar)

    def checkSpacebar(self, instence, value):
        if value and value[-1] == ' ':
            if self.started:
                self.attemptWordRemoval(value[:-1])
            else:
                self.start()
            self.userInput.text = ''

    def start(self):
        self.userInput.text = ''
        self.userInput.focus = True
        self.sinceLastSpawn = 1
        self.spawnFrequency = self.difficultyLookUp[self.currentDifficulty]['Frequency']
        self.difficultyRamping = self.difficultyLookUp[self.currentDifficulty]['Ramping']
        self.started = True
        self.score.text = '0'
        self.startButton.disabled = True
        self.endButton.text = 'Die Now'
        self.endButton.on_release = self.end
        self.beginInstructions.text = ''
        self.changeButtonDisabledPropertyForDifficultyButtons(True)
        self.spawning = Clock.schedule_interval(self.update, .1)

    def end(self):
        self.manager.record_results('Zerg Rush', self.score.text, 0)
        self.started = False
        self.startButton.disabled = False
        self.endButton.text = 'Exit'
        self.endButton.on_release = self.Exit
        self.beginInstructions.text = 'You Died'
        self.chgDif(self.currentDifficulty)
        Clock.unschedule(self.spawning)
        for label in self.allSpawns:
            label.parent.remove_widget(label)
        self.allSpawns = []
        self.wordSpawns = []
        
    def update(self,dt):
        self.sinceLastSpawn += 1
        if self.sinceLastSpawn >= self.spawnFrequency:
            self.sinceLastSpawn = 0
            self.spawnFrequency-=self.difficultyRamping
            self.spawnNew()

    def spawnNew(self):
        word = choice(self.words)
        x,y = randomBorderCoord()
        label = Label(text=word,size_hint=[.2,.2],pos_hint={'x':x-.1,'y':y-.1})
        self.gameScreen.add_widget(label)
        movement = Animation(
            pos_hint={'x':.4,'y':.4},
            duration=self.timeToCenter)
        movement.bind(on_complete=self.spawnReachedCenter)
        movement.start(label)
        self.allSpawns+=[label]
        self.wordSpawns+=[word]

    def spawnReachedCenter(self,animation, label):
        if label in self.allSpawns:
            self.end()

    def attemptWordRemoval(self, word):
        if word in self.wordSpawns:
            self.ids.score.text = str(int(self.ids.score.text)+(len(word)*self.scoreMultiplier))
            index = self.wordSpawns.index(word)
            self.allSpawns[index].parent.remove_widget(self.allSpawns[index])
            self.allSpawns.pop(index)
            self.wordSpawns.pop(index)

    def chgDif(self, newDifficulty):
        self.changeButtonDisabledPropertyForDifficultyButtons(False)
        numericDiff = list(self.difficultyLookUp.keys()).index(newDifficulty)+1
        exec('self.diff{0}.disabled = True'.format(
            str(numericDiff)))
        self.currentDifficulty = newDifficulty
        self.scoreMultiplier = numericDiff

    def changeButtonDisabledPropertyForDifficultyButtons(self, abool):
        self.diff1.disabled = abool
        self.diff2.disabled = abool
        self.diff3.disabled = abool
        self.diff4.disabled = abool
        self.diff5.disabled = abool

    def Exit(self):
        if not self.started:
            self.manager.leave_me()

if __name__ == '__main__':
    class Root(App):
        def build(self):
            return Zerg_Rush_Layout()

    root = Root()
    root.run()