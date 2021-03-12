#Python Standard Library
import sys
import threading as thread
import time as perf
from os import listdir
import datetime
import traceback

#pynput stuff
from Modules.pynput import keyboard
from Modules.pynput.keyboard import Key as keyModule

#Kivy stuff
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock

#Stuff we made
from Logic.FindWorstFile import *
import Logic.CSVFuncs as ce

Builder.load_file(sys.path[0]+'/KivyGraphicFiles/ResultsScreenGUI.kv')
Window.borderless = False

class Chart(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    def redo(self, lesson, files):
        done = True
        if self.done:
            self.parent.parent.exit()
            files = [file[0] for file in files]
            self.parent.parent.parent.parent.nextLesson = files.index(lesson[0])
            self.parent.parent.parent.parent.MakeTypingWindow()
            self.parent.parent.parent.parent.current = 'TypingWindow'

class ResultsWindow(BoxLayout):

    pathything = sys.path[0]
    secondsofdowntime = 15
    delayforspacebar = 1
    time = 0-secondsofdowntime
    print('This is a thing')

    def __init__(self, user, files, idleTime, day, **kwargs):
        print('this thing does a thing half of the time')
        self.user = user
        self.files = files
        self.numOfLessons = day.numOfLessons
        self.doneWithAllLessons = True if len(self.files)>=day.numOfLessons else False
        self.lessonName = day.lessonName
        self.buildChart()
        print('It does not get stuck at buildChart')
        super().__init__(**kwargs)
        print('It does not get stuck at super')
        self.idleTime = idleTime
        self.runclock = True
        Clock.schedule_once(self.setupScreen)
        print('It does not get sutck at clock.schedule_once')
        self.StartKeyLogger()
        #self.changeLessonName()
        print("There is a good chance it didn't get here")
        
    def setupScreen(self,clockvar):
        print('I am trying to print something inside a function. For some reason it has decided that it does not want to work on a different function so I am trying it on a function that definately works.')
        while True:
            try:
                self.ids.idletime.text = str(self.parent.parent.idleTime)
                break
            except:
                pass
        self.children[1].children[0].done = self.doneWithAllLessons
        self.averageResults()
        self.ids.averageaccuracy.text,self.ids.averagewpm.text = str(self.averageAccuracy),str(self.averageWPM)
        self.startClock()
        self.ids.idletime.text = self.formatTime(self.idleTime)
        self.ids.timeUntilIdleTime.text = self.formatTime(self.time)
        
    def startClock(self):
        self.clockThread = thread.Thread(target=self.clockLoop)
        self.clockThread.start()

    def clockLoop(self):
        runClock = True
        self.timeCache = perf.perf_counter()
        while runClock:
            runClock = self.runclock
            perf.sleep(self.timeCache+1-perf.perf_counter())
            self.timeCache = perf.perf_counter()
            self.clockUpdate()

    def stopClock(self):
        self.runclock = False

    def clockUpdate(self):
        self.time += 1
        if self.time > 0:
            self.idleTime+=1
        self.ids.idletime.text = self.formatTime(self.idleTime)
        self.ids.timeUntilIdleTime.text = self.formatTime(self.time)
        if self.time > 0:
            self.ids.timeUntilIdleTime.color = 1,0,0,1

    def StartKeyLogger(self):
        self.listener = keyboard.Listener(on_press=self.KeyPress)
        self.listener.start()

    def StopKeyLogger(self):
        self.listener.stop()

    def KeyPress(self, key):
        if key in [keyModule.enter, keyModule.space] and self.time > (0-self.secondsofdowntime+self.delayforspacebar):
            self.nextLesson()

    def formatTime(self, sec):
        '''Formats a time in seconds to mm:ss
        Parameters: int
        Returns: str'''
        neg = False if sec >= 0 else True
        sec = abs(sec)
        minutes,seconds = str(sec//60),str(sec%60)
        minutes,seconds = minutes if len(minutes)>1 else '0'+minutes, seconds if len(seconds)>1 else '0'+seconds
        minutes,seconds = minutes if len(minutes)>1 else '00', seconds if len(seconds)>1 else '00'
        time = minutes+':'+seconds
        return '- '+time if neg else time
        
    def buildChart(self):
        print('Get Stuck')
        Builder.unload_file('chartgui.kv')
        chart = """
<Chart>:
    cols:1
"""
        for onfile in range(len(self.files)):
            chart+="""
    GridLayout:
        cols: 2

        Label:
            text: '{0}'""".format(self.files[onfile][0])
            if self.hilightBest()[onfile] == 1 and len(self.files) >= self.numOfLessons:
                chart+="""
            color: 0,1,0,1"""
            chart +="""
            font_size: root.width*root.height*0.00002

        GridLayout:
            cols: 4

            Label:
                text:'{0}'
                font_size: root.width*root.height*0.00002

            Label:
                text: ''

            Label:
                text:'{1}'
                font_size: root.width*root.height*0.00002

            GridLayout:
                cols: 3

                Label:
                    text: ''

                GridLayout:
                    rows: 3
                    Label:
                        text: ''""".format(self.files[onfile][1], self.files[onfile][2])

            if self.doneWithAllLessons:
                chart+="""    
                    Button:
                        size_hint_y: None
                        height: 30
                        text: 'redo'
                        on_press: root.redo({0},{1})""".format(str(self.files[onfile]), str(self.files))
                
            else:
                chart+="""
                    Label:
                        text: ''"""
            chart+="""
                    Label:
                        text: ''
                Label:
                    text: ''

"""
        for i in range(9-len(self.files)):
            chart+='    Label:\n'
        while True:
            try:
                kivyfile = open('KivyGraphicFiles/chartgui.kv','w')
                kivyfile.write(chart)
                kivyfile.close()
                Builder.unload_file('KivyGraphicFiles/chartgui.kv')
                Builder.load_file('KivyGraphicFiles/chartgui.kv')
                break
            except:
                print('Aye Aye, captain')
                print(traceback.format_exc())
                [0,1][2]

    def averageResults(self):
        if not self.doneWithAllLessons:
            accuracies = [int(x) for a,x,b in self.files]
            wpms = [int(x) for a,b,x in self.files]
        else:
            best4 = bestOfFiles(self.files)
            accuracies = [int(x) for a,x,b in best4]
            wpms = [int(x) for a,b,x in best4]
        self.averageAccuracy,self.averageWPM = round(sum(accuracies)/len(accuracies),0),round(sum(wpms)/len(wpms),0)

    def recordFinalResults(self):
        ce.writeToCSVFile('/'.join(sys.path[0].split('\\')[:-1])+'/UserData/'+self.user.username+'/history.csv',[{'Lesson':self.lessonName,
                                                                                                        'Accuracy':round(self.averageAccuracy,0),
                                                                                                        'WPM':round(self.averageWPM,0),
                                                                                                        'IdleTime':self.idleTime}])
                               
    
    def exit(self):
        self.StopKeyLogger()
        self.runclock = False
        self.parent.parent.idleTime = self.idleTime
        self.recordFinalResults()
        self.parent.parent.current = 'LessonSelectScreen'
        Window.fullscreen = False
        

    def games(self):
        pass       

    def nextLesson(self):
        print('If it gets here then it is getting stuck somewhere in the next 2 lines of code but somehow it still goes on')
        self.StopKeyLogger()
        self.runclock = False
        self.parent.parent.idleTime = self.idleTime
        print('It should be here but for some reason that is totally beyond me it refuses to do my print statements')
        print('Supposedly the worst file is: ',worstFile(self.files))
        self.parent.parent.nextLesson = len(self.files) if not self.doneWithAllLessons else worstFile(self.files)
        self.parent.parent.MakeTypingWindow()
        self.parent.parent.current = 'TypingWindow'

    def changeLessonName(self):
        print('beepboopbeep')
        self.ids.lessonName.text = self.lessonName
