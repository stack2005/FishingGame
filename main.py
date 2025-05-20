# -*- coding: utf-8 -*-  # 新增编码声明
import pygame,sys
from cannon import Cannon
from fish import Fish, get_fish_detail
from number import Number
from switchButton import SwitchButton


pygame.init()

pygame.display.set_caption('fish')

bg=pygame.image.load('images/BG3.jpg')
introduce_bg = pygame.image.load('images/bg.jpg')
intro_bg = pygame.image.load('images/02.png')
bar=pygame.image.load('images/bottom-bar.png')
start_bg=pygame.image.load('images/startbg.jpg')
tt_bg=pygame.image.load('images/text.png')
pause=pygame.image.load('images/pause.png')


screen=pygame.display.set_mode((1024,768))

cannon = Cannon()
number=Number()
fishlist=[]
switchButton=SwitchButton()
score=5000

def main():
    PAUSE=False
    global score
    ##随机定时产生鱼，即设置一个事件定时器
    PRODUCT_FISH_EVENT=pygame.USEREVENT+1
    pygame.time.set_timer(PRODUCT_FISH_EVENT,3000)
    fps=60

    tClock=pygame.time.Clock()

    while 1:


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            if event.type==PRODUCT_FISH_EVENT:
                fish = Fish()
                fishlist.append(fish)
            if event.type==pygame.KEYDOWN:
                if event.key==27:
                    PAUSE=not PAUSE
            if event.type==pygame.MOUSEBUTTONDOWN:
                mouse=pygame.mouse.get_pressed()
                if mouse[0]:
                    ###enemtlist就是fishlist
                    switchButton.hit(cannon)
                    if not switchButton.isHit:
                        cannon.shot(fishlist)
                        ##射击扣减根据炮弹不同。
                        score-=cannon.key
                    if PAUSE:
                        x,y=pygame.mouse.get_pos()
                        if 460 <= x <= 757 and 253 <= y <= 340:
                            PAUSE=not PAUSE
                        if 460 <= x <= 757 and 395 <= y <= 484:
                            start()
                        if 460 <= x <= 757 and 536 <= y <= 619:
                            quit()

            if event.type==pygame.MOUSEBUTTONUP:
                switchButton.back()


        if not PAUSE:
            screen.blit(bg, (0, 0))
            screen.blit(bar, ((bg.get_width() - bar.get_width()) / 2, bg.get_height() - bar.get_height()))

            cannon.display(screen)
            cannon.rotate()
            for bullet in cannon.bulletlist:
                bullet.display(screen)
                if bullet.isDestory:
                    cannon.bulletlist.remove(bullet)


            for fish in fishlist:
                fish.display(screen)
                fish.move()
                if fish.isAttack:
                    fish.net.display(screen)
                    fish.cointext.display(screen)
                    fish.coin.display(screen)
                if fish.isDestory:
                    fishlist.remove(fish)
                ##捕获鱼增加分数
                if fish.isAttack and fish.isDestory:
                    score+=(fish.reward*fish.bshape)

            # print(fishlist)
            number.display(screen,score)
            switchButton.display(screen)

            tClock.tick(fps)
        else:
            screen.blit(pause, (0, 0))
        pygame.display.update()

def start():
    BLUE_GRADIENTS = [
        (8, 24, 44),      # 深海军蓝
        (15, 82, 186),    # 宝石蓝
        (31, 117, 254),   # 亮钴蓝
        (100, 147, 242),  # 天空蓝
        (72, 209, 204),   # 绿松石蓝
        (135, 206, 235),  # 浅天蓝
        (174, 217, 224),  # 冰蓝
        (207, 231, 244)   # 淡雪花青
    ]

    while 1:
        screen.blit(start_bg,(0,0))
        tt_rect = pygame.Rect(80, 80, 298, 74)
        screen.blit(tt_bg, tt_rect)
        button_rect = pygame.Rect(360, 360, 298, 74)
        intro_btn = pygame.Rect(360, 520, 298, 74)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)

        # 绘制渐变背景
        for i in range(button_rect.height):
            # 根据悬停状态调整亮度
            color_index = int((i / button_rect.height) * (len(BLUE_GRADIENTS)-1))
            base_color = BLUE_GRADIENTS[color_index]
            final_color = tuple(min(c + 30 if is_hover else c, 255) for c in base_color)

            pygame.draw.line(screen, final_color,
                           (button_rect.left, button_rect.top + i),
                           (button_rect.right, button_rect.top + i))

        # 绘制intro按钮
        for i in range(intro_btn.height):
            # 根据悬停状态调整亮度
            color_index = int((i / intro_btn.height) * (len(BLUE_GRADIENTS)-1))
            base_color = BLUE_GRADIENTS[color_index]
            final_color = tuple(min(c + 30 if is_hover else c, 255) for c in base_color)

            pygame.draw.line(screen, final_color,
                           (intro_btn.left, intro_btn.top + i),
                           (intro_btn.right, intro_btn.top + i))


        # 添加按钮文字
        font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 48)
        text1 = font.render("start game", True, (255, 255, 255))
        text2 = font.render("introduction", True, (255, 255, 255))
        text1_rect = text1.get_rect(center=button_rect.center)
        text2_rect = text2.get_rect(center=intro_btn.center)
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    if button_rect.collidepoint(event.pos):
                        main()
                    elif intro_btn.collidepoint(event.pos):
                        introduce()  # 调用介绍页面函数
        pygame.display.flip()


def introduce():
    # 鱼类数据加载
    fish_types = [
        {'id': 1, 'name': '林星宇', 'img': 'fishi1.png'},
        {'id': 2, 'name': 'fish2', 'img': 'fishi2.png'},
        {'id': 3, 'name': 'fish2', 'img': 'fishi3.png'},
        {'id': 4, 'name': 'fish2', 'img': 'fishi4.png'},
        {'id': 5, 'name': 'fish2', 'img': 'fishi5.png'},
        {'id': 6, 'name': 'fish2', 'img': 'fishi6.png'},
        {'id': 7, 'name': 'fish2', 'img': 'fishi7.png'},
        {'id': 8, 'name': 'fish2', 'img': 'fishi8.png'},
        {'id': 9, 'name': 'fish2', 'img': 'fishi9.png'},

    ]

    while True:
        screen.blit(introduce_bg, (0, 0))

        # 网格布局展示鱼类
        for i, fish in enumerate(fish_types):
            x = 100 + (i % 3) * 300
            y = 100 + (i // 3) * 200
            btn = pygame.Rect(x, y, 200, 150)

            # 绘制带悬停效果的鱼图标
            if btn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (0, 150, 255), btn, border_radius=8)

            # 加载并绘制鱼图标
            icon = pygame.image.load(f'images/{fish["img"]}')
            screen.blit(icon, (x + 10, y + 10))

            # 显示基础信息
            font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 24)
            text = font.render(f'{fish["name"]}', True, (255, 255, 255))
            screen.blit(text, (x, y + 130))

            # 返回按钮
            back_btn = pygame.Rect(50, 50, 100, 40)
            if back_btn.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (200, 0, 0), back_btn)
            font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
            screen.blit(font.render("返回", True, (255,125,36)), (60, 55))

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, fish in enumerate(fish_types):
                    btn = pygame.Rect(100 + (i % 3) * 300, 100 + (i // 3) * 200, 200, 150)
                    if btn.collidepoint(event.pos):
                        fish_detail(fish['id'])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start()

        pygame.display.flip()


def fish_detail(fish_type):
    # 根据类型加载详细数据
    detail = get_fish_detail(fish_type)  # 需要实现的鱼类数据获取方法

    while True:
        screen.blit(intro_bg, (0, -100))

        # 显示大图和信息面板
        big_img = pygame.image.load(f'images/fishi{fish_type}.png')
        screen.blit(big_img, (300, 350))

        # 绘制信息文字
        font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
        lines = [
            f"名称: {detail['name']}",
            f"血量: {detail['hp']}",
            f"出现条件: {detail['condition']}",
            f"详细描述: {detail['desc']}"
        ]
        y_offset = 250
        for line in lines:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (500, y_offset))
            y_offset += 50

        # 返回按钮
        back_btn = pygame.Rect(50, 50, 100, 40)
        if back_btn.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (200, 0, 0), back_btn)
        font = pygame.font.Font('C:/Windows/Fonts/simhei.ttf', 28)
        screen.blit(font.render("返回", True, (255, 255, 255)), (60, 55))

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()


if __name__ == '__main__':
    start()
