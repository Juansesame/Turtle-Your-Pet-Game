# -*- coding: utf-8 -*-

import pygame
import sys
import random
import math
import webbrowser

pygame.init()
pygame.mixer.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turtle Your Pet")

clock = pygame.time.Clock()

WHITE=(255,255,255)
BLACK=(0,0,0)
UI=(240,240,240)
BORDER=(160,160,160)

BAR_BG=(30,30,30)
LIFE_COLOR=(255,80,80)
HAPPY_COLOR=(255,200,0)

font=pygame.font.SysFont(None,36)
smallfont=pygame.font.SysFont(None,18)

# hidden dev signature
dev_signature = "Original Developer: Juan Sebastian Salamanca Melo"

# AUDIO
background_music = pygame.mixer.Sound("backgroundmp3.mp3")
death_sound = pygame.mixer.Sound("deathmp3.mp3")
shock_sound = pygame.mixer.Sound("shockmp3.mp3")

background_music.set_volume(0.4)
death_sound.set_volume(0.35)
shock_sound.set_volume(1.0)

# BACKGROUNDS
background=pygame.image.load("ocean.png")
background=pygame.transform.scale(background,(WIDTH,HEIGHT))

homepage=pygame.image.load("homepage.png")
homepage=pygame.transform.scale(homepage,(WIDTH,HEIGHT))

# TURTLES
turtle1=pygame.image.load("turtlepng.png")
turtle2=pygame.image.load("turtle2png.png")
turtle3=pygame.image.load("turtle3png.png")
turtle4=pygame.image.load("turtle4png.png")

turtle1=pygame.transform.scale(turtle1,(220,220))
turtle2=pygame.transform.scale(turtle2,(220,220))
turtle3=pygame.transform.scale(turtle3,(220,220))
turtle4=pygame.transform.scale(turtle4,(220,220))

# HOOK
hook=pygame.image.load("hookpng.png")
hook=pygame.transform.scale(hook,(180,180))

hook_y=-200
hook_speed=6
hook_state="idle"

# ACCESSORIES
hat_img=pygame.image.load("hatpng.png")
hair_img=pygame.image.load("hairpng.png")
necklace_img=pygame.image.load("necklacepng.png")

hat=pygame.transform.scale(hat_img,(120,50))
hair=pygame.transform.scale(hair_img,(200,120))
necklace=pygame.transform.scale(necklace_img,(80,60))

hat_icon=pygame.transform.scale(hat_img,(60,25))
hair_icon=pygame.transform.scale(hair_img,(80,50))
necklace_icon=pygame.transform.scale(necklace_img,(40,30))

# MENU ICONS
shirt_icon=pygame.image.load("shirtpng.png")
burger_icon=pygame.image.load("burgerpng.png")
ball_icon=pygame.image.load("ballpng.png")
umbrella_icon=pygame.image.load("umbrellapng.png")

shirt_icon=pygame.transform.scale(shirt_icon,(50,50))
burger_icon=pygame.transform.scale(burger_icon,(50,50))
ball_icon=pygame.transform.scale(ball_icon,(50,50))
umbrella_icon=pygame.transform.scale(umbrella_icon,(50,50))

# FOOD
fish=pygame.image.load("fishpng.png")
kelp=pygame.image.load("Kelpng.png")
matcha=pygame.image.load("matchapng.png")

fish=pygame.transform.scale(fish,(70,70))
kelp=pygame.transform.scale(kelp,(70,70))
matcha=pygame.transform.scale(matcha,(70,70))

# UI ICONS
heart_img=pygame.image.load("heartpng.png")
happy_img=pygame.image.load("happypng.png")

heart_img=pygame.transform.scale(heart_img,(35,35))
happy_img=pygame.transform.scale(happy_img,(35,35))

bubble=pygame.image.load("bubble.png")
bubble=pygame.transform.scale(bubble,(70,70))
bubble_rect=bubble.get_rect()

bottom_bar=pygame.Rect(0,510,WIDTH,90)
menu_bar=pygame.Rect(210,400,480,95)

def make_btn(x):
    return pygame.Rect(x,525,70,70)

shirt_btn=make_btn(250)
burger_btn=make_btn(350)
ball_btn=make_btn(450)
umbrella_btn=make_btn(550)

hat_btn=pygame.Rect(260,415,90,70)
hair_btn=pygame.Rect(405,415,90,70)
necklace_btn=pygame.Rect(550,415,90,70)

fish_btn=pygame.Rect(260,415,90,70)
kelp_btn=pygame.Rect(405,415,90,70)
matcha_btn=pygame.Rect(550,415,90,70)

start_btn=pygame.Rect(350,420,200,60)
restart_btn=pygame.Rect(330,360,240,60)
home_btn=pygame.Rect(330,440,240,60)
link_btn=pygame.Rect(250,200,400,50)

game_state="home"
menu="room"

wear_hat=False
wear_hair=False
wear_necklace=False

fish_used=False
kelp_used=False
matcha_used=False

life=100
happiness=100

bubble_score=0
time=0

did_accessories=False
did_feed=False
did_play=False

turtle_x=WIDTH//2-120
turtle_y=210

turtle_up_y=0
rise_speed=4

fade_alpha=0
fade_active=False

message=""
message_timer=0

def show_message(text):
    global message,message_timer
    message=text
    message_timer=pygame.time.get_ticks()

def draw_message():
    if message!="":
        if pygame.time.get_ticks()-message_timer < 5000:
            msg=font.render(message,True,(0,30,60))
            x = WIDTH//2 - msg.get_width()//2
            y = 70
            screen.blit(msg,(x,y))

def draw_watermark():
    wm_font = pygame.font.SysFont(None,18)
    text = wm_font.render(
        "Juan Sebastian Salamanca Melo ©",
        True,
        (209,209,209)
    )
    text.set_alpha(110)
    screen.blit(text,(10,HEIGHT-20))

def new_bubble_position():
    return (random.randint(50,850),random.randint(120,450))

bubble_rect.topleft=new_bubble_position()

def draw_icon(img,rect,enabled):
    icon=img.copy()
    if not enabled:
        icon.set_alpha(80)
    x=rect.x+rect.width//2-img.get_width()//2
    y=rect.y+rect.height//2-img.get_height()//2-10
    screen.blit(icon,(x,y))

def draw_text(text,rect):
    txt=smallfont.render(text,True,BLACK)
    x=rect.x+rect.width//2-txt.get_width()//2
    y=rect.y+rect.height-15
    screen.blit(txt,(x,y))

def reset_game():
    global life,happiness,wear_hat,wear_hair,wear_necklace
    global fish_used,kelp_used,matcha_used
    global bubble_score,menu,game_state
    global did_accessories,did_feed,did_play
    global hook_y,hook_state,turtle_up_y,fade_alpha,fade_active

    background_music.play(-1)

    life=100
    happiness=100

    wear_hat=False
    wear_hair=False
    wear_necklace=False

    fish_used=False
    kelp_used=False
    matcha_used=False

    bubble_score=0

    hook_y=-200
    hook_state="idle"

    turtle_up_y=0

    fade_alpha=0
    fade_active=False

    did_accessories=False
    did_feed=False
    did_play=False

    menu="room"
    game_state="game"

while True:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_j]:
        print(dev_signature)

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN:

            m=event.pos

            if game_state=="home":
                if start_btn.collidepoint(m):
                    reset_game()

            elif game_state=="game":

                if menu=="room":

                    if shirt_btn.collidepoint(m):
                        menu="accessories"

                    elif burger_btn.collidepoint(m) and did_accessories:
                        menu="feed"

                    elif ball_btn.collidepoint(m) and did_feed:
                        menu="play"
                        show_message("Pop his oxygen bubbles!")

                    elif umbrella_btn.collidepoint(m) and did_play:
                        background_music.stop()
                        hook_state="descending"
                        game_state="ending"

                elif menu=="accessories":

                    if hat_btn.collidepoint(m):
                        wear_hat=not wear_hat
                        did_accessories=True
                        show_message("Shelly you look radiant!")

                    elif hair_btn.collidepoint(m):
                        wear_hair=not wear_hair
                        did_accessories=True
                        show_message("Shelly you look stunning!")

                    elif necklace_btn.collidepoint(m):
                        wear_necklace=not wear_necklace
                        did_accessories=True
                        show_message("Shelly you look gorgeous!")

                    elif bottom_bar.collidepoint(m):
                        menu="room"

                elif menu=="feed":

                    if fish_btn.collidepoint(m) and not fish_used:
                        fish_used=True
                        did_feed=True
                        show_message("Shelly enjoyed the fish!")

                    elif kelp_btn.collidepoint(m) and not kelp_used:
                        kelp_used=True
                        did_feed=True
                        show_message("Shelly liked the kelp!")

                    elif matcha_btn.collidepoint(m) and not matcha_used:
                        matcha_used=True
                        did_feed=True
                        show_message("Shelly loved the plastic cup!")

                    elif bottom_bar.collidepoint(m):
                        menu="room"

                elif menu=="play":

                    if bubble_rect.collidepoint(m):
                        bubble_score+=1
                        did_play=True
                        bubble_rect.topleft=new_bubble_position()

                    if bottom_bar.collidepoint(m):
                        menu="room"

            elif game_state=="credits":

                if restart_btn.collidepoint(m):
                    reset_game()

                if home_btn.collidepoint(m):
                    game_state="home"

                if link_btn.collidepoint(m):
                    webbrowser.open_new("https://1081221-d8f87f9f0f3e4d8da729a89ec727d8bb-v5-dev.dev.atoms.dev")

    if game_state=="home":

        screen.blit(homepage,(0,0))

        pygame.draw.rect(screen,UI,start_btn,border_radius=10)
        txt=font.render("START GAME",True,BLACK)
        screen.blit(txt,(370,435))

    elif game_state=="game":

        life=max(0,life-0.02)
        happiness=max(0,happiness-0.03)

        screen.blit(background,(0,0))

        time+=0.05
        turtle_y=210+math.sin(time)*6

        if matcha_used:
            turtle_current=turtle3
        elif did_accessories:
            turtle_current=turtle2
        else:
            turtle_current=turtle1

        screen.blit(turtle_current,(turtle_x,turtle_y))

        if wear_hat:
            screen.blit(hat,(turtle_x+51,turtle_y-32))

        if wear_hair:
            screen.blit(hair,(turtle_x+10,turtle_y-1))

        if wear_necklace:
            screen.blit(necklace,(turtle_x+71,turtle_y+105))

        draw_message()

        if menu=="accessories":

            pygame.draw.rect(screen,UI,menu_bar,border_radius=15)
            pygame.draw.rect(screen,BORDER,menu_bar,3,border_radius=15)

            draw_icon(hat_icon,hat_btn,True)
            draw_icon(hair_icon,hair_btn,True)
            draw_icon(necklace_icon,necklace_btn,True)

            draw_text("Cute hat",hat_btn)
            draw_text("Stylish braids",hair_btn)
            draw_text("Fancy necklace",necklace_btn)

        elif menu=="feed":

            pygame.draw.rect(screen,UI,menu_bar,border_radius=15)
            pygame.draw.rect(screen,BORDER,menu_bar,3,border_radius=15)

            draw_icon(fish,fish_btn,not fish_used)
            draw_icon(kelp,kelp_btn,not kelp_used)
            draw_icon(matcha,matcha_btn,not matcha_used)

            draw_text("Yummy fish",fish_btn)
            draw_text("Fresh kelp",kelp_btn)
            draw_text("Delicious juice!",matcha_btn)

        elif menu=="play":

            screen.blit(bubble,bubble_rect)

            score=font.render("Bubbles: "+str(bubble_score),True,WHITE)
            screen.blit(score,(380,120))

        pygame.draw.rect(screen,BAR_BG,(20,20,200,18))
        pygame.draw.rect(screen,LIFE_COLOR,(20,20,life*2,18))
        screen.blit(heart_img,(230,10))

        pygame.draw.rect(screen,BAR_BG,(20,65,200,18))
        pygame.draw.rect(screen,HAPPY_COLOR,(20,65,happiness*2,18))
        screen.blit(happy_img,(230,55))

        pygame.draw.rect(screen,UI,bottom_bar)
        pygame.draw.rect(screen,BORDER,bottom_bar,3)

        draw_icon(shirt_icon,shirt_btn,True)
        draw_icon(burger_icon,burger_btn,did_accessories)
        draw_icon(ball_icon,ball_btn,did_feed)
        draw_icon(umbrella_icon,umbrella_btn,did_play)

        draw_text("Accessories",shirt_btn)
        draw_text("Food",burger_btn)
        draw_text("Play",ball_btn)
        draw_text("Beach time!",umbrella_btn)

    elif game_state=="ending":

        screen.blit(background,(0,0))

        hook_x=turtle_x+40

        if hook_state=="descending":

            hook_y+=hook_speed

            screen.blit(turtle3,(turtle_x,260))
            screen.blit(hook,(hook_x,hook_y))

            if hook_y>=260:
                death_sound.play()
                shock_sound.play()
                hook_state="caught"
                turtle_up_y=260

        elif hook_state=="caught":

            turtle_up_y-=rise_speed
            hook_y-=rise_speed

            screen.blit(hook,(hook_x,hook_y))
            screen.blit(turtle4,(turtle_x,turtle_up_y))

            if turtle_up_y<50:
                fade_active=True

        if fade_active:

            fade=pygame.Surface((WIDTH,HEIGHT))
            fade.fill((0,0,0))
            fade.set_alpha(fade_alpha)

            screen.blit(fade,(0,0))

            fade_alpha+=4

            if fade_alpha>=255:
                game_state="credits"

    elif game_state=="credits":

        screen.fill(BLACK)

        text=font.render("Human actions harm marine life.",True,WHITE)
        screen.blit(text,(260,120))

        pygame.draw.rect(screen,UI,link_btn,border_radius=8)
        link_text=smallfont.render("Learn more about ocean protection (click here)",True,BLACK)
        screen.blit(link_text,(WIDTH//2-link_text.get_width()//2,215))

        pygame.draw.rect(screen,UI,restart_btn,border_radius=10)
        pygame.draw.rect(screen,UI,home_btn,border_radius=10)

        screen.blit(font.render("RESTART",True,BLACK),(400,375))
        screen.blit(font.render("HOME",True,BLACK),(420,455))

    draw_watermark()

    pygame.display.update()
    clock.tick(60)
    
    
    
    
    
    
    
    
"""
Developer Signature:
Juan Sebastian Salamanca Melo
Project: Turtle Your Pet
Build ID: JS-SHELLY-2026
"""