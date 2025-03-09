from pygame import *
from random import randint
w = display.set_mode((0, 0), FULLSCREEN)
w_win, h_win = w.get_size()
bg1 = transform.scale(image.load("Images\Roads.png"), (w_win, h_win))
bg2 = transform.scale(image.load("Images\Roads.png"), (w_win, h_win))
x_bg_move = 0
x_bg2_move = w_win
game = 1
fps = 40
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, x, y, speed):
        super().__init__()
        self.im = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.r = self.im.get_rect()
        self.r.x = x
        self.r.y = y
    def reset(self):
        w.blit(self.im, (self.r.x, self.r.y))
class Buttons(sprite.Sprite):
    def __init__(self, filename, w, h, x, y, text=None):
        super().__init__()
        self.im = transform.scale(image.load(filename), (w, h))
        self.r = self.im.get_rect()
        self.r.x = x
        self.r.y = y
        self.text = text
    def blitbutton(self):
        w.blit(self.im, (self.r.x, self.r.y))
class RaceCar(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            if self.r.y >= 550:
                self.r.y -= self.speed
        if keys[K_DOWN] or keys[K_s]:
            if self.r.y <= 805:
                self.r.y += self.speed
        if keys[K_LEFT] or keys[K_a]:
            if self.r.x >= 0:
                self.r.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            if self.r.x <= w_win - self.r.w:
                self.r.x += self.speed
class Car(GameSprite):
    def update(self):
        self.r.x -= self.speed
        if self.r.x <= -self.r.w:
            self.r.x = w_win + self.r.w
rc = RaceCar("Images\Car_1.png", 160, 78, 200, 550, 5)
car_1 = Car("Images\Red_car.png", 160, 78, h_win + 160, 550, 5)
btn_ex = Buttons("Images\Exit_button.png", 50, 50, 25, 25)
c = time.Clock()
while game:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if btn_ex.r.collidepoint(x, y):
                game = 0 
    w.blit(bg1, (x_bg_move, 0))
    x_bg_move -= 5
    w.blit(bg2, (x_bg2_move, 0))
    x_bg2_move -= 5
    if x_bg_move <= -w_win:
        x_bg_move = w_win
    if x_bg2_move <= -w_win:
        x_bg2_move = w_win
    rc.reset()
    rc.update()
    car_1.reset()
    car_1.update()
    btn_ex.blitbutton()
    c.tick(fps)
    display.update()
    