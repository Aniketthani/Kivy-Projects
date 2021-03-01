from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.image import Image
from kivy.properties import ObjectProperty,NumericProperty,ListProperty,AliasProperty
from kivy.clock import Clock
from random import uniform
from kivy.uix.image import Image as ImageWidget
from kivy.core.window import Window,Keyboard
from kivy.core.audio import SoundLoader

class  MultiAudio:
    _next=0

    def __init__(self,filename,count):
        self.buff=[SoundLoader.load(filename) for i in range(count)]
    
    def play(self):
        self.buff[self._next].play()
        self._next=(self._next + 1) % len(self.buff)

class BaseWidget(Widget):
    def load_tileable(self,name):
        t=Image("images/%s.png"%name).texture
        t.wrap="repeat"
        
        setattr(self,'tx_%s'%name,t)

class Background(BaseWidget):
    tx_floor=ObjectProperty(None)
    tx_grass=ObjectProperty(None)
    tx_cloud=ObjectProperty(None)
    def __init__(self,**kwargs):
        super(Background,self).__init__(**kwargs)

        for tx in ('floor','cloud','grass'):       
            self.load_tileable(tx)
    def update(self,nap):
        self.set_background_uv('tx_floor',2*nap)
        self.set_background_uv('tx_cloud',0.1*nap)
        self.set_background_uv('tx_grass',0.5*nap)
    
    def set_background_uv(self,name,nap):
        t=getattr(self,name)
        t.uvpos=((t.uvpos[0]+nap)%self.width,t.uvpos[1])
        self.property(name).dispatch(self)
    
    def set_background_size(self):
        tx=getattr(self,"tx_cloud")
        tx.uvsize=(self.width/tx.width,-1)
        self.property("tx_cloud").dispatch(self)

    def on_size(self,*args):
        self.set_background_size()

class Pipe(BaseWidget):
    
    
    

    FLOOR=96
    PCAP_HEIGHT=26
    PIPE_GAP=3*Window.height/15

    tx_pipe=ObjectProperty(None)
    tx_pcap=ObjectProperty(None)

    ratio=NumericProperty(0.5)
    lower_len=NumericProperty(0)
    lower_coords=ListProperty([0,0,1,0,1,1,0,1])
    upper_len=NumericProperty(0)
    upper_coords=ListProperty([0,0,1,0,1,1,0,1])

    

    def __init__(self,**kwargs):
        super(Pipe,self).__init__(**kwargs)

        for name in ('pipe','pcap'):
            self.load_tileable(name)

        self.bind(ratio=self.on_size)


    def set_coords(self,coords,len):
        len/=20 # here 20 is the height of the texture of pipe
        coords[5:]=(len,0,len) # set the last 3 items
        return coords

    def on_size(self,*args):
        pipe_length= self.height - (self.FLOOR + self.PIPE_GAP  + 2*self.PCAP_HEIGHT  ) # len of both pipe body only
       
        self.lower_len=self.ratio * pipe_length
        
        self.upper_len=pipe_length - self.lower_len

        self.upper_coords=self.set_coords(self.upper_coords,self.upper_len)
        self.lower_coords=self.set_coords(self.lower_coords,self.lower_len)


class Bird(ImageWidget):
    ACCEL_FALL=0.25
    ACCEL_JUMP = 5

    
    speed=NumericProperty(0)
    angle=AliasProperty(lambda self: 5*self.speed,None,bind=['speed'])
    def gravity_on(self,height):
        # Replace pos_hint with a value
        self.pos_hint.pop('center_y', None)
        self.center_y = 0.6 * height
    def update(self,nap):
        
        self.speed -= self.ACCEL_FALL
        self.y += self.speed
        

        
        
        
    def bump(self):
        self.speed = Bird.ACCEL_JUMP
       

class KivyBirdApp(App):
    snd_bump=MultiAudio('sounds/bump.wav',4)
    snd_game_over=SoundLoader.load('sounds/game_over.wav')
    playing=False
    pipes=[]
    was_colliding=False

    hiscore=0

    with open("highscore.txt","r") as f:
        txt=f.read()
        if txt:
            hiscore=str(txt)
            f.close()

    

    def test_game_over(self):
        self.score=self.root.ids.score
        is_colliding=False
        if self.bird.y < 90 or self.bird.y > self.root.height - 50:
            return True
        for p in self.pipes:
            if self.bird.collide_widget(p):
                is_colliding=True
                if self.bird.y < p.FLOOR + p.lower_len + p.PCAP_HEIGHT :
                    return True
                if self.bird.top > p.FLOOR + p.lower_len + p.PCAP_HEIGHT + p.PIPE_GAP:
                    return True 
        if self.was_colliding and not is_colliding:
            self.score.text=str(int(self.score.text)+1)
        self.was_colliding=is_colliding
        return False

    def on_start(self):
        
        
        self.title="Kivy Bird By Aniket Thani"
        self.spacing=0.5*self.root.width
        self.background=self.root.ids.background
        self.bird=self.root.ids.bird
        
        self.root.ids.highscore.text="HighScore : "+ str(self.hiscore)

        Clock.schedule_interval(self.update,1/60)
        Window.bind(on_key_down=self.on_key_down)
        self.background.on_touch_down=self.user_action

    
    def on_key_down(self,window,key,*args):
        if key==Keyboard.keycodes['spacebar']:
            self.user_action()
    
    def user_action(self,*args):
        self.snd_bump.play()
        self.bird.bump()
        
        if not self.playing:
            self.root.ids.score.text="0"
            self.was_colliding=False
            self.bird.gravity_on(self.root.height)
            self.spawn_pipes()
            self.playing=True
            self.root.ids.start_or_over_label.text=""
            self.root.ids.highscore.text=""
            


    def update(self,nap): 
        
        if  not self.playing:
            return
        self.background.update(nap)
        self.bird.update(nap)

        for p in self.pipes:
            p.x-=100*nap
            if p.x<=-64:  # pipe gone off screen
                p.x += 4*self.spacing
                p.ratio = uniform(0.25,0.75)

        

        if self.test_game_over():
            self.snd_game_over.play()
            self.playing=False
            self.root.ids.start_or_over_label.text='Gameover !! Tap to Restart'
            
            with open("highscore.txt","rt") as f:
                hscore=f.read()
                
                if hscore and int(hscore)<int(self.root.ids.score.text):
                    f.close()
                    with open("highscore.txt","w") as file:
                        file.write(self.root.ids.score.text)
                        file.close()
                        self.root.ids.highscore.text="Highscore : "+str(self.root.ids.score.text)
            

        
    def spawn_pipes(self):
        for p in self.pipes:
            self.root.remove_widget(p)
        self.pipes=[]

        for i in range(4):
            p=Pipe(x=self.root.width + (self.spacing*i),width=64,size_hint_x=None)
            p.ratio=uniform(0.25,0.75)
            
            
            self.root.add_widget(p)
            self.pipes.append(p)

if __name__=="__main__":
    KivyBirdApp().run()
