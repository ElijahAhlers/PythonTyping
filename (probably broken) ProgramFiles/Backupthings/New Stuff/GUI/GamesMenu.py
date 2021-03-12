from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import sys

class GamesMenu(GridLayout):
    def __init__(self,**kwargs):
        Builder.load_file('/'.join(sys.path[0].split('\\')[:-1])+'/ProgramFiles/KivyGraphicFiles/GamesMenu.kv')
        super(GamesMenu,self).__init__(**kwargs)

    def goToLetterGame(self):
        self.parent.parent.LetterGame()
        self.parent.parent.current = 'Letter Game'

if __name__ == "__main__":
    class GamesMaster(App):
        def build(self):
            return GamesMenu()

    x = GamesMaster()
    x.run()
        


    
