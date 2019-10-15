# -*- coding=utf-8 -*-
import pygame
import string
from threading import Thread
from widget import *
from req import *
import Thirteen_Poker
# from Queue import Queue
from threading import Thread

# q = Queue()



WHITE = (255, 255, 255)
GREEN = ( 0, 128, 128)
BLUE = ( 0, 0, 128)
BLACK = (0, 0, 0)


 
 # 文本
def Laber_draw(text, screen, x, y):
    font = pygame.font.SysFont('arial', 12)
    textSurfaceObj = font.render(text, True, (0, 0, 0))
    rect = textSurfaceObj.get_rect()
    rect.center = x,y
    screen.blit(textSurfaceObj,  rect)

def draw_card(screen, x, y, card_list=None ,card_dirt=None):
    i = 0
    n1 = x
    n2 = y
    if(card_list != None):
        for c in card_list:
            i += 1
            screen.blit(card_dirt[c], (n1,n2))
            n1 += 20
            if i == 3 or i == 8:
                n2 += 30
                n1 = x
    else:
        for c in range(13):
            i += 1
            pygame.draw.rect(screen,GREEN,[n1,n2,71,96])
            pygame.draw.rect(screen,BLACK,[n1,n2,71,96],2)
            n1 += 20
            if i == 3 or i == 8:
                n2 += 30
                n1 = x
        
def main():
    # init
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('十三水')
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    # 加载背景
    background = pygame.image.load('res/background.jpg')
    background_rank = pygame.image.load('res/rank.png')
    background_history = pygame.image.load('res/history.png')

    screen.blit(background, (0, 0))
    
    # 数据定义
    card = "*A *2 *K *3 *4 *5 *10 *6 *7 *8 *9 *J *Q"
    card_list = card.split(" ")
    rank_data = []
    history_data = []
    TL1 = TextList(rank_data, 174, 185, 5, 3, [130, 200, 124], 49, 1)
    TL2 = TextList(history_data, 69, 187, 5, 3, [131, 382, 131], 57, 2)
    TB1 = TextBox(250, 40, 336, 224)
    TB2 = TextBox(250, 40, 336, 280)

    # card img load
    card_dirt = {}          # 通过此字典访问img
    suites = {
        '$': 'spades',      # 黑桃
        '&': 'hearts',      # 红桃
        '*': 'clubs',       # 梅花
        '#': 'diamonds'     # 方块
    }
    faces = {'A': 'ace', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '10':'10', 'J': 'jack', 'Q': 'queen', 'K': 'king'}
    for suite in suites:
        for face in faces:
            key = suite + face
            res = 'res/cards/' + faces[face] + '_' + suites[suite] + '.png'
            img = pygame.image.load(res).convert()
            card_dirt[key] = img
    
    # button img load
    button_login = Button('res/buttons/login.png', 433, 420)
    button_register = Button('res/buttons/register.png', 228, 420)
    button_back = Button('res/buttons/back.png', 433, 420)
    button_back_2 = Button('res/buttons/back.png', 0, 0)
    button_open = Button('res/buttons/open.png', 300, 300)
    button_history_detail = Button('res/buttons/history_detail.png', 680, 78)
    button_history = Button('res/buttons/history.png', 680, 39)
    button_rank = Button('res/buttons/rank.png', 680, 0)
    button_login.draw(screen)
    button_register.draw(screen)
    button_b1 = Button('res/buttons/b.png', 210, 462)
    button_n1 = Button('res/buttons/n.png', 520, 462)
    button_b2 = Button('res/buttons/b.png', 196, 508)
    button_n2 = Button('res/buttons/n.png', 516, 508)
    # button_b3 = Button('res/buttons/b.png', 210, 462)
    # button_n3 = Button('res/buttons/n.png', 520, 462)
    
    # 控件打包
    page = [[] for _ in range(8)]

    page[1].append(button_login)
    page[1].append(button_register)
    page[1].append(TB1)
    page[1].append(TB2)

    page[2].append(button_back)
    page[2].append(button_register)
    page[2].append(TB1)
    page[2].append(TB2)

    page[3].append(button_open)

    page[4].append(button_history)
    page[4].append(button_rank)
    page[4].append(button_history_detail)

    page[5].append(button_back_2)
    page[5].append(button_b1)
    page[5].append(button_n1)
    page[5].append(TL1)

    page[6].append(button_back_2)
    page[6].append(button_b2)
    page[6].append(button_n2)
    page[6].append(TL2)

    page[7].append(button_back_2)
    # page[7].append(button_b3)
    # page[7].append(button_n3)
    current_page = 1
    pygame.display.flip()

    p1 = Player('te342d3', '12345678')

    # t = Thread(target=f)
    # t.daemon = True
    # t.start()

    

    running = True
    while running:

        # 从消息队列中获取事件并对事件进行处理
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                p1.logout()
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if current_page == 1:
                    mouse = pygame.mouse.get_pos()
                    if(TB1.pressed(mouse)):
                        TB1.key_down(event)
                    if(TB2.pressed(mouse)):
                        TB2.key_down(event)

            # 监控鼠标点击
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos() 
                
                # page 1
                if current_page == 1:
                    if button_login.pressed(mouse):
                        p1.login()
                        if p1.check_login_status():
                            current_page = 3
                    if button_register.pressed(mouse):
                        current_page = 2

                # page 2
                if current_page == 2:
                    if button_register.pressed(mouse):
                        pass
                    if button_back.pressed(mouse):
                        current_page = 1
                
                # page 3
                if current_page == 3:
                    if button_open.pressed(mouse):

                        card = p1.game_open()
                        card_list = card.split(" ")
                        p1.push = False
                        current_page = 4
                
                # page 4
                if current_page == 4:
                    if button_rank.pressed(mouse):
                        current_page = 5
                        rank_data = p1.get_rank()
                        TL1.update(0, rank_data)
                    if button_history.pressed(mouse):
                        current_page = 6
                        history_data = p1.get_history(5, 5, 1)
                        TL2.update(0, history_data)
                # page 5
                if current_page == 5:
                    if button_back_2.pressed(mouse):
                        current_page = 4
                    
                    if button_b1.pressed(mouse):
                        if TL1.p != 0:
                            TL1.update(TL1.p - 1)
                    if button_n1.pressed(mouse):
                        if((TL1.p + 1) * 5 <= len(rank_data) - 1 ):
                            TL1.update(TL1.p + 1)
                
                 # page 6
                if current_page == 6:
                    if button_back_2.pressed(mouse):
                        current_page = 4
                    
                    if button_b2.pressed(mouse):
                        if TL2.p != 0:
                            TL2.update(TL2.p - 1)
                    if button_n2.pressed(mouse):
                      if((TL2.p + 1) * 5 <= len(history_data) - 1 ):
                        TL2.update(TL2.p + 1)

                #  # page 7
                # if current_page == 7:
                #     if button_back_2.pressed(mouse):
                #         current_page = 4
                #     if button_b3.pressed(mouse):
                #         pass
                #     if button_n3.pressed(mouse):
                #         pass


            if event.type == pygame.MOUSEBUTTONUP:
                pass

        # display update
        if current_page == 1:
            screen.blit(background, (0, 0))
            for w in page[1]:
                w.draw(screen)
            Laber_draw('username: ',screen, 276,244)
            Laber_draw('password: ',screen, 276,300)
        
        elif current_page == 2:
            screen.blit(background, (0, 0))
            for w in page[2]:
                w.draw(screen)
            Laber_draw('username: ',screen, 276,244)
            Laber_draw('password: ',screen, 276,300)
        
        elif current_page == 3:
            screen.blit(background, (0, 0))
            for w in page[3]:
                w.draw(screen)
        
        elif current_page == 4:
            screen.blit(background, (0, 0))
            for w in page[4]:
                w.draw(screen)
            draw_card(screen, 300, 400, card_list, card_dirt)
            draw_card(screen, 400, 30)
            draw_card(screen, 30, 150)
            draw_card(screen, 600, 250)            

        elif current_page == 5:
            screen.blit(background_rank, (0, 0))
            for w in page[5]:
                w.draw(screen)
        
        elif current_page == 6:
            screen.blit(background_history, (0, 0))
            for w in page[6]:
                w.draw(screen)

        pygame.display.update()
        pygame.display.flip()
        if(current_page == 4 and p1.push == False):
                s = Thirteen_Poker.AI(card)
                p1.game_submit(s)
                p1.push = True
        clock.tick(20)

if __name__ == '__main__':
    main()