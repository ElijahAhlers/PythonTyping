from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('KivyGraphicFiles/AdminScreen.kv')

class AdminScreenLayout(BoxLayout):

    def goToTyping(self):
        print('I did something!')
        self.parent.parent.current = 'LessonSelectScreen'
