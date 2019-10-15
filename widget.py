import pygame

# 列表
class TextList():
    def __init__(self, data, x, y, limit, Column, w, h, flag,font=None):
        self.data = data
        self.x = x
        self.y = y
        self.limit = limit
        self.Column = Column
        self.w = w
        self.h = h
        self.p = 0
        self.surf = []
        self.rect = []
        self.flag = flag
        self.push = None
        if font is None:
            #self.font = pygame.font.Font(None, 32)  # 使用pygame自带字体
            self.font = pygame.font.SysFont('arial', 22)
        else:
            self.font = font
    
        for item in range(self.Column):
            self.surf.append(pygame.Surface((w[item], self.h)))
            self.surf[item].fill((255,255,255))
            self.surf[item].set_alpha(0)
        
    def update(self, p, data=None):
        self.p = p
        if data != None:
            self.data = data
    
    def draw(self,screen):
        if(self.flag == 1):
            Laber_draw(str(self.p + 1),screen, 398,482)
            
        else:
            Laber_draw(str(self.p + 1),screen, 390,527)
        y = self.y
        x = self.x
        index = self.p * self.limit
        for row in range(self.limit):
            x = self.x
            text = ""
            if(index > len(self.data) - 1 ):
                return 
            dirt = self.data[index]
            for item in range(self.Column):
                if self.flag ==  1:
                    if item == 0:
                        text = str(dirt["player_id"])
                    elif item == 1:
                        text = str(dirt["name"])
                    else:
                        text = str(dirt["score"])
                else:
                    if item == 0:
                        text = str(dirt["id"])
                    elif item == 1:
                        list = dirt["card"]
                        text = list[0] + '  ' + list[1] + '  ' + list[2]
                    else:
                        text = str(dirt["score"])
                if self.flag == 2 and item == 1:
                  font = pygame.font.SysFont('arial', 18)
                  text_surf = font.render(text, True, (0, 0, 0))
                else:
                  text_surf = self.font.render(text, True, (0, 0, 0))
                screen.blit(self.surf[item], (x, y))
                # if self.flag == 2 and item == 1:
                #   screen.blit(text_surf, (x , y + (self.h - text_surf.get_height())/2 ),
                #     (0, 0, self.w[item], self.h))
                # else:
                screen.blit(text_surf, (x + (self.w[item] - text_surf.get_width())/2 ,
                 y + (self.h - text_surf.get_height())/2 ),
                    (0, 0, self.w[item], self.h))
                x += self.w[item]
            y += self.h
            index += 1
 
# 按钮
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

    def draw(self, dest_surf):
        dest_surf.blit(self.surf, self.rect)

# 文本框
class TextBox():
    def __init__(self, w, h, x, y, font=None, callback=None):
        """
        :param w:文本框宽度
        :param h:文本框高度
        :param x:文本框坐标
        :param y:文本框坐标
        :param font:文本框中使用的字体
        :param callback:在文本框按下回车键之后的回调函数
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.text = ""  # 文本框内容
        self.callback = callback
        # 创建
        self.__surface = pygame.Surface((w, h))
        self.__surface.fill((255,255,255))
        self.__surface.set_alpha(200)
        self.rect = self.__surface.get_rect()
        self.rect.topleft = x,y
        if font is None:
            self.font = pygame.font.Font(None, 32)  # 使用pygame自带字体
        else:
            self.font = font
 
    def draw(self, dest_surf):
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        dest_surf.blit(self.__surface, (self.x, self.y))
        dest_surf.blit(text_surf, (self.x, self.y + (self.height - text_surf.get_height())/2 ),
                       (0, 0, self.width, self.height))
 
    def key_down(self, event):
        unicode = event.unicode
        key = event.key
 
        # 退位键
        if key == 8:
            self.text = self.text[:-1]
            return
        # 切换大小写键
        if key == 301:
            return
        # 回车键
        if key == 13:
            if self.callback is not None:
                self.callback()
            return
        if unicode != "":
            char = unicode
        else:
            char = chr(key)
 
        self.text += char

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
 
def callback():
    print("回车测试")
 
 
def main():
    # 英文文本框demo
    pygame.init()
    winSur = pygame.display.set_mode((640, 480))
    # 创建文本框
    text_box = TextBox(200, 30, 200, 200, callback=callback)
 
    # 游戏主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                mouse = pygame.mouse.get_pos()
                if(text_box.pressed(mouse)):
                    text_box.key_down(event)
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        pygame.time.delay(33)
        winSur.fill((0, 50, 0))
        text_box.draw(winSur)
        pygame.display.flip()
 
 
if __name__ == '__main__':
    main()
