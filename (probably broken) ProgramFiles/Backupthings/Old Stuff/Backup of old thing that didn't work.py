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
from functools import partial




class TypingWindow(GridLayout):
    
    
    def changevar(self,var,attr,value):
        '''Changes your variable's .text attribute to your value
        Parameters: str, str
        Returns: None'''
        exec('self.ids.'+str(var)+'.'+str(attr)+' = "'+str(value)+'"')
        
    def exit(self):
        #self.ids.rawWPM.text = 'hello'
        self.get_root_window().close()

class TypingAppWindow(App):
    def build(self):
        self.window = TypingWindow()
        return self.window

    def getDaWindow(self):
        return self.window

class RunningWindow():
    '''Makes a window for typing.  Makes a blank window
        when you call it, but needs constant updating.
        Methods: update,changevar'''

    def __init__(self):
        from kivy.core.window import Window
        Builder.load_file('KivyGraphicFiles/TypingWindow.kv')
        #Window.fullscreen = 'auto'
        #Window.boarderless = False
        self.widget = TypingWindow()
        runTouchApp(self.widget, slave=True)
        self.counter = 0
        

    def update(self):
        '''Updates the screen.
        Parameters: None
        Returns: None'''
        EventLoop.window._mainloop()

    def mainloop(self):
        EventLoop.window.mainloop()
        print('afterthemainloop')

    def startUpdateClock(self):
        print('arrived at startUpdateClock')
        Clock.schedule_interval(self.updateScreenThingy,1/60)
        print('at the end of the startUpdateClock function')

    def updateScreenThingy(self,var):
        EventLoop.window._mainloop()
        print(self.counter)
        self.counter+=1

    def changevar(self, var, attr, value):
        '''Changes a variable of the window.
        Parameters: str,str,str
        Returns: None'''
        self.widget.changevar(var, attr, value)


if __name__ == '__main__':
    app = RunningWindow()
    while True:
        app.update()

