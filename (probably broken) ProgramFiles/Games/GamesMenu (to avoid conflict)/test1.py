from kivy.uix.widget import Widget
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix

KV = """

CRect:
    canvas:
        Color:
            rgba: 1,0,0,1
        rectangle:
            pos: 100,0
            size: 40,40


"""

class CRect(Widget):
    velocity = ListProperty([200, 100])
    rect_x, rect_y = 0, 0

    def __init__(self, **kwargs):
        super(CRect, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        rect = self.canvas.children[-1]
        self.rect_x += self.velocity[0]
        self.rect_y += self.velocity[1]

        rect.pos = self.rect_x, self.rect_y

        if self.rect_x < 0 or (self.rect_x+rect.size[0]) > Window.width:
            self.velocity[0] *= -1

        if self.rect_y < 0 or (self.rect_y+rect.size[1]) > Window.height:
            self.velocity[1] *= -1


class MyApp(App):
    def build(self):
        return Builder.load_string(KV)

MyApp().run()
