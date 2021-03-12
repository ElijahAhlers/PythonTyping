from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App


from pynput.keyboard import Key as keyModule
from pynput import keyboard
from datetime import date
import threading as th
import time as perf
import random
import sys




class LetterGrid(GridLayout):
    
    listOfLetters = 'abcdefghijklmnopqrstuvwxyz'
    listOfNumbersAndSymbols = "1234567890-=,./;'`[]\\*-+"
    listOfCorrespondingSymbols = '!@#$%^&*()_+<>?:"~{}|'
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.gameStarted = True
        self.returnKeyPresses = True
        self.shiftDownl = False
        self.shiftDownr = False
        self.capsLockOn = False
        self.gridWidth = 10
        self.gridHeight = 10
##        self.StartKeyLogger()
        self.buildLetterGrid()
        self.makeAnswers()
        Clock.schedule_once(self.fillLetters)
        if self.gameStarted:
            Clock.schedule_once(self.makedathread)
        
        
    
    def buildLetterGrid(self):
        lg = """
<LetterGrid>:
    rows: {0}
""".format(self.gridHeight)
        for i in range(self.gridHeight):
            lg += """
    GridLayout:
        cols: {0}
""".format(self.gridWidth)
            for j in range(self.gridWidth):
                lg += """
        Label:
            id: t"""+str(i)+str(j)+"""
            text: ''
            bold: False
            color: 1,1,1,1"""

        Builder.load_string(lg)

    def makeAnswers(self):
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.answers = {}
        for i in range(self.gridWidth*self.gridHeight):
            index = 't'+str(i)
            if len(index) == 2:
                index = index[:1]+'0'+index[1:]   
            self.answers[index]=letters[random.randint(0,len(letters)-1)]

        self.otherAnswers = self.answers

        
    def fillLetters(self,dumbvarthatkivyhastouse):
        for letter in self.answers:
            exec('self.ids.'+letter+".text = '"+self.answers[letter]+"'")
            exec('self.ids.'+letter+".font_size = 20")
        
    def chooseLetterToType(self):
        self.letter = random.choice(list(self.answers.keys()))
        exec("self.ids."+str(self.letter)+".color = 0,.5,1,1")
        exec('self.ids.'+str(self.letter)+".bold = True")
        exec('self.ids.'+str(self.letter)+".font_size = 35")

            
    def StartKeyLogger(self):
        self.listener = keyboard.Listener(on_press=self.KeyPress, on_release=self.KeyRelease)
        self.listener.start()
        player = th.Thread(target = self.testmode)
        player.start()

    def StopKeyLogger(self):
        self.listener.stop()

    def KeyPress(self, key):
        if self.returnKeyPresses:
            self.IdentifyKey(key)           

    def KeyRelease(self, key):
        if key == keyModule.shift:
            self.shiftDownl = False
        elif key == keyModule.shift_r:
            self.shiftDownr = False
        
    def makedathread(self,kivybs):
        thr = th.Thread(target = self.chooseLetterToType)
        thr.start()


    def IdentifyKey(self, key):
        try:
            if key.char in self.listOfLetters:
                self.KeyPressMaster(key.char if (not self.shiftDownl) and (not self.shiftDownr) and (not self.capsLockOn) else key.char.upper())
            elif key.char in self.listOfNumbersAndSymbols:
                self.KeyPressMaster(key.char if (not self.shiftDownl) and (not self.shiftDownr) else self.listOfCorrespondingSymbols[self.listOfNumbersAndSymbols.index(key.char)])
        except:
            if key == keyModule.space:
                self.KeyPressMaster(' ')
            elif key == keyModule.caps_lock:
                self.capsLockOn = not self.capsLockOn
            elif key == keyModule.shift:
                self.shiftDownl = True
            elif key == keyModule.shift_r:
                self.shiftDownr = True
            elif key == keyModule.backspace:
                self.KeyPressMaster('bspace')
                
    def KeyPressMaster(self, key):
        if key == self.answers[self.letter]:
            exec("self.ids."+str(self.letter)+".text = ''")
            self.answers.pop(str(self.letter))
            if len(list(self.answers.keys())) > 0:
                self.chooseLetterToType()
        else:
            pass
        if len(self.answers) == 1:
            self.done()

    def done(self):
        self.parent.parent.parent.parent.youWin()
        self.parent.parent.parent.parent.stopClock()

    def testmode(self):
        while len(list(self.answers.keys())) > 0:
            perf.sleep(0.02)
            self.KeyPressMaster(self.answers[self.letter])

        
class GameBoard(BoxLayout):

    Builder.load_file('/'.join(sys.path[0].split('\\')[:-1])+'/ProgramFiles/Games/LetterGame/LetterGame.kv')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = int
        self.runclock = True
        self.clockStarted = False
        Window.fullscreen = 'auto'
        self.ids.difficulty.bind(value=self.changeTimeSelection)

        
    def startClock(self):
        self.clockStarted = True
        self.clockThread = th.Thread(target=self.clockLoop)
        self.clockThread.start()

    def clockLoop(self):
        outOfTime = False
        runClock = True
        self.timeCache = perf.perf_counter()
        while runClock:
            runClock = self.runclock
            perf.sleep(self.timeCache+1-perf.perf_counter())
            self.timeCache = perf.perf_counter()
            self.clockUpdate()
            if not self.time:
                outOfTime = True
                self.runclock = False
        self.timesUp(outOfTime)

    def stopClock(self):
        self.runclock = False
        self.clockStarted = False

    def clockUpdate(self):
        self.time -= 1
        self.ids.difficulty.value = self.time
        self.ids.timeAllowed.text = str(self.time)+' Seconds' #str(self.time)[:-2]+' Seconds' if self.time > -1 else str(0)+' Seconds'

    def formatTime(self, sec):
        '''Formats a time in seconds to mm:ss
        Parameters: int
        Returns: str'''
        minutes,seconds = str(sec//60),str(sec%60)
        minutes,seconds = minutes if len(minutes)>1 else '0'+minutes, seconds if len(seconds)>1 else '0'+seconds
        minutes,seconds = minutes if len(minutes)>1 else '00', seconds if len(seconds)>1 else '00'
        return minutes+':'+seconds
    
    def timesUp(self,outOfTime = False):
        if outOfTime:
            self.ids.winLoss.text = 'Game Over'
        self.children[1].children[0].children[1].children[0].StopKeyLogger()
        self.stopClock()
        self.ids.difficulty.value = self.valueStarted

    def changeTimeSelection(self,instance,value):
        self.ids.timeAllowed.text = str(value) +' Seconds'

    def BeginGame(self):
        self.valueStarted = self.ids.difficulty.value
        if not self.clockStarted:
            self.children[1].children[0].children[1].children[0].StartKeyLogger()
            self.time = self.ids.difficulty.value
            self.startClock()

    def youWin(self):
        self.ids.winLoss.text = "You Win!"
        


if __name__ == '__main__':
    
    class BuildApp(App):
        
        def build(self):
            
            gb = GameBoard()
            return gb
        
    LG = BuildApp()
    LG.run()
