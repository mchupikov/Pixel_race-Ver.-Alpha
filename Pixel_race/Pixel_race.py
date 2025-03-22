from pygame import *
from random import choice
import json
font.init()
mixer.init()
mixer.music.load("Audio\On_the_road_to_the_eighties.mp3")
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
with open("JSONfiles\settings_save.json", "r") as file:
    data_set = json.load(file)
music_volume = data_set["mus_vol"]
sound_volume = data_set["s_vol"]
accident_sound = mixer.Sound("Audio\An_accident.ogg")
accident_sound.set_volume(sound_volume)
mixer.music.set_volume(music_volume)
mixer.music.play()
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
    def __init__(self, filename, w, h, x, y, sound, text=None):
        super().__init__()
        self.im = transform.scale(image.load(filename), (w, h))
        self.rect = self.im.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text
        self.sound = mixer.Sound(sound)
    def blitbutton(self):
        w.blit(self.im, (self.rect.x, self.rect.y))
        txtf = font.Font("Fonts\Pixel.ttf", 40)
        text_surface = txtf.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center = self.rect.center)
        w.blit(text_surface, text_rect)
    def playsound(self):
        self.sound.set_volume(sound_volume)
        self.sound.play()
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
settings_title = ftxt1.render("Налаштування", True, (0, 0, 0))
sound_text = ftxt1.render("Гучність звуку", True, (0, 0, 0))
music_text = ftxt1.render("Гучність музики", True, (0, 0, 0))
gamelogo = transform.scale(image.load("Images\Game_logo.png"), (600, 78))
rc = RaceCar("Images\Car_1.png", 160, 78, 200, 485, 5)
car_npc = Car("Images\Red_car.png", 160, 78, 1160, 485, 5)
bl = Block("Images\Block_1.png", 100, 100, 1100, 705, 5)
bus1 = Bus("Images\School_bus.png", 200, 85, 1500, 705, 2)
btn_ex = Buttons("Images\Exit_button.png", 50, 50, 25, 25, "Audio\Button_sound.ogg")
btn_play = Buttons("Images\Button.png", 400, 50, 300, 300, "Audio\Button_sound.ogg", "Грати")
btn_reset = Buttons("Images\Button.png", 400, 50, 300, 400, "Audio\Button_sound.ogg", "Грати ще раз")
btn_lite = Buttons("Images\Button.png", 400, 50, 300, 300, "Audio\Button_sound.ogg", "Легка")
btn_normal = Buttons("Images\Button.png", 400, 50, 300, 400, "Audio\Button_sound.ogg", "Нормальна")
btn_hard = Buttons("Images\Button.png", 400, 50, 300, 500, "Audio\Button_sound.ogg", "Складна")
btn_rules = Buttons("Images\Button.png", 400, 50, 300, 400, "Audio\Button_sound.ogg", "Як грати?")
btn_records = Buttons("Images\Button.png", 400, 50, 300, 500, "Audio\Button_sound.ogg", "Рекорди")
btn_settings = Buttons("Images\Button.png", 400, 50, 300, 600, "Audio\Button_sound.ogg", "Налаштування")
btn_mute_sound = Buttons("Images\Mute_sound.png", 100, 100, 300, 300, "Audio\Button_sound.ogg")
btn_minus_sound = Buttons("Images\Minus.png", 100, 100, 410, 300, "Audio\Button_sound.ogg")
btn_plus_sound = Buttons("Images\Plus.png", 100, 100, 510, 300, "Audio\Button_sound.ogg")
btn_mute_music = Buttons("Images\Mute.png", 100, 100, 300, 500, "Audio\Button_sound.ogg")
btn_minus_music = Buttons("Images\Minus.png", 100, 100, 410, 500, "Audio\Button_sound.ogg")
btn_plus_music = Buttons("Images\Plus.png", 100, 100, 510, 500, "Audio\Button_sound.ogg")
c = time.Clock()
while game:
    if screen == "chosing_difficulity":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
                if btn_lite.rect.collidepoint(x, y):
                    btn_lite.playsound()
                    screen = "lite"
                    finish = 0 
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    life_x = 700
                    lifes = []
                    for i in range(3):
                        life = GameSprite("Images\Heart.png", 50, 50, life_x, 10, 0)
                        lifes.append(life)
                        life_x += 75
                if btn_normal.rect.collidepoint(x, y):
                    btn_normal.playsound()
                    screen = "normal"
                    finish = 0 
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
                    life_x = 700
                    lifes = []
                    for i in range(2):
                        life = GameSprite("Images\Heart.png", 50, 50, life_x, 10, 0)
                        lifes.append(life)
                        life_x += 75
                if btn_hard.rect.collidepoint(x, y):
                    btn_hard.playsound()
                    screen = "hard"
                    finish = 0 
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
                    bus1.rect.x, bus1.rect.y = 1500, 705
                    life_x = 700
                    lifes = []
                    for i in range(2):
                        life = GameSprite("Images\Heart.png", 50, 50, life_x, 10, 0)
                        lifes.append(life)
                        life_x += 75
        w.blit(bg1, (0, 0))
        w.blit(chosing_difficulity_txt, (60, 200))
        btn_lite.blitbutton()
        btn_normal.blitbutton()
        btn_hard.blitbutton()
        btn_ex.blitbutton()
    if screen == "lite":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
                if btn_reset.rect.collidepoint(x, y):
                    btn_reset.playsound()
                    finish = 0
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 705
        if sprite.collide_rect(rc, car_npc):
            if len(lifes) > 0:
                rc.rect.x -= 200
                lifes.pop()
            else:
                accident_sound.play()
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
            for h in lifes:
                h.reset()
        if finish:
            w.blit(game_over_txt, (300, 150))
            btn_reset.blitbutton()
            life_x = 700
            lifes = []
            for i in range(3):
                life = GameSprite("Images\Heart.png", 50, 50, life_x, 10, 0)
                lifes.append(life)
                life_x += 75
    if screen == "normal":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
                if btn_reset.rect.collidepoint(x, y):
                    btn_reset.playsound()
                    finish = 0
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
        if sprite.collide_rect(rc, car_npc) or sprite.collide_rect(rc, bl):
            if len(lifes) > 0:
                rc.rect.x -= 200
                lifes.pop()
            else:
                accident_sound.play()
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
            for h in lifes:
                h.reset()
        if finish:
            w.blit(game_over_txt, (300, 150))
            btn_reset.blitbutton()
            life_x = 700
            lifes = []
            for i in range(2):
                life = GameSprite("Images\Heart.png", 50, 50, life_x, 10, 0)
                lifes.append(life)
                life_x += 75
    if screen == "hard":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
                if btn_reset.rect.collidepoint(x, y):
                    btn_reset.playsound()
                    finish = 0
                    rc.rect.x, rc.rect.y = 200, 485
                    car_npc.rect.x, car_npc.rect.y = 1160, 485
                    bl.rect.x, bl.rect.y = 1100, 705
                    bus1.rect.x, bus1.rect.y = 1500, 705
        if sprite.collide_rect(rc, car_npc) or sprite.collide_rect(rc, bl) or sprite.collide_rect(rc, bus1):
            if len(lifes) > 0:
                rc.rect.x -= 200
                lifes.pop()
            else:
                accident_sound.play()
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
            for h in lifes:
                h.reset()
        if finish:
            w.blit(game_over_txt, (300, 150))
            btn_reset.blitbutton()
            life_x = 700
            lifes = []
            for i in range(2):
                life = GameSprite("Images\Heart.png", 50, 50, life_x, 10, 0)
                lifes.append(life)
                life_x += 75
    if screen == "menu":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    game = 0
                if btn_play.rect.collidepoint(x, y):
                    btn_play.playsound()
                    screen = "chosing_difficulity"
                if btn_settings.rect.collidepoint(x, y):
                    btn_settings.playsound()
                    screen = "settings"
                if btn_rules.rect.collidepoint(x, y):
                    btn_rules.playsound()
                    screen = "rules"
                if btn_records.rect.collidepoint(x, y):
                    btn_records.playsound()
                    screen = "records"
        w.blit(bg1, (0, 0))
        w.blit(gamelogo, (250, 200))
        btn_ex.blitbutton()
        btn_play.blitbutton()
        btn_rules.blitbutton()
        btn_records.blitbutton()
        btn_settings.blitbutton()
    if screen == "settings":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
                if btn_mute_sound.rect.collidepoint(x, y):
                    btn_mute_sound.playsound()
                    with open("JSONfiles\settings_save.json", "w") as file:
                        data_set["s_vol"] = 0
                        sound_volume = data_set["s_vol"]
                        json.dump(data_set, file)
                    accident_sound.set_volume(sound_volume)
                if btn_minus_sound.rect.collidepoint(x, y):
                    if sound_volume > 0:
                        btn_minus_sound.playsound()
                        with open("JSONfiles\settings_save.json", "w") as file:
                            data_set["s_vol"] -= 0.1
                            sound_volume = data_set["s_vol"]
                            json.dump(data_set, file)
                        accident_sound.set_volume(sound_volume)
                if btn_plus_sound.rect.collidepoint(x, y):
                    if sound_volume < 1:
                        btn_plus_sound.playsound()
                        with open("JSONfiles\settings_save.json", "w") as file:
                            data_set["s_vol"] += 0.1
                            sound_volume = data_set["s_vol"]
                            json.dump(data_set, file)
                        accident_sound.set_volume(sound_volume)
                if btn_mute_music.rect.collidepoint(x, y):
                    btn_mute_music.playsound()
                    with open("JSONfiles\settings_save.json", "w") as file:
                        data_set["mus_vol"] = 0
                        music_volume = data_set["mus_vol"]
                        json.dump(data_set, file)
                    mixer.music.set_volume(music_volume)
                if btn_minus_music.rect.collidepoint(x, y):
                    if music_volume > 0:
                        btn_minus_music.playsound()
                        with open("JSONfiles\settings_save.json", "w") as file:
                            data_set["mus_vol"] -= 0.1
                            music_volume = data_set["mus_vol"]
                            json.dump(data_set, file)
                        mixer.music.set_volume(music_volume)
                if btn_plus_music.rect.collidepoint(x, y):
                    if music_volume < 1:
                        btn_plus_music.playsound()
                        with open("JSONfiles\settings_save.json", "w") as file:
                            data_set["mus_vol"] += 0.1
                            music_volume = data_set["mus_vol"]
                            json.dump(data_set, file)
                        mixer.music.set_volume(music_volume)
        w.blit(bg1, (0, 0))
        w.blit(settings_title, (150, 100))
        w.blit(sound_text, (200, 200))
        w.blit(music_text, (200, 400))
        btn_ex.blitbutton()
        btn_mute_sound.blitbutton()
        btn_minus_sound.blitbutton()
        btn_plus_sound.blitbutton()
        btn_mute_music.blitbutton()
        btn_minus_music.blitbutton()
        btn_plus_music.blitbutton()
    if screen == "records":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
        w.blit(bg1, (0, 0))
        btn_ex.blitbutton()
    if screen == "rules":
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if btn_ex.rect.collidepoint(x, y):
                    btn_ex.playsound()
                    screen = "menu"
        w.blit(bg1, (0, 0))
        btn_ex.blitbutton()
    c.tick(fps)
    display.update()