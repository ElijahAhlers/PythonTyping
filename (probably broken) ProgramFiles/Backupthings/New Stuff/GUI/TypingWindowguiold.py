#Python Standard Library
import threading as thread
import time as perf
from datetime import date
from time import sleep
import sys

#Pynput stuff
from Modules.pynput import keyboard
from Modules.pynput.keyboard import Key as keyModule

#Kivy stuff
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.core.image import Image
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar

#Stuff we made
from Logic.CSVFuncs import *

class TypingWindow(GridLayout):

#Define constant variables for this class and all it's instances

    Builder.load_file('KivyGraphicFiles/TypingWindow.kv')
    listOfLetters = 'abcdefghijklmnopqrstuvwxyz'
    listOfNumbersAndSymbols = "1234567890-=,./;'`[]\\*-+"
    listOfCorrespondingSymbols = '!@#$%^&*()_+<>?:"~{}|'
    colors = ['#00ff00','#ff0000']
    cursor = '_'
    currentCursor = cursor

###################################################################################################################################

#Define the initiation of the window.  Only creates variables.
    
    def __init__(self, day, lesson, user, lastTimeInfo=False,**kwargs):
        '''Will make a running lesson instence.  Doesn't start the lesson
        window until told to start.
        Parameters: str, bool, bool, int(seconds), int, int, int(seconds), str, str,
        str, list[int(accuracy(between -1 and 101)),int(wpm),int(idle time(seconds))]
        Returns: class instance of RunningLesson'''
        super().__init__(**kwargs)
        self.day = day
        self.lesson = lesson
        self.wordsToType = lesson.text
        self.bSpace = lesson.backspace
        self.forced100 = lesson.forced100
        self.totalTime = lesson.time
        self.time = lesson.time
        self.percentComplete = 0
        self.fileIdleTime = 0
        self.filename = lesson.filename
        self.user = user
        self.didLessonAlready = lastTimeInfo if not lastTimeInfo else True
        self.previousTimeStats = lastTimeInfo
        self.secondsOfIdleTimeAllowed = 5
        self.accuracy = 100
        self.rawWPM = 0
        self.realWPM = 0
        self.shownText = self.wordsToType[:50]
        self.typedText = ''
        self.onScreenText = ''
        self.lettersTyped = 0
        self.idleTimeCache = perf.perf_counter()
        self.runclock = True
        self.timeRanOut = False
        self.timeCache = perf.perf_counter()
        self.returnKeyPresses = False
        self.shiftDownl = False
        self.shiftDownr = False
        self.capsLockOn = False
        self.lettersRight = []
        self.numOfLettersShownOnTheScreen = 60
        self.percentOfSpaceLeftAfterYourTyping = .5
        self.lettersOnScreen = int(self.numOfLettersShownOnTheScreen*(1-self.percentOfSpaceLeftAfterYourTyping))
        self.spacesOnScreen = self.numOfLettersShownOnTheScreen-self.lettersOnScreen
        self.makeWindow()
        Window.fullscreen = 'auto'
        
###################################################################################################################################
###################################################################################################################################
#Window layout stuff
     
    def changevar(self,var,attr,value):
        '''Changes your variable's attribute to your value
        Parameters: str, str, any
        Returns: None'''
        exec('self.ids.'+str(var)+'.'+str(attr)+' = "'+str(value)+'"')
        
    def exit(self):
        self.recordResults()
        self.parent.parent.results.append([self.filename,str(self.accuracy),str(self.realWPM)])
        self.parent.parent.idleTime+=self.fileIdleTime
        print('beep')
        self.parent.parent.GoToResults()
        print('boop')
        self.parent.parent.current = 'ResultsWindow'
        print('beepboop')
        
###################################################################################################################################
###################################################################################################################################
#Logic stuff
###################################################################################################################################

#Define the running of the window.  Will make the window.
        
    def makeWindow(self):
        self.prepScreen()
        self.startClock()
        self.StartKeyLogger()
        self.returnKeyPresses = True
        Window.fullscreen = 'auto'
        

#####################################################################################################################

#Define functions for keylogger
        
    def StartKeyLogger(self):
        self.listener = keyboard.Listener(on_press=self.KeyPress, on_release=self.KeyRelease)
        self.listener.start()

    def StopKeyLogger(self):
        self.listener.stop()

    def KeyPress(self, key):
        if self.returnKeyPresses:
            self.IdentifyKey(key,False)
            self.idleTimeCache = perf.perf_counter()

    def KeyRelease(self, key):
        if key == keyModule.shift:
            self.shiftDownl = False
        elif key == keyModule.shift_r:
            self.shiftDownr = False
            
#####################################################################################################################

    def prepScreen(self):
        self.ids.firstname.text = self.user.firstName
        self.ids.lastname.text = self.user.lastName
        self.ids.lessonNum.text = 'Lesson '+str(self.lesson.part)
        self.ids.filename.text = self.filename
        self.ids.givenText.text = self.makeLetterDisplayString()
        self.ids.typedText.text = ''
        self.ids.accuracy.text = '0'
        self.ids.rawwpm.text = '0'
        self.ids.realwpm.text = '0'
        self.ids.time.text = self.formatTime(self.time)
        self.ids.idletime.text = '00:00'
        self.ids.percentcomplete.text = self.addZeroesToPercent(0)
        self.ids.bsonoff.text = 'Backspace is ' + ('on' if self.bSpace else 'off')
        self.ids.forced100.text = 'Forced Accuracy is ' + ('on' if self.forced100 else 'off')

#####################################################################################################################

#Define functions to identify keys

    def IdentifyKey(self, key, down):
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

#####################################################################################################################

#Define functions to display your key presses on the screen

    def makeKeyString(self):
        if len(self.onScreenText) > self.lettersOnScreen:
            self.onScreenText = self.onScreenText[1:]
            return [self.onScreenText, self.currentCursor+' '*(self.spacesOnScreen-1)]
        else:
            return [self.onScreenText, self.currentCursor+' '*(self.numOfLettersShownOnTheScreen-len(self.onScreenText)-1)]


    def makeLetterDisplayString(self):
        if self.lettersTyped > self.lettersOnScreen:
            screentext = self.wordsToType[self.lettersTyped-self.lettersOnScreen:self.lettersTyped+self.spacesOnScreen]
            return screentext + ' '*(self.numOfLettersShownOnTheScreen-len(screentext))
        else:
            return self.wordsToType[:self.numOfLettersShownOnTheScreen]+' '*(self.numOfLettersShownOnTheScreen-len(self.wordsToType[:self.numOfLettersShownOnTheScreen]))

            

    def KeyPressMaster(self,key):
        self.idleTimeCache = perf.perf_counter()
        if key == 'bspace':
            if self.bSpace:
                if self.typedText:
                    self.typedText = self.typedText[:-1]
                    self.onScreenText = self.onScreenText[:-1]
                    if len(self.typedText) > len(self.onScreenText):
                        self.onScreenText = self.typedText[-len(self.onScreenText)-1] + self.onScreenText
                    self.lettersTyped-=1
                    self.lettersRight = self.lettersRight[:-1]
        elif self.forced100:
            self.lettersTyped+=1
            self.typedText+=key
            self.onScreenText+=key
            if self.typedText[-1] == self.wordsToType[self.lettersTyped-1]:
                try:
                    self.lettersRight.append(0)
                except:
                    Exit()
            else:
                self.lettersTyped-=1
                self.typedText = self.typedText[:-1]
                self.onScreenText = self.onScreenText[:-1]
            
                
        else:
            self.lettersTyped+=1
            self.typedText+=key
            self.onScreenText+=key
            try:
                self.lettersRight.append(0 if self.typedText[-1] == self.wordsToType[self.lettersTyped-1] else 1)
            except:
                self.Exit()
        print(self.makeLetterDisplayString())
        self.changevar('typedText','text',self.formatLetters(self.makeKeyString(),self.lettersRight[self.lettersTyped-self.lettersOnScreen:self.lettersTyped+self.spacesOnScreen] if len(self.lettersRight)>self.lettersOnScreen else self.lettersRight))
        self.changevar('givenText','text',self.makeLetterDisplayString())
        self.calculatePercent()
        self.changevar('percentcomplete','text',self.addZeroesToPercent(self.percentComplete))
        self.ids.percentprogress.value = int(self.percentComplete)
        if self.lettersTyped == len(self.wordsToType):
            self.Exit()

    def formatLetters(self,letters,listOfColors):
        returnstr = ''
        for letter,color in map(lambda a,b:[a,b],letters[0],listOfColors):
            if letter == ' ':
                returnstr+=' '
            elif letter == '|':
                returnstr+='|'
            elif letter == '"':
                returnstr+='[color='+self.colors[color]+']\"[/color]'
            elif letter == '[':
                returnstr+='[color='+self.colors[color]+']&br;[/color]'
            elif letter == ']':
                returnstr+='[color='+self.colors[color]+']&bl;[/color]'
            else:
                returnstr+='[color='+self.colors[color]+']'+letter+'[/color]'
        return returnstr+letters[1]
            

        
###################################################################################################################################

#Define functions to use in the program later

    def formatTime(self, sec):
        '''Formats a time in seconds to mm:ss
        Parameters: int
        Returns: str'''
        minutes,seconds = str(sec//60),str(sec%60)
        minutes,seconds = minutes if len(minutes)>1 else '0'+minutes, seconds if len(seconds)>1 else '0'+seconds
        minutes,seconds = minutes if len(minutes)>1 else '00', seconds if len(seconds)>1 else '00'
        return minutes+':'+seconds

    def addZeroesToPercent(self, percent):
        return 'Percent Complete: '+' '*(3-len(str(percent)))+str(percent)+'%'

    def calculateRealWPM(self):
        self.realWPM = int(((self.lettersRight.count(0)/5)/(self.totalTime-self.time))*60)

    def calculateAccuracy(self):
        self.accuracy = int(self.lettersRight.count(0)/len(self.lettersRight)*100) if len(self.lettersRight) else 0

    def calculateRawWPM(self):
        self.rawWPM = int(len(self.lettersRight)/5/(self.totalTime-self.time)*60)

    def calculatePercent(self):
        self.percentComplete = int(self.lettersTyped/len(self.wordsToType)*100)

###################################################################################################################################

#Define functions for the clock loop

    def startClock(self):
        self.clockThread = thread.Thread(target=self.clockLoop)
        self.clockThread.start()

    def clockLoop(self):
        runclock = self.runclock
        while runclock:
            perf.sleep(self.timeCache+1-perf.perf_counter())
            self.timeCache = perf.perf_counter()
            self.clockUpdate()
            if self.timeCache-self.idleTimeCache > self.secondsOfIdleTimeAllowed:
                self.fileIdleTime+=1
                self.ids.idletime.color = 1,0,0,1
            if not self.time:
                self.runclock = False
                self.timeRanOut = True
                self.Exit()
            runclock = self.runclock

    def stopClock(self):
        self.runclock = False

    def clockUpdate(self):
        self.time -= 1
        self.calculateAccuracy()
        self.calculateRealWPM()
        self.calculateRawWPM()
        if self.accuracy >= 80:
            self.ids.accuracy.color = 0,1,1,1
        elif self.accuracy >= 50:
            self.ids.accuracy.color = 1,.5,.5,1
        else:
            self.ids.accuracy.color = 1,0,0,1
        self.changevar('accuracy','text',self.accuracy)
        self.changevar('rawwpm','text',self.rawWPM)
        self.changevar('realwpm','text',self.realWPM)
        self.changevar('time','text',self.formatTime(self.time))
        self.changevar('idletime','text',self.formatTime(self.fileIdleTime))
        #Blinking cursor thing that didn't work self.currentCursor = ' ' if self.currentCursor == self.cursor else self.cursor

###################################################################################################################################

#Define how to record results

    def recordResults(self):
        fileAlreadyMade = True
        file = '/'.join(sys.path[0].split('\\')[:-1])+'/UserData/'+self.user.username+'/History/'+str(date.today())+self.day.lessonName+'.csv'
        try:
            open(file,'r')
        except:
            fileAlreadyMade = False 
        if fileAlreadyMade:            
            writeToCSVFile(file,[{'Lesson':self.lesson.filename,
                                'Accuracy':self.accuracy,
                                'WPM':self.realWPM,
                                'IdleTime': self.fileIdleTime}])
        else:
            writeNewCSVFile(file,['Lesson','Accuracy','WPM','IdleTime'],
                           [{'Lesson':self.lesson.filename,
                            'Accuracy':self.accuracy,
                            'WPM':self.realWPM,
                            'IdleTime': self.fileIdleTime}])
        
###################################################################################################################################

#Define exit function

    def Exit(self):
        self.StopKeyLogger()
        self.stopClock()
        self.exit()

        
###################################################################################################################################

#Runs this when opened, but not when imported
  
if __name__ == '__main__':
    x = RunningLesson('hihellohiandstuffandthings',
                      False,True,220,'thisismyfile','debugme')
    x.makeWindow()


