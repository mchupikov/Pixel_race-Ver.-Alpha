from pygame import *
from random import randint, choice
w = display.set_mode((1000, 800))
bg1 = transform.scale(image.load("Images\Roads.png"), (1000, 800))
bg2 = transform.scale(image.load("Images\Roads.png"), (1000, 800))
car_color = ["Images\Orange_car.png",
             "Images\Green_car.png",
             "Images\Red_car.png"]
ypositions = [485, 605, 705]
r_car_anim = [transform.scale(image.load("Images\Car_1.png"), (160, 78)),
              transform.scale(image.load("Images\Car_2.png"), (160, 78))]
r_car_anim_count = 0
x_bg_move = 0
x_bg2_move = 1000
game = 1
fps = 40
finish = 0
class GameSprite(sprite.Sprite):
    def __init__(self, filename, w, h, x, y, speed):
        super().__init__()
        self.filename = filename
        self.w, self.h = w, h
        self.im = transform.scale(image.load(filename), (w, h))
        self.speed = speed
        self.rect = self.im.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        w.blit(self.im, (self.rect.x, self.rect.y))
class Buttons(sprite.Sprite):
    def __init__(self, filename, w, h, x, y, text=None):
        super().__init__()
        self.im = transform.scale(image.load(filename), (w, h))
        self.rect = self.im.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
    def blitbutton(self):
        w.blit(self.im, (self.rect.x, self.rect.y))
class RaceCar(GameSprite):
    def update(self):
        global r_car_anim_count
        keys = key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            if self.rect.y >= 485:
                self.rect.y -= self.speed
        if keys[K_DOWN] or keys[K_s]:
            if self.rect.y <= 705:
                self.rect.y += self.speed
        if keys[K_LEFT] or keys[K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if keys[K_RIGHT] or keys[K_d]:
            if self.rect.x <= 1000 - self.rect.w:
                self.rect.x += self.speed
        if r_car_anim_count <= 1:
            w.blit(r_car_anim[r_car_anim_count], (self.rect.x, self.rect.y))
            r_car_anim_count += 1
        else:
            r_car_anim_count = 0
            w.blit(r_car_anim[r_car_anim_count], (self.rect.x, self.rect.y))
class Car(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= -self.rect.w:
            self.filename = choice(car_color)
            self.im = transform.scale(image.load(self.filename), (self.w, self.h))
            self.rect.x = 1000 + self.rect.w
            self.rect.y = choice(ypositions)
rc = RaceCar("Images\Car_1.png", 160, 78, 200, 485, 5)
car_npc = Car("Images\Red_car.png", 160, 78, 1160, 485, 5)
btn_ex = Buttons("Images\Exit_button.png", 50, 50, 25, 25)
c = time.Clock()
while game:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if btn_ex.rect.collidepoint(x, y):
                game = 0
    if sprite.collide_rect(rc, car_npc):
        finish = 1
    if not finish:
        w.blit(bg1, (x_bg_move, 0))
        x_bg_move -= 5
        w.blit(bg2, (x_bg2_move, 0))
        x_bg2_move -= 5
        if x_bg_move <= -1000:
            x_bg_move = 1000
        if x_bg2_move <= -1000:
            x_bg2_move = 1000
        rc.reset()
        rc.update()
        car_npc.reset()
        car_npc.update()
        btn_ex.blitbutton()
    c.tick(fps)
    display.update()
    