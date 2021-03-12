#Built into python
import threading as Thread
import smtplib
import traceback

#Get rid of kivy info text
import os
#os.environ["KIVY_NO_CONSOLELOG"] = '1'

#Wierd Module stuff that works
import sys
sys.path.append('/'.join(sys.path[0].split('\\')[:-1])+'/ProgramFiles/Modules')

#Kivy stuff
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.config import Config

#Stuff we made
from GUI.LoginWindowgui import LoginWindow as LW
from GUI.ChangePasswordgui import firstLogin as CP
from GUI.LessonSelectgui import HomeWindow as LS
from GUI.TypingWindowgui import TypingWindow as TW
from GUI.ResultsScreenGUI import ResultsWindow as RW
from GUI.GamesMenu import GamesMenu as GM
from GUI.TypingHistory import TypingHistory as TH
from Logic.Results import Results
from Games.LetterGame.LetterGame import GameBoard as LG

#Stuff we made
from Logic.UserClass import User as UserObject

#Set up kivy window
Window.borderless = True
Config.read('KivyGraphicFiles/config.ini')

#Define instances of classes for use in creating the window later
class Screen1(Screen):
    pass

class Login(LW):
    pass


#Main manager:  controls the different screens
#also holds information that needs to be shared with other programs/classes
class Manager(ScreenManager):

    #Day user is currently doing
    activeDay = None

    #What the next day will be
    nextLesson = None

    #the user that logged in (default for debugging)
    activeUser = UserObject('debugme')

    #Results being transferred to the results screen
    results = []

    #if this needs explaining, don't touch my program
    idleTime = 0

    #seriously, if you can't figure this out, go do something else
    doneWithLessons = False

    #makes the results object for storing results after the files
    resultsObject = None

    
    def AddSelectScreen(self):
        screen = Screen(name = 'LessonSelectScreen')
        screen.add_widget(LS(self.activeUser))
        self.add_widget(screen)

        
    def ChangePassword(self):
        screen = Screen(name='ChangePasswordScreen')
        screen.add_widget(CP(self.activeUser))
        self.add_widget(screen)

        
    def MakeTypingWindow(self):
        if 'TypingWindow' in [x.name for x in self.screens]:
            self.screens.pop([x.name for x in self.screens].index('TypingWindow'))
        screen = Screen(name='TypingWindow')
        screen.add_widget(TW(self.activeDay, self.activeDay.lessonlist[self.nextLesson],self.activeUser))
        self.add_widget(screen)

        
    def GoToResults(self):
        if 'ResultsWindow' in [x.name for x in self.screens]:
            self.screens.pop([x.name for x in self.screens].index('ResultsWindow'))
        screen = Screen(name='ResultsWindow')
        screen.add_widget(RW(self.activeUser, self.results, self.idleTime, self.activeDay))
        self.add_widget(screen)

    def TypingHistory(self):
        if 'TypingHistory' not in [x.name for x in self.screens]:
            screen = Screen(name='TypingHistory')
            screen.add_widget(TH(self.activeUser))
            self.add_widget(screen)
        
    def GamesMenu(self):
        if 'Games Menu' in [x.name for x in self.screens]:
            self.screens.pop([x.name for x in self.screens].index('Games Menu'))
        screen = Screen(name='Games Menu')
        screen.add_widget(GM())
        self.add_widget(screen)

    def LetterGame(self):
        if 'Letter Game' in [x.name for x in self.screens]:
            self.screens.pop([x.name for x in self.screens].index('Letter Game'))
        screen = Screen(name = 'Letter Game')
        screen.add_widget(LG())
        self.add_widget(screen)
        
    #Used to make the cheaty button of doom(if you don't understand, run the program)
    def cheatyFunc(self):
        self.AddSelectScreen()
        self.current = 'LessonSelectScreen'



#Makes the basic kivy window 
Builder.load_string('''
<Screen1>:
    name: 'LoginScreen'
    Login:
    
<Manager>:
    Screen1:

''')


#Makes an app object to put the manager object on
class LoginMaster(App):
    def build(self):
        return Manager()

#Instance of app class
app = LoginMaster()


#Tries to run the app and if anything goes wrong, it emails us the error and prints it out
try:
    app.run()
except Exception as error:
    gmailer = smtplib.SMTP_SSL('smtp.gmail.com',465)
    gmailer.login('elpythongames@gmail.com',
                  ''.join(
                      [chr((ord(letter)+9)//2) for letter in 'ÛÕß¹ÛßÝÉÓÉÑ¿¹']
                      )
                  )

    emailThatShouldntBeSent = '''
From: elpythongames@gmail.com
To: elpythongames@gmail.com
Subject: Unfortunately something went wrong

{0}

'''.format(traceback.format_exc())
    print(emailThatShouldntBeSent)
    gmailer.sendmail('elpythongames@gmail.com',
                     'elpythongames@gmail.com',
                     emailThatShouldntBeSent)
