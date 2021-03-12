from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Canvas, Rectangle


kv = """
<Stick_Man>:
    rows: 1
    cols: 1
    canvas.before:
        Color:
            rgba: (.4, .6, 9, 1)
        Rectangle:
            size: self.size
            pos: self.pos
    canvas:
        Color:
            rgba: (1, 1, 1,1)
        Rectangle:
            size : 20,200
            pos : self.width/2.025, self.height/2.2
            
        Line:
            circle: (self.width/1.993, self.height/1.15, 30)
            width: 30
##            circle: (415, 450, 50)
##            width: 10

 
<mainScreen>:
    rows: 1
    cols: 1
    Stick_Man
"""
Builder.load_string(kv)
class Stick_Man(GridLayout):
    pass
#    def on_touch_down

class mainScreen(GridLayout):
    pass

class MyApp(App):
    def build(self):
        return mainScreen()

app = MyApp()
app.run()
