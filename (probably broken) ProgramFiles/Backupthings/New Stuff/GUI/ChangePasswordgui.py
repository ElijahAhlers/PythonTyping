#Build into python
import sys

#Kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

#Our Stuff
from Logic.CSVFuncs import writeNewCSVFile as wnCSV
from Logic.CSVFuncs import readCSVFile as rCSV

Window.borderless = True

class firstLogin(GridLayout):
    Builder.load_file('KivyGraphicFiles/firstLogin.kv')
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.alldata = rCSV('/'.join(sys.path[0].split('\\')[:-1])+'/UserData/UsernameAndPassword.csv')
        
    def changePassword(self):
        count = 0
        for person in self.alldata:
            if person['Username'] == self.user.username:
                registered = person['Registered']
                self.alldata.pop(count)
                break
            count+=1
        newdata = {'Username':self.user.username,'Password':self.ids.newPassword.text,'Registered':registered}
        self.alldata.insert(count,newdata)
        wnCSV('/'.join(sys.path[0].split('\\')[:-1])+'/UserData/UsernameAndPassword.csv',['Username','Password','Registered'],self.alldata)
        self.parent.parent.current = 'LessonSelectScreen'

    def verifyData(self):
        oldPasswordCorrect = False
        passwordsMatch = False
        for person in self.alldata:
            if person['Username'] == self.user.username:
                if self.ids.oldPassword.text == person['Password']:
                    oldPasswordCorrect = True
                else:
                    self.ids.whatWentWrong.text = 'Old password is incorrect'
        if self.ids.newPassword.text == self.ids.confirmNewPassword.text:
            passwordsMatch = True
        else:
            self.ids.whatWentWrong.text = 'Passwords do not match'
        if oldPasswordCorrect and passwordsMatch:
            self.changePassword()
