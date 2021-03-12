#Kivy stuff
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

#Stuff we made
from Logic import CheckLogin as cl
from Logic import UserClass

Builder.load_file('KivyGraphicFiles/LoginMaster.kv')    
Window.borderless = True
Window.clearcolor = (0,0,0,0)

class LoginWindow(GridLayout):

    needToUpdate = False
    
    def ExitButton(self):
        self.get_root_window().close()
        
    def Authenticate(self):
        self.username = self.ids.username.text.lower()
        if not cl.CheckCreds(self.ids.username.text.lower(),self.ids.password.text):
            self.ids.incpass.text = 'Incorrect Password'
            self.ids.incpass.color = 1,0,0,1
        else:
            self.parent.parent.activeUser = UserClass.User(self.username)
            self.parent.parent.AddSelectScreen()
            self.parent.parent.current = 'LessonSelectScreen'
            

    def changeUpdateStatus(self,boolean):
        self.needToUpdate = boolean
        
    def checkforupdates(self):
        if self.needToUpdate:
            self.ids.notifyupdate.text = 'Update will begin \nwith sucessful login'
            self.ids.notifyupdate.color = 1,0,0,1
