from time import sleep
import threading as Thread
import traceback




##thing = fileProcesser(data)
##thing.start(.03,len(thing.wordsToType))

######################GUI#######################

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder


class TestWindow(GridLayout):
    
    currentCursor = '|'
    lettersRight = []
    listOfColors = []
    colors = ['#00ff00','#ff0000']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        file = 'TypingFiles/LessonParts/Three Minute File 21.txt'
        file = open(file, 'r')
        data = file.read()
        file.close()
        self.wordsToType = data
idle        self.shownText = self.wordsToType[:50]
        self.typedText = ''
        self.onScreenText = ''
        self.lettersTyped = 0
        self.numOfLettersShownOnTheScreen = 60
        self.percentOfSpaceLeftAfterYourTyping = .5
        self.lettersOnScreen = int(self.numOfLettersShownOnTheScreen*(1-self.percentOfSpaceLeftAfterYourTyping))
        self.spacesOnScreen = self.numOfLettersShownOnTheScreen-self.lettersOnScreen
        #self.startClock()

    def makeLetterDisplayString(self):
        if self.lettersTyped > self.lettersOnScreen:
            screentext = self.wordsToType[self.lettersTyped-self.lettersOnScreen:self.lettersTyped+self.spacesOnScreen]
            return screentext + ' '*(self.numOfLettersShownOnTheScreen-len(screentext))
        else:
            return self.wordsToType[:self.numOfLettersShownOnTheScreen]+' '*(self.numOfLettersShownOnTheScreen-len(self.wordsToType[:self.numOfLettersShownOnTheScreen]))

    def makeKeyString(self):
        if len(self.onScreenText) > self.lettersOnScreen:
            self.onScreenText = self.onScreenText[1:]
            return [self.onScreenText, self.currentCursor+' '*(self.spacesOnScreen-1)]
        else:
            return [self.onScreenText, self.currentCursor+' '*(self.numOfLettersShownOnTheScreen-len(self.onScreenText)-1)]

    def formatLetters(self,letters,listOfColors):
        returnstr = ''
        for letter,color in map(lambda a,b:[a,b],letters[0],listOfColors):
            if letter == ' ':
                returnstr+=' '
            elif letter == '"':
                returnstr+='[color='+self.colors[color]+']\"[/color]'
            elif letter == '[':
                returnstr+='[color='+self.colors[color]+']&br;[/color]'
            elif letter == ']':
                returnstr+='[color='+self.colors[color]+']&bl;[/color]'
            else:
                returnstr+='[color='+self.colors[color]+']'+letter+'[/color]'
        return returnstr+letters[1]


    def keyPressed(self):
        self.lettersTyped+=1
        self.typedText += self.wordsToType[self.lettersTyped]
        self.onScreenText+= self.wordsToType[self.lettersTyped]
        self.listOfColors.append(0)
        #self.printInColor(self.makeKeyString(),self.lettersRight[self.lettersTyped-self.lettersOnScreen:self.lettersTyped+self.spacesOnScreen] if len(self.lettersRight)>self.lettersOnScreen else self.lettersRight)
        self.lettersRight.append(0 if self.typedText[-1] == self.wordsToType[self.lettersTyped-1] else 1)

    def start(self,delay,numOfTimes):
        x = 0
        while x != numOfTimes:
            x+=1
            self.keyPressed()
            sleep(delay)

    def iterateOverTwoLists(self,list1,list2):
        if len(list1)!=len(list2):
            return 'You done screwed up'
        for i in range(len(list1)):
            yield (list1[i],list2[i])

    def startClock(self):
        self.clockThread = Thread.Thread(target=self.clockLoop)
        self.clockThread.start()

    def clockLoop(self):
        while True:
            try:
                self.keyPressed()
                #sleep(.04)
                self.ids.label1.text = self.makeLetterDisplayString()
                self.ids.label2.text = self.formatLetters(self.makeKeyString(),self.listOfColors)
            except:
                break

class BuildTestWindow(App):
    def build(self):
        Builder.load_string("""
<TestWindow>:
    rows: 20
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        id: label1
        text: 'This is label 1 \\"Hello\\''
    Label:
        id: label2
        markup: True
        text: 'This is label 2'
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''
    Label:
        text: ''""")
        self.myWindow = TestWindow()
        return self.myWindow

try:
    x = BuildTestWindow()
    x.run()
except Exception as e:
    emailThatShouldntBeSent = '''
From: elpythongames@gmail.com
To: elpythongames@gmail.com
Subject: Unfortunately something went wrong

{0}

'''.format(traceback.format_exc())
    
    print(emailThatShouldntBeSent)
    
    
    input()
