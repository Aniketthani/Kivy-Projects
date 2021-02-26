from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score=NumericProperty(0)

    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset



class PongBall(Widget):
    

    velocity_x=NumericProperty(0)
    velocity_y=NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y

    velocity=ReferenceListProperty(velocity_x,velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball

    


    def move(self):
        self.pos=Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball=ObjectProperty(None)
    paddle1=ObjectProperty(None)
    paddle2=ObjectProperty(None)
    
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(7, 0).rotate(randint(0, 360))

    def update_game(self,dt):
        self.ball.move()
        self.paddle1.bounce_ball(self.ball)
        self.paddle2.bounce_ball(self.ball)

        #bounce from top and bottom
        if (self.ball.center[1]+self.ball.size[0]/2)>=self.height:
            self.ball.velocity_y*=-1
        if (self.ball.center[1]-self.ball.size[0]/2)<=0:
            self.ball.velocity_y*=-1
        
        #bounce from left and right
        if (self.ball.center[0]+self.ball.size[0]/2)>=self.width:
            self.ball.velocity_x*=-1
            
            
                
        if (self.ball.center[0]-self.ball.size[0]/2 )<=0:
            self.ball.velocity_x*=-1

        # went of to a side to score point?
        if self.ball.x < self.x:
            self.paddle2.score += 1
            self.serve_ball()
        if self.ball.center_x > self.width -self.ball.size[0]/2  :
            self.paddle1.score += 1
            self.serve_ball()
        
    def on_touch_move(self,touch):
        if touch.x < self.width/3:
            
                if touch.y<7*self.height/10:
                    self.paddle1.center_y=touch.y
                if touch.y>3*self.height/10:
                    self.paddle1.center_y=touch.y
        if touch.x > 2*self.width/3:
            if touch.y<7*self.height/10:
              self.paddle2.center_y=touch.y       
            if touch.y>3*self.height/10:
              self.paddle2.center_y=touch.y       

             

class PongApp(App):
    def build(self):
       
        self.title="Pong By Aniket Thani"
        game=PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update_game,1/60)
        return game

if __name__=="__main__":
    PongApp().run()