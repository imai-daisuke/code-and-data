import pygame
from pygame.locals import *
import sys 
import random
import time
from pygame.time import Clock


speed_2 = 10
speed = 10
active = False
text = ''
answer = ''
(w, h) = (768,432)
done = 0
move = 0#none

def enemy(screen,x,y):
    enemy_size_w = 60
    enemy_size_h = 60
    enemy = pygame.image.load("data\monster.png")
    enemy = pygame.transform.scale(enemy,(enemy_size_w,enemy_size_h))
    screen.blit(enemy,(x,y))
    check = [x + enemy_size_w , y , x , y + enemy_size_h]
    return check


def redcoin(screen,x,y):
    coin_size_w = 60
    coin_size_h = 60
    redcoin = pygame.image.load("data\coin_red.png")
    redcoin = pygame.transform.scale(redcoin,(coin_size_w,coin_size_h))
    screen.blit(redcoin,(x,y))
    check = [x + coin_size_w , y , x , y + coin_size_h]
    return check


def bluecoin(screen,x,y):
    coin_size_w = 60
    coin_size_h = 60
    bluecoin = pygame.image.load("data\coin_blue.png")
    bluecoin = pygame.transform.scale(bluecoin,(coin_size_w,coin_size_h))
    screen.blit(bluecoin,(x,y))
    check = [x + coin_size_w , y , x , y + coin_size_h]
    return check


def greencoin(screen,x,y):
    coin_size_w = 60
    coin_size_h = 20
    greencoin = pygame.image.load("data\green.png")
    greencoin = pygame.transform.scale(greencoin,(coin_size_w,coin_size_h))
    screen.blit(greencoin,(x,y))
    check = [x + coin_size_w , y , x , y + coin_size_h]
    return check

def enemy_s(screen,x,y):
    enemy_size_w = 60
    enemy_size_h = 20
    enemy = pygame.image.load("data\monster.png")
    enemy = pygame.transform.scale(enemy,(enemy_size_w,enemy_size_h))
    screen.blit(enemy,(x,y))
    check = [x + enemy_size_w , y , x , y + enemy_size_h]
    return check

def generate(screen,x,y,g):
    check = []
    if g == 0:
        check = enemy(screen,x,y)
    elif g == 1:
        check = redcoin(screen,x,y)
    elif g == 2:
        check = bluecoin(screen,x,y)
    elif g == 3:
        check = greencoin(screen,x,y)
    elif g == 4:
        check = enemy_s(screen,x,y)
    return check

def helper_color(check,g1,x,y,player_size_w,player_size_h,check_p,r,g,b,h,help):
    if (min(check[0] , x + player_size_w) >= max(check[2] , x)) & (min(check[3] , y + player_size_h) >= max(check[1] , y)):
        global done
        done = 1
        if ((help == 3) and (random.random() <= 0.3)):
            if g1 == 1:
                (r,g,b) = (255,0,0)
                check_p = 1
            if g1 == 2:
                (r,g,b) = (0,0,255)
                check_p = 2
            if g1 == 3:
                (r,g,b) = (0,255,0)
                check_p = 3
                player_size_h = 60
                y = h - player_size_h
    return (r,g,b) , check_p , player_size_h , y , done


def move_checker(check1,check2,x,player_size_w,g1,g2):
    s = 0
    check_d = min(x - check1[0],x - check2[0]) 
    check_d2 = max(x - check1[0],x - check2[0])
    d1 = check1[2] - (x + player_size_w)
    d2 = check2[2] - (x + player_size_w)
    if (check_d < 0):
        if (d1 <= d2):
            if (d1 <= 40):
                s = 1
        else:
            if (d2 <= 40):
                s = 2
    else:
        s = 0
    if (check_d2 >= 0):
        if (s == 1) and ((g2 == 3) or (g2 ==2) or (g2 == 1)):
            s = 0
        elif (s == 2) and ((g1 == 3) or (g2 ==2) or (g2 == 1)):
            s = 0
    return s , d1 , d2


def helper_move(g1,g2,check1,check2,x,y,player_size_w,player_size_h,help):
    global move
    (s,d1,d2) = move_checker(check1,check2,x,player_size_w,g1,g2)
    if s == 0:
        move = 0
    if ((help == 3) and (random.random() <= 0.3)):
        if ((s == 1) and (g1 == 4)) or ((s ==2) and (g2 == 4)):
            move = 1
        #if (abs(d1-d2) < (player_size_h * 5)):
        if (s == 2) and (g2 == 0):
            if (g1 == 0):
                move =2
            else:
                move = 0
        elif (s == 2) and ((g2 == 4) or(g2 == 1) or (g2 == 2)):
            move = 1
        elif (s ==1):
            if (g1 == 0):
                if (g2 == 4) or (g2 == 1) or (g2 == 2):
                    move = 1
                elif (g2 ==3) or (g2 == 0):
                    move=2
    return move




def main():           
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    game_state = 2
    check1 = []
    check2 = []
    count = 0
    a=0.2
    score = 0
    red_counter = 0
    green_counter = 0
    blue_counter = 0
    global done
    global move
    (w, h) = (768,432)
    (r,g,b) = (255,255,255)
    jump = 200
    jump2 = 30
    player_size_w = 60
    player_size_h = 100
    crouch = player_size_h / 2
    default = player_size_h
    (x, y) = (60,h-player_size_h)
    pygame.display.set_mode((w, h), 0, 32)
    screen = pygame.display.get_surface()
    pygame.display.set_caption("Pygame")
    font = pygame.font.SysFont("Arial", 37)
    font_big = pygame.font.SysFont("Arial",90)
    font_small = pygame.font.SysFont("Arial",27)
    jfont = pygame.font.Font('data\姫明朝ともえごぜんmini.otf', 30)
    jfont2 = pygame.font.Font('data\姫明朝ともえごぜんmini.otf', 20)
    jfont3 = pygame.font.Font('data\姫明朝ともえごぜんmini.otf', 40)
    game1 = 0
    game2 = 0
    game3 = 0
    game4 = 0

    #g1 = random.randint(0,4) # 0 = enemy, 1 = redcoin, 2 = bluecoin, 3 = greencoin, 4 = smallenemy
    #g2 = random.randint(0,4)
    #while(g2 == g1):
    #    g2 = random.randint(0,4)
    #if g1 == 3 or g1 == 4:
    #    (g_x , g_y) = (w , 412)
    #else:
    #    (g_x , g_y) = (w , 300)
    
    #if g2 == 3 or g2 == 4:
    #    (g2_x , g2_y) = (w * 1.5 , 412)
    #else:
    #    (g2_x , g2_y) = (w * 1.5 , 130)
    
    while(True):
        pygame.event.pump()
        if game_state == 0:
            key = pygame.key.get_pressed()
            if (((key[K_SPACE]) & (y > 0) & (y >= ((h - player_size_h)- jump))) or move == 1):
                player_size_h = default
                y = (h - player_size_h) - jump
                #y = y - jump2#連続
            #elif y + player_size_h < h:
                #y = h - player_size_h
                #y = y + 10
            elif (((key[K_s]) and (y == h - player_size_h)) or move == 2):
                player_size_h = crouch
                y = h - player_size_h#連続
                (r,g,b) = (0,255,0)
                check_p = 3
            else:
                player_size_h = default
                y = h - player_size_h
            
            if key[K_SPACE]:
                player_size_h = default
                (r,g,b) = (255,255,255)
                check_p = 0

            if (key[K_q] == 1) & (key[K_e] == 0) & (key[K_s] == 0):
                (r,g,b) = (255,0,0)
                check_p = 1
            elif (key[K_e] == 0) & (key[K_s] == 0):
                (r,g,b) = (255,255,255)
                check_p = 0
            
            if (key[K_q] == 0) & (key[K_e] == 1) & (key[K_s] == 0):
                (r,g,b) = (0,0,255)
                check_p = 2
            elif (key[K_q] == 0) & (key[K_s] == 0):
                (r,g,b) = (255,255,255)
                check_p = 0
            
            global speed
            speed = speed_2 + count * a
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0,0,0))

            if (g_x <= 0):
                count += 1
                done = 0
                g_x = w
                g1 = random.randint(0,4)
                if (g2 == 0) and (g1 == 4):
                    g1 = random.randint(0,3)
                if g1 == 3 or g1 == 4:
                    (g_x , g_y) = (w , 412)
                else:
                    (g_x , g_y) = (w , 300)
            if (g_x > 0):
                g_x = g_x - speed
                check1 = generate(screen,g_x,g_y,g1)

                if done == 0:
                    (r,g,b) , check_p , player_size_h , y ,done= helper_color(check1,g1,x,y,player_size_w,player_size_h,check_p,r,g,b,h,help)

                if (min(check1[0] , x + player_size_w) >= max(check1[2] , x)) & (min(check1[3] , y + player_size_h) >= max(check1[1] , y)):
                    if g1 == 0 or g1 == 4:
                        pygame.mixer.music.load("data\Arcade-Action01-6(Impact).mp3")
                        pygame.mixer.music.play(1)
                        g_x = 0
                        game_state = 1
                    elif g1 == check_p:
                        pygame.mixer.music.load("data\Arcade-Action01-3(Score).mp3")
                        pygame.mixer.music.play(1)
                        count += 1
                        done = 0
                        g_x = 0
                        if g1 == 1:
                            score = score + 10
                            red_counter = red_counter + 1
                        elif g1 == 2:
                            score = score + 10
                            blue_counter = blue_counter + 1
                        elif g1 == 3:
                            score = score + 10
                            green_counter = green_counter + 1

            
            if (g2_x <= 0):
                count += 1
                done = 0
                g2_x = w
                g2 = random.randint(0,4)
                while (g1 == 0 or g1 == 4) and (g2 == 0 or g2 == 4):
                    g2 = random.randint(0,4)
                if g1 == 4:
                    g2 = random.randint(1,2)
                if g2 == 3 or g2 == 4:
                    (g2_x , g2_y) = (w , 412)
                else:
                    (g2_x , g2_y) = (w , 130)
                if (min((g2_x + 60) , check1[0]) >= max(g2_x , check1[2])) or (abs(g_x - g2_x) <= 120):
                    g2_x = g_x + 150
            if (g2_x > 0):
                g2_x = g2_x - speed
                check2 = generate(screen,g2_x,g2_y,g2)
                
                if done == 0:
                    (r,g,b) , check_p ,player_size_h , y, done= helper_color(check2,g2,x,y,player_size_w,player_size_h,check_p,r,g,b,h,help)

                if (min(check2[0] , x + player_size_w) >= max(check2[2] , x)) & (min(check2[3] , y + player_size_h) >= max(check2[1] , y)):
                    if g2 == 0 or g2 == 4:
                        pygame.mixer.music.load("data\Arcade-Action01-6(Impact).mp3")
                        pygame.mixer.music.play(1)
                        g2_x = 0
                        game_state = 1
                    elif g2 == check_p:
                        pygame.mixer.music.load("data\Arcade-Action01-3(Score).mp3")
                        pygame.mixer.music.play(1)
                        count += 1
                        done = 0
                        g2_x = 0
                        if g2 == 1:
                            score = score + 10
                            red_counter = red_counter + 1
                        elif g2 == 2:
                            score = score + 10
                            blue_counter = blue_counter + 1
                        elif g2 == 3:
                            score = score + 10
                            green_counter = green_counter + 1

            move = helper_move(g1,g2,check1,check2,x,y,player_size_w,player_size_h,help)
            
            text_test = font.render("score:{:2d}".format(score), True, (255,255,255), (0,0,0))
            control = font.render("Red:Q  Blue:E", True, (255,255,255), (0,0,0))
            control2 = font.render("jump:space  green:S", True, (255,255,255), (0,0,0))
            screen.blit(text_test,(0,0))
            screen.blit(control,(540,0))
            screen.blit(control2,(480,50))
            pygame.draw.rect(screen, (r,g,b), (x,y,player_size_w,player_size_h))
        
        if game_state == 1:# gameover
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0,0,0))
            gameover = font_big.render("GAMEOVER!!" , True , (255,0,0), (0,0,0))
            guid = font.render(" Press Enter ", True , (255 , 255 ,255),(0,0,0))
            screen.blit(gameover,(w/2 - 220 , 70))
            screen.blit(text_test,(w/2 - 85,200))
            screen.blit(guid,(w/2 - 95, 300))
            key = pygame.key.get_pressed()
            if key[K_RETURN]:
                game_state = 3
                count = 0
        
        if game_state == 2: #start
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            key = pygame.key.get_pressed()
            screen.fill((0,0,0))
            start = font_big.render("GAME START" , True , (50,255,50), (0,0,0))
            select = font_small.render("press 1" , True , (255,255,255), (0,0,0))
            screen.blit(start, (w/2 - 220,70))
            screen.blit(select, (w/2 - 50,250))
            if key[K_1]:
                done = 0
                g1 = random.randint(0,4) # 0 = enemy, 1 = redcoin, 2 = bluecoin, 3 = greencoin, 4 = smallenemy
                g2 = random.randint(0,4)
                while(g2 == g1):
                    g2 = random.randint(0,4)
                if g1 == 3 or g1 == 4:
                    (g_x , g_y) = (w , 412)
                else:
                    (g_x , g_y) = (w , 300)
                
                if g2 == 3 or g2 == 4:
                    (g2_x , g2_y) = (w * 1.5 , 412)
                else:
                    (g2_x , g2_y) = (w * 1.5 , 130)
                if (game1 == 0):
                    game_state = 0
                    help = 1
                    game1 = 1
                elif (game2 == 0):
                    game_state = 0
                    help = 2
                    game2 = 1
                elif (game3 == 0):
                    game_state = 0
                    help = 3
                    game3 = 1
                elif (game4 == 0):
                    game_state = 0
                    help = 4
                    game4 = 1
                else:
                    game_state = 4
            '''
            if key[K_1]:
                game_state = 0
                help = 1
                done = 0
                g1 = random.randint(0,4) # 0 = enemy, 1 = redcoin, 2 = bluecoin, 3 = greencoin, 4 = smallenemy
                g2 = random.randint(0,4)
                while(g2 == g1):
                    g2 = random.randint(0,4)
                if g1 == 3 or g1 == 4:
                    (g_x , g_y) = (w , 412)
                else:
                    (g_x , g_y) = (w , 300)
                
                if g2 == 3 or g2 == 4:
                    (g2_x , g2_y) = (w * 1.5 , 412)
                else:
                    (g2_x , g2_y) = (w * 1.5 , 130)
            if key[K_2]:
                game_state = 0
                help = 2
                done = 0
                g1 = random.randint(0,4) # 0 = enemy, 1 = redcoin, 2 = bluecoin, 3 = greencoin, 4 = smallenemy
                g2 = random.randint(0,4)
                while(g2 == g1):
                    g2 = random.randint(0,4)
                if g1 == 3 or g1 == 4:
                    (g_x , g_y) = (w , 412)
                else:
                    (g_x , g_y) = (w , 300)
                
                if g2 == 3 or g2 == 4:
                    (g2_x , g2_y) = (w * 1.5 , 412)
                else:
                    (g2_x , g2_y) = (w * 1.5 , 130)
            if key[K_3]:
                game_state = 0
                help = 3
                done = 0
                g1 = random.randint(0,4) # 0 = enemy, 1 = redcoin, 2 = bluecoin, 3 = greencoin, 4 = smallenemy
                g2 = random.randint(0,4)
                while(g2 == g1):
                    g2 = random.randint(0,4)
                if g1 == 3 or g1 == 4:
                    (g_x , g_y) = (w , 412)
                else:
                    (g_x , g_y) = (w , 300)
                
                if g2 == 3 or g2 == 4:
                    (g2_x , g2_y) = (w * 1.5 , 412)
                else:
                    (g2_x , g2_y) = (w * 1.5 , 130)
            if key[K_4]:
                game_state = 0
                help = 4
                g1 = random.randint(0,4) # 0 = enemy, 1 = redcoin, 2 = bluecoin, 3 = greencoin, 4 = smallenemy
                g2 = random.randint(0,4)
                while(g2 == g1):
                    g2 = random.randint(0,4)
                if g1 == 3 or g1 == 4:
                    (g_x , g_y) = (w , 412)
                else:
                    (g_x , g_y) = (w , 300)
                
                if g2 == 3 or g2 == 4:
                    (g2_x , g2_y) = (w * 1.5 , 412)
                else:
                    (g2_x , g2_y) = (w * 1.5 , 130)
            '''

        if game_state == 3:
            input_box = pygame.Rect(w/2 -120, 240, 140, 32)
            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            box_color = color_inactive
            global active
            global text

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    box_color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if text.isdecimal():
                                if (int(text) >= 0) and (int(text) <= 10):
                                    f = open('survey1_C.txt' , 'a')
                                    f.write("survey{} : {}  ".format(help,text))
                                    f.write("score : {}  {} {} {}\n".format(score,red_counter,green_counter,blue_counter))
                                    f.close()
                                    text = ''
                                    score = 0
                                    red_counter = 0
                                    green_counter = 0
                                    blue_counter = 0
                                    game_state = 2
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            key = pygame.key.get_pressed()
            screen.fill((0,0,0))
            survey = jfont.render("思い通りに操作できましたか",True,(255,255,255),(0,0,0))
            survey2 = jfont2.render("まったく思い通りにならない　　完全に思い通りに動かせた",True,(255,255,255),(0,0,0))
            survey3 = font.render("0               ~                 10",True,(255,255,255),(0,0,0))
            txt_surface = font.render(text, True, box_color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            screen.blit(survey,(w/2 - 220, 70))
            screen.blit(survey2,(w/2 - 300, 130))
            screen.blit(survey3,(w/2 - 150, 160))
            pygame.draw.rect(screen, box_color, input_box, 2)
            screen.blit(txt_surface, (input_box.x+5, input_box.y-3))
        pygame.display.update()
        clock.tick(40)
        #pygame.time.wait(5) 

        if game_state == 4:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0,0,0))
            announce = jfont2.render("このゲームは終わりです.次のゲームに移行してください",True,(255,255,255),(0,0,0))
            screen.blit(announce,(w/2 - 250, 180))

if __name__ == "__main__":
    main()
