from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.base import EventLoop
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from time import sleep
import threading as thread


###################################################################################################################################
#Typing Window

class TypingWindow(GridLayout):

    Builder.load_file('KivyGraphicFiles/TypingWindow.kv')
     
    def changevar(self,var,attr,value):
        '''Changes your variable's .text attribute to your value
        Parameters: str, str
        Returns: None'''
        exec('self.ids.'+str(var)+'.'+str(attr)+' = "'+str(value)+'"')
        
    def exit(self):
        #self.ids.rawWPM.text = 'hello'
        self.get_root_window().close()

###################################################################################################################################
#App to put window in

class TypingAppWindow(App):
    print(0.1)

    windowThingamabob = TypingWindow()
    print(0.2)
    def build(self):
        print(0.3)
        return self.windowThingamabob

    def getDaWindow(self):
        print(2.1)
        return self.windowThingamabob

###################################################################################################################################
#My class to modify window

class RunningWindow():
    '''Makes a window for typing.  Makes a blank window
        when you call it, but needs constant updating.
        Methods: update,changevar'''

    def __init__(self):
        from kivy.core.window import Window
        
        #Window.fullscreen = 'auto'
        #Window.boarderless = False
        self.masterWindow = TypingAppWindow()

    def mainloop(self):
        print(1.1)
        self.widgetThread = thread.Thread(target=self.doTheMainloop)
        print(1.2)
        self.widgetThread.start()
        print(1.3)
        print(1.35)
        self.widget = self.masterWindow.getDaWindow()
        print(1.4)

    def doTheMainloop(self):
        self.masterWindow.run()

    def changevar(self, var, attr, value):
        '''Changes a variable of the window.
        Parameters: str,str,str
        Returns: None'''
        self.widget.changevar(var, attr, value)

    def getWindow(self):
        sleep(.5)
        self.widget = self.masterWindow.getDaWindow()

    def dodathing(self):
        print(self.widget.ids.accuracy.text)

###################################################################################################################################

if __name__ == '__main__':
    app = RunningWindow()
    app.mainloop()
    app.getWindow()
    app.changevar('accuracy','text','thisWorks')
    app.dodathing()



