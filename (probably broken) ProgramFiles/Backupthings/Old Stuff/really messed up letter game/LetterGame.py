from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
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
import os

from Logic.CSVFuncs import *


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
        self.errors = 0
        self.letters = [' ']
        self.gridWidth = 11
        self.gridHeight = 11
        self.buildLetterGrid()
        self.makeAnswers()
        Clock.schedule_once(self.fillLetters)
        if self.gameStarted:
            Clock.schedule_once(self.makedathread)
        

##    def rebuild(self,width,height):
##        self.gridWidth = width
##        self.gridHeight = height
##        self.parent.remove_widget(LetterGrid)
##        self.buildLetterGrid()
##        self.makeAnswers()
##        th.Thread(target=self.fillLetters).start()
    
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
        self.answers = {}
        for i in range(self.gridWidth*self.gridHeight):
            index = 't'+str(i)
            if len(index) == 2:
                index = index[:1]+'0'+index[1:]
            print(index)
            self.answers[index]=self.letters[random.randint(0,len(self.letters)-1)]

        self.otherAnswers = self.answers

        
    def fillLetters(self,*args):
        print(self.ids)
        for letter in self.answers:
            try:
                print('self.ids.'+letter+".text")
                exec('self.ids.'+letter+".text = '"+self.answers[letter]+"'")
                exec('self.ids.'+letter+".font_size = '18sp'")
                try:
                    if letter == self.letter:
                        exec('self.ids.'+str(self.letter)+".font_size = '50sp'")

                except:
                    pass
            except:
                print('It failed')
        
    def chooseLetterToType(self):
        self.letter = random.choice(list(self.answers.keys()))
        exec("self.ids."+str(self.letter)+".color = .8,0,.1,1")
        exec('self.ids.'+str(self.letter)+".bold = True")
        exec('self.ids.'+str(self.letter)+".font_size = '50sp'")

            
    def StartKeyLogger(self):
        self.listener = keyboard.Listener(on_press=self.KeyPress, on_release=self.KeyRelease)
        self.listener.start()
##        player = th.Thread(target = self.testmode)
##        player.start()
##        

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
        
    def makedathread(self,*args):
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
            self.makeLettersDissappear()
            if len(list(self.answers.keys())) > 0:
                self.chooseLetterToType()
            if len(self.answers) == 0:
                self.done()
        else:
            self.errors+=1


    def makeLettersDissappear(self,*args):
        exec("self.ids."+str(self.letter)+".text = ''")
        exec("self.ids."+str(self.letter)+".color = 1,1,1,1")
        exec('self.ids.'+str(self.letter)+".font_size = '18sp'")
        self.answers.pop(str(self.letter))

    def done(self):
        self.parent.parent.parent.parent.youWin()
        self.parent.parent.parent.parent.clock.stopClock()

    def testmode(self):
        while len(list(self.answers.keys())) > 0:
            perf.sleep(0.05)
            self.KeyPressMaster(self.answers[self.letter])

        
class GameBoard(BoxLayout):

    Builder.load_file(os.getcwd()+'/Games/LetterGame/LetterGame.kv')

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.time = int
        self.clockStarted = False
        self.finished = False
        self.addedHomeRow = False
        self.addedEHOR = False
        self.addedITUC = False
        self.addedNWGBP = False
        self.addedMXYZQ = False
        self.addedCapitals = False
        self.addedPeriodCommaColonQuestion = False
        self.addedQuotesApostropheHyphen = False
        self.addedNumbers = False
        self.addedSpecialCharacters = False
        self.gamewidth = 10
        self.gameheight = 10
        self.timesTheTimeHasBeenUp = 0
        self.user = user
        self.fillScores()
##        self.ids.difficulty.bind(value=self.changeTimeSelection)
##        self.ids.widthSlider.bind(value=self.changeWidth)
##        self.ids.heightSlider.bind(value=self.changeHeight)

    def changeWidth(self,instance,value):
##        self.gamewidth = value
##        self.ids.setWidth.text = 'Grid Width: '+str(int(self.gamewidth))
##        self.children[1].children[0].children[1].children[0].rebuild(self.gamewidth,self.gameheight)
        pass
    def changeHeight(self,instance,value):
##        self.gameheight = value
##        self.ids.setHeight.text = 'Grid Height: '+str(int(self.gameheight))
##        self.children[1].children[0].children[1].children[0].rebuild(self.gamewidth,self.gameheight)
        pass
    def fillScores(self):
        Scores = readCSVFile(str(open('Save Location.txt').read()+'UserData/'+self.user.username+'/GamesHistory/LetterGame.csv'))
        Scores = sorted(Scores, key = lambda i: int(i['Score']),reverse=True)
        for i in range(10):
            try:
                exec('self.ids.game'+str(i)+'.text = "'+str(Scores[i]['Date'])+'"')
                exec('self.ids.time'+str(i)+'.text = "'+str(Scores[i]['Score'])+'"')
            except:
                pass
    
    def timesUp(self,outOfTime = False):
        if outOfTime:
            self.ids.winLoss.text = 'Game Over'
            self.ids.BeginButton.text = 'Start New Game'
        self.children[1].children[0].children[1].children[0].StopKeyLogger()
        self.clock.stopClock()
        self.determineScore()
        self.ids.difficulty.value = self.valueStarted
        self.finished = True
        self.ids.BeginButton.disabled = False

    def changeTimeSelection(self,instance,value):
        self.ids.timeAllowed.text = str(int(value)) +' Seconds'

    def updateTimeLeft(self):
        while self.clock.runclock:
            self.ids.difficulty.value = self.clock.ammountOfTime
            self.ids.timeAllowed.text = str(self.clock.ammountOfTime) +' Seconds' #str(self.time)[:-2]+' Seconds' if self.time > -1 else str(0)+' Seconds'
            perf.sleep(.5)
        self.timesUp(self.clock.outOfTime)

    def BeginGame(self):
        if not self.finished:
            self.valueStarted = self.ids.difficulty.value
            if not self.clockStarted:
                self.clock = MyClock(self.valueStarted)
                self.children[1].children[0].children[1].children[0].StartKeyLogger()
                self.time = self.ids.difficulty.value
                self.clock.startClock()
                self.updateThread = th.Thread(target = self.updateTimeLeft)
                self.updateThread.start()
                self.ids.hr.disabled = True
                self.ids.ehor.disabled = True
                self.ids.ituc.disabled = True
                self.ids.nwgbp.disabled = True
                self.ids.mxyzq.disabled = True
                self.ids.perComColQuest.disabled = True
                self.ids.quoteApostHyp.disabled = True
                self.ids.Cap.disabled = True
                self.ids.Num.disabled = True
                self.ids.specChar.disabled = True
                self.ids.BeginButton.disabled = True
                self.ids.difficulty.disabled = True


    def youWin(self):
        self.ids.winLoss.text = "You Win!"
        self.finished = True
        self.clock.stopClock()
        self.ids.BeginButton.text = 'Start New Game'

    def determineScore(self):
        timeused = self.valueStarted - self.clock.ammountOfTime
        timeused = 300 - timeused
        timeused = timeused*100
        timeused = timeused - (self.valueStarted*10)
        score = timeused - self.children[1].children[0].children[1].children[0].errors
        for i in range(len(self.children[1].children[0].children[1].children[0].answers)):
            score = score//1.1
        self.recordResult(score)

    def recordResult(self,result):
        try:
            writeToCSVFile(str(open('Save Location.txt').read()+'UserData/'+self.user.username+'/GamesHistory/LetterGame.csv'),[[date.strftime(date.today(), "%m/%d/%Y"),
                                                                                                                                 int(result),
                                                                                                                                 self.children[1].children[0].children[1].children[0].errors,
                                                                                                                                 len(self.children[1].children[0].children[1].children[0].answers)]])

        except Exception as error:
            print(traceback.format_exc())
        self.fillScores()
            
    def exit(self):
        Window.fullscreen = False
        self.parent.parent.current = 'select'
        
    def addHomeRow(self):
        if self.addedHomeRow:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('a','s','d','f','j','k','l',';')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
                self.ids.Cap.disabled = True
            self.addedHomeRow = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return


        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['a','s','d','f','j','k','l',';']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('a','s','d','f','j','k','l',';'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.ids.Cap.disabled = False
        self.addedHomeRow = True

    def addEHOR(self):
        if self.addedEHOR:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('e','h','o','r')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
                self.ids.Cap.disabled = True
            self.addedEHOR = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['e','h','o','r']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('e','h','o','r'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.ids.Cap.disabled = False
        self.addedEHOR = True

    def addITUC(self):
        if self.addedITUC:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('i','t','u','c')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
                self.ids.Cap.disabled = True
            self.addedITUC = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['i','t','u','c']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('i','t','u','c'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.ids.Cap.disabled = False
        self.addedITUC = True

    def addNWGBP(self):
        if self.addedNWGBP:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('n','w','g','b','p')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
                self.ids.Cap.disabled = True
            self.addedNWGBP = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['n','w','g','b','p']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('n','w','g','b','p'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.ids.Cap.disabled = False
        self.addedNWGBP = True

    def addMXYZQ(self):
        if self.addedMXYZQ:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('m','x','y','z','q')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
                self.ids.Cap.disabled = True
            self.addedMXYZQ = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['m','x','y','z','q']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('m','x','y','z','q'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.ids.Cap.disabled = False
        self.addedMXYZQ = True

    def addPeriodCommaColonQuestion(self):
        if self.addedPeriodCommaColonQuestion:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('.',',',':','?')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
            self.addedPeriodCommaColonQuestion = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['.',',',':','?']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('.',',',':','?'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.addedPeriodCommaColonQuestion = True


    #need to make ' work
    def addQuotesApostropheHyphen(self):
        if self.addedQuotesApostropheHyphen:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('"','-')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
            self.addedQuotesApostropheHyphen = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['"','-']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('"','-'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.addedQuotesApostropheHyphen = True

    #Right now yhou have to double press add capitals on the screen to add capital letters that you selected after hitting capital letters
    def addCapitals(self):
        letters = []
        if self.addedHomeRow:
            letters.extend(('A','S','D','F','J','K','L'))
        if self.addedEHOR:
            letters.extend(('E','H','O','R'))
        if self.addedITUC:
            letters.extend(('I','T','U','C'))
        if self.addedNWGBP:
            letters.extend(('N','W','G','B','P'))
        if self.addedMXYZQ:
            letters.extend(('M','X','Y','Z','Q'))
        if self.addedCapitals:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in letters]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
            self.addedCapitals = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = letters
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(letters)
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.addedCapitals = True



    def addNumbers(self):
        if self.addedNumbers:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('0','1','2','3','4','5','6','7','8','9')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
            self.addedNumbers = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['0','1','2','3','4','5','6','7','8','9']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('0','1','2','3','4','5','6','7','8','9'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.addedNumbers = True

    def addSpecialCharacters(self):
        if self.addedSpecialCharacters:
            self.children[1].children[0].children[1].children[0].letters = [i for i in self.children[1].children[0].children[1].children[0].letters if i not in ('!','@','#','$','%','^','&','*','(',')','<','>')]
            if len(self.children[1].children[0].children[1].children[0].letters) == 0:
                self.children[1].children[0].children[1].children[0].letters.append(' ')
                self.ids.BeginButton.disabled = True
            self.addedSpecialCharacters = False
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            return

        if self.children[1].children[0].children[1].children[0].letters[0] == ' ':
            self.children[1].children[0].children[1].children[0].letters = ['!','@','#','$','%','^','&','*','(',')','<','>']
        else:
            self.children[1].children[0].children[1].children[0].letters.extend(('!','@','#','$','%','^','&','*','(',')','<','>'))
        self.children[1].children[0].children[1].children[0].makeAnswers()
        self.children[1].children[0].children[1].children[0].fillLetters()
        self.ids.BeginButton.disabled = False
        self.addedSpecialCharacters = True
        


            
    def resetGameBoard(self):
        if self.finished:
            self.ids.hr.disabled = False
            self.ids.ehor.disabled = False
            self.ids.ituc.disabled = False
            self.ids.nwgbp.disabled = False
            self.ids.mxyzq.disabled = False
            self.ids.perComColQuest.disabled = False
            self.ids.quoteApostHyp.disabled = False
            self.ids.Cap.disabled = False
            self.ids.Num.disabled = False
            self.ids.specChar.disabled = False
            self.ids.difficulty.disabled = False
            self.ids.BeginButton.text = 'Begin'
            self.ids.winLoss.text = ''
            self.ids.hr.state = 'normal'
            self.ids.ehor.state = 'normal'
            self.ids.ituc.state = 'normal'
            self.ids.nwgbp.state = 'normal'
            self.ids.mxyzq.state = 'normal'
            self.ids.perComColQuest.state = 'normal'
            self.ids.quoteApostHyp.state = 'normal'
            self.ids.Cap.state = 'normal'
            self.ids.Num.state = 'normal'
            self.ids.specChar.state = 'normal'
            self.runClock = True
            self.clockStarted = False
            self.finished = False
            self.children[1].children[0].children[1].children[0].errors = 0
            self.children[1].children[0].children[1].children[0].letters = [' ']
            self.children[1].children[0].children[1].children[0].makeAnswers()
            self.children[1].children[0].children[1].children[0].fillLetters()
            self.children[1].children[0].children[1].children[0].makedathread()
            
            

class MyClock:

    def __init__(self,ammountOfTime):
        self.clockStarted = False
        self.runclock = True
        self.ammountOfTime = ammountOfTime
    
    def startClock(self):
        self.clockStarted = True
        self.clockThread = th.Thread(target=self.clockLoop)
        self.clockThread.start()

    def clockLoop(self):
        self.outOfTime = False
        runClock = True
        self.timeCache = perf.perf_counter()
        while runClock:
            runClock = self.runclock
            perf.sleep(self.timeCache+1-perf.perf_counter())
            self.timeCache = perf.perf_counter()
            self.clockUpdate()
            if not self.ammountOfTime:
                self.outOfTime = True
                self.runclock = False
        

    def stopClock(self):
        self.runclock = False
        self.clockStarted = False

    def clockUpdate(self):
        self.ammountOfTime -= 1


    def formatTime(self, sec):
        minutes,seconds = str(sec//60),str(sec%60)
        minutes,seconds = minutes if len(minutes)>1 else '0'+minutes, seconds if len(seconds)>1 else '0'+seconds
        minutes,seconds = minutes if len(minutes)>1 else '00', seconds if len(seconds)>1 else '00'
        return minutes+':'+seconds


    

class LetterGameScreen(Screen):
    def __init__(self,user,**kwargs):
        super().__init__(**kwargs)
        self.name = 'LetterGame'
        self.add_widget(GameBoard(user))

        
