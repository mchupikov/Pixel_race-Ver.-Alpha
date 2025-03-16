from pygame import *
from random import randint, choice
font.init()
ftxt1 = font.Font("Fonts\Pixel.ttf", 80)
w = display.set_mode((1000, 800))
bg1 = transform.scale(image.load("Images\Roads.png"), (1000, 800))
bg2 = transform.scale(image.load("Images\Roads.png"), (1000, 800))
car_color = ["Images\Orange_car.png",
             "Images\Green_car.png",
             "Images\Red_car.png"]
ypositions = [485, 605, 705]
r_car_anim = [transform.scale(image.load("Images\Car_1.png"), (160, 78)),
              transform.scale(image.load("Images\Car_2.png"), (160, 78))]
block_anim = [transform.scale(image.load("Images\Block_1.png"), (100, 100)),
              transform.scale(image.load("Images\Block_1.png"), (100, 100)),
              transform.scale(image.load("Images\Block_2.png"), (100, 100)),
              transform.scale(image.load("Images\Block_2.png"), (100, 100)),
              transform.scale(image.load("Images\Block_3.png"), (100, 100)),
              transform.scale(image.load("Images\Block_3.png"), (100, 100))]
r_car_anim_count = 0
block_anim_count = 0
x_bg_move = 0
x_bg2_move = 1000
game = 1
fps = 40
finish = 0
screen = "menu"
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
        txtf = font.Font("Fonts\Pixel.ttf", 40)
        text_surface = txtf.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center = self.rect.center)
        w.blit(text_surface, text_rect)
class RaceCar(GameSprite):
    def update(self):
        global r_car_anim_count
        if r_car_anim_count <= 1:
            w.blit(r_car_anim[r_car_anim_count], (self.rect.x, self.rect.y))
            r_car_anim_count += 1
        else:
            r_car_anim_count = 0
            w.blit(r_car_anim[r_car_anim_count], (self.rect.x, self.rect.y))
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
class Car(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= -self.rect.w:
            self.filename = choice(car_color)
            self.im = transform.scale(image.load(self.filename), (self.w, self.h))
            self.rect.x = 1000 + self.rect.w
            self.rect.y = choice(ypositions)
class Block(GameSprite):
    def update(self):
        global block_anim_count
        if block_anim_count <= 5:
            w.blit(block_anim[block_anim_count], (self.rect.x, self.rect.y))
            block_anim_count += 1
        else:
            block_anim_count = 0
            w.blit(block_anim[block_anim_count], (self.rect.x, self.rect.y))
        self.rect.x -= self.speed
        if self.rect.x <= -self.rect.w:
            self.rect.x = 1000 + self.rect.w
            self.rect.y = choice(ypositions)
class Bus(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x <= -self.rect.w:
            self.rect.x = 1500
            self.rect.y = choice(ypositions)
chosing_difficulity_txt = ftxt1.render("Виберіть складність", True, (0, 0, 0))
game_over_txt = ftxt1.render("Game over!!!", True, (255, 0, 0))
gamelogo = transform.scale(image.load("Images\Game_logo.png"), (600, 78))
rc = RaceCar("Images\Car_1.png", 160, 78, 200, 485, 5)
car_npc = Car("Images\Red_car.png", 160, 78, 1160, 485, 5)
bl = Block("Images\Block_1.png", 100, 100, 1100, 705, 5)
bus1 = Bus("Images\School_bus.png", 200, 85, 1500, 705, 2)
btn_ex = Buttons("Images\Exit_button.png", 50, 50, 25, 25)
btn_play = Buttons("Images\Button.png", 400, 50, 300, 300, "Грати")
btn_reset = Buttons("Images\Button.png", 400, 50, 300, 400, "Грати ще раз")
btn_lite = Buttons("Images\Button.png", 400, 50, 300, 300, "Легка")
btn_normal = Buttons("Images\Button.png", 400, 50, 300, 400, "Нормальна")
btn_hard = Buttons("Images\Button.png", 400, 50, 300, 500, "Складна")
c = time.Clock()
while game:
    if screen == "lite":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    screen = "menu"
                if btn_reset.rect.collidepoint(x, y):
                    finish = 0
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 705
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
        if finish:
            w.blit(game_over_txt, (300, 150))
            btn_reset.blitbutton()
    if screen == "normal":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    screen = "menu"
                if btn_reset.rect.collidepoint(x, y):
                    finish = 0
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
        if sprite.collide_rect(rc, car_npc) or sprite.collide_rect(rc, bl):
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
            bl.reset()
            bl.update()
            btn_ex.blitbutton()
        if finish:
            w.blit(game_over_txt, (300, 150))
            btn_reset.blitbutton()
    if screen == "hard":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    screen = "menu"
                if btn_reset.rect.collidepoint(x, y):
                    finish = 0
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
                    bus1.rect.x, bus1.rect.y = 1500, 705
        if sprite.collide_rect(rc, car_npc) or sprite.collide_rect(rc, bl) or sprite.collide_rect(rc, bus1):
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
            bl.reset()
            bl.update()
            bus1.reset()
            bus1.update()
            btn_ex.blitbutton()
        if finish:
            w.blit(game_over_txt, (300, 150))
            btn_reset.blitbutton()
    if screen == "menu":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    game = 0
                if btn_play.rect.collidepoint(x, y):
                    screen = "chosing_difficulity"
        w.blit(bg1, (0, 0))
        w.blit(gamelogo, (250, 200))
        btn_ex.blitbutton()
        btn_play.blitbutton()
    if screen == "chosing_difficulity":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    screen = "menu"
                if btn_lite.rect.collidepoint(x, y):
                    screen = "lite"
                    finish = 0 
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                if btn_normal.rect.collidepoint(x, y):
                    screen = "normal"
                    finish = 0 
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
                if btn_hard.rect.collidepoint(x, y):
                    screen = "hard"
                    finish = 0 
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
                    bus1.rect.x, bus1.rect.y = 1500, 705
        w.blit(bg1, (0, 0))
        w.blit(chosing_difficulity_txt, (60, 200))
        btn_lite.blitbutton()
        btn_normal.blitbutton()
        btn_hard.blitbutton()
        btn_ex.blitbutton()
    c.tick(fps)
    display.update()