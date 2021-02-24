from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line,Color
from kivy.lang import Builder
#for changing the behavior of ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton 

Builder.load_file("paint.kv")

class RadioButton(ToggleButton):
    def _do_press(self):
        if self.state=="normal":
            ToggleButtonBehavior._do_press(self)

class MyCanvas(Widget):
    line_width = 2
    def on_touch_down(self,touch):
        for widgets in self.children:
            if widgets.on_touch_down(touch):
                return True
        with self.canvas:
           
            touch.ud['line']=Line(points=(touch.x,touch.y),width=self.line_width)
    def on_touch_move(self,touch):
        if not (touch.y>=0 and touch.y<=40):
            touch.ud['line'].points+=(touch.x,touch.y)
    def clear_screen(self):
        saved_widgets=self.children[:]
        #remove all widgets
        self.clear_widgets()
        #clear the canvas
        self.canvas.clear()
        #add the widgets back 
        for w in saved_widgets:
            self.add_widget(w)
    def set_color(self,new_color):
        
        with self.canvas:
            Color(*new_color)
    def set_line_width(self,line_width):
        self.line_width={'Thin': 1, 'Normal': 2, 'Thick': 4}[line_width]       
    
class PaintApp(App):
    def build(self):
        
        return MyCanvas()

if __name__=="__main__":

    #setting window size
    from kivy.config import Config
    Config.set('graphics','width','1000')
    Config.set('graphics','height','800')

    #making window non resizable
    #Config.set('graphics','resizable','0')

    #disable multitouch by mouse's right click that also generate a dot at that place
    Config.set('input', 'mouse', 'mouse,disable_multitouch')
    from kivy.core.window import Window
    Window.clearcolor=(1,1,1,1)
    PaintApp().run()