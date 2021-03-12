from TypingWindow import RunningWindow
import threading as thread
import time as perf



class RunningLesson():

#Define constant variables for this class and all it's instances
    
    listofmainvars = ['accuracy','rawWPM','realWPM','time','totalIdleTime','fileIdleTime']
    listoftypingvars = ['givenText','typedText']
    listofothervars = ['filename','number']

###################################################################################################################################

#Define the initiation of the window.  Only creates variables.
    
    def __init__(self, wordsToType, backspaceAllowed, forced100, time,
                 numLessonsInTheDay, lessonTheyAreOn, totalIdleTime,
                 filename, number, user, lastTimeInfo=False):
        '''Will make a running lesson instence.  Doesn't start the lesson
        window until told to start.
        Parameters: str, bool, bool, int(seconds), int, int, int(seconds), str, str,
        str, list[int(accuracy(between -1 and 101)),int(wpm),int(idle time(seconds))]
        Returns: class instance of RunningLesson'''
        self.wordsToType = [letter for letter in wordsToType]
        self.bSpace = backspaceAllowed
        self.forced100 = forced100
        self.time = time
        self.numOfLessons = numLessonsInTheDay
        self.onLesson = lessonTheyAreOn
        self.totalIdleTime = totalIdleTime
        self.fileIdleTime = 0
        self.filename = filename
        self.number = number
        self.user = user
        self.didLessonAlready = lastTimeInfo if not lastTimeInfo else True
        self.previousTimeStats = lastTimeInfo
        self.accuracy = 100
        self.rawWPM = 0
        self.realWPM = 0
        self.runclock = True
        self.timeRanOut = False
        self.timeCache = perf.perf_counter()

###################################################################################################################################

#Define the running of the window.  Will make the window.
        
    def makeWindow(self):
        self.window = RunningWindow()
        self.startClock()
        self.window.mainloop()

       
###################################################################################################################################

#Define functions to use in the program later
            
    def formatLetterList(self, letterlist, font):
        '''Formats a list of letters into a string with your
            font choice that kivy can interpret.
            Parameters: list,str
            Returns: str'''
        return '[font='+font+']'+str(''.join(letterlist))+'[/font]'

    def formatTime(self, sec):
        '''Formats a time in seconds to mm:ss
        Parameters: int
        Returns: str'''
        minutes,seconds = str(sec//60),str(sec%60)
        minutes,seconds = minutes if len(minutes)>1 else '0'+minutes, seconds if len(seconds)>1 else '0'+seconds
        minutes,seconds = minutes if len(minutes)>1 else '00', seconds if len(seconds)>1 else '00'
        return minutes+':'+seconds

    def formatWordsToType(self, listofletters):
        '''Formats a list of letters to be left justified in
            your kivy file
            Parameters: list
            Returns: str'''
        returningstuff = listofletters[:50]
        return returningstuff if (len(returningstuff) > 49) else (''.join(returningstuff) + ' '*(50-len(returningstuff)))

###################################################################################################################################

#Define functions for the clock loop

    def startClock(self):
        self.clockThread = thread.Thread(target=self.clockLoop)
        self.clockThread.start()

    def clockLoop(self):
        while self.runclock:
            if not self.time:
                self.runclock = False
                self.timeRanOut = True
            perf.sleep(self.timeCache+1-perf.perf_counter())
            self.timeCache = perf.perf_counter()
            self.clockUpdate()

    def stopClock(self):
        self.runclock = False

    def clockUpdate(self):
        self.time -= 1
        self.window.changevar('accuracy','text',self.accuracy)
        self.window.changevar('rawWPM','text',self.rawWPM)
        self.window.changevar('realWPM','text',self.realWPM)
        self.window.changevar('time','text',self.formatTime(self.time))

    def clockUpdate2(self):
        self.time-=1

###################################################################################################################################

#Define functions to run mainloop of window
        
        
###################################################################################################################################

#Runs this when opened, but not when imported
  
if __name__ == '__main__':
    x = RunningLesson('hihellohi',True,False,20,4,2,400,'thisismyfile','1 out of imlazy','debugme')
    x.makeWindow()


