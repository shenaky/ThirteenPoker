import pygame

class Button():
    def __init__(self, img, x, y):
        self.surf = pygame.image.load(img).convert()
        self.rect = self.surf.get_rect()
        self.rect.topleft = x,y

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('十三水')
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()
    background = pygame.image.load('res/background.jpg')
    rect = background.get_rect()
    rect.topleft = 0,50
    screen.blit(background, background.get_rect())
    '''
    $ 黑桃 spade
    & 红桃 heart
    * 梅花 club
    # 方块 diamond
    '''
    suites = {
        '$': 'spades',
        '&': 'hearts',
        '*': 'clubs',
        '#': 'diamonds'
    }
    faces = {
        'A': 'ace',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '9',
        '10':'10',
        'J': 'jack',
        'Q': 'queen',
        'K': 'king'
    }
    card_dirt = {}
    for suite in suites:
        for face in faces:
            key = suite + face
            res = 'res/cards/' + faces[face] + '_' + suites[suite] + '.png'
            img = pygame.image.load(res).convert()
            card_dirt[key] = img
    # button 
    button_login = Button('res/buttons/login.png', 300, 500)
    button_register = Button('res/buttons/register.png', 300, 500)
    button_back = Button('res/buttons/back.png', 300, 500)
    button_login = Button('res/buttons/login.png', 300, 500)
    button_login = Button('res/buttons/login.png', 300, 500)
    button_dirt = {}
    screen.blit(button_login.surf, button_login.get_rect())
    n = 200
    for card in card_dirt:
        screen.blit(card_dirt[card], (n, 400))
        n = n + 30
    pygame.display.flip()

    running = True
    while running:

        for event in pygame.event.get(): # 从消息队列中获取事件并对事件进行处理
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos() #鼠标坐标
                if button_login.pressed(mouse):
                    print ('button hit')
            
            if event.type == pygame.MOUSEBUTTONUP:
                pass

        
        clock.tick(20)

if __name__ == '__main__':
    main()