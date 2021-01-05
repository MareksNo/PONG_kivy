from random import randint

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def reset_score(self):
        self.player2.score, self.player1.score = 0, 0

    def serve_ball(self):
        self.ball.pos = self.center
        self.ball.velocity = Vector(3, 0).rotate(randint(20, 340))

    def update(self, dt):

        self.player2.bounce_ball(self.ball)
        self.player1.bounce_ball(self.ball)
        if (self.ball.y <= 0) or (self.ball.y >= self.height - self.ball.height):
            self.ball.velocity_y *= -1

        if self.ball.x <= 15:
            self.ball.velocity_x *= -1
            self.player2.score += 1
            if self.player2.score >= 7:
                self.reset_score()
            self.serve_ball()

        if self.ball.x >= self.width - self.ball.width - 15:
            self.ball.velocity_x *= -1
            self.player1.score += 1
            if self.player1.score >= 7:
                self.reset_score()
            self.serve_ball()

        self.ball.move()

    def on_touch_move(self, touch):
        if touch.x < self.width / 4:
            self.player1.center_y = touch.y
        if touch.x > self.width / 4 * 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1/90.0)
        return game


if __name__ == '__main__':
    PongApp().run()


'''    
def count_score(self):
        if self.ball.x < self.player1.width / 2:
            self.score2.text = str(int(self.score2.text) + 1)
            self.ball.pos = self.center
            self.ball.velocity_x = 4

        if self.ball.right > self.player2.right:

            self.score1.text = str(int(self.score1.text) + 1)
            self.ball.pos = self.center
            self.ball.velocity_x = -4
'''
