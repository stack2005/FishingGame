# *_* coding : UTF-8 *_*

import pygame
import random
import pandas as pd

data=[
    # 格式: (宽度, 高度, 动画帧数, 生存帧数, 基础分值, 血量)
    (55,296,8,4,1,1),   # 1号鱼 血量1
    (78,512,8,4,3,2),   # 2号鱼 血量2
    (72,448,8,4,5,3),   # 3号鱼 血量3
    (77,472,8,4,8,4),   # 4号鱼 血量4
    (107,976,8,4,10,5), # 5号鱼 血量5
    (105,948,12,8,20,6),
    (92,1510,10,6,30,7),
    (174,1512,12,8,40,8),
    (166,2196,12,8,50,9),
    (178,1870,10,6,100,10)  # 10号鱼 血量10
]

fish_details = {
    1: {
        'name': '小丑鱼',
        'condition': '初级海域出现',
        'hp': 1,
        'desc': '行动缓慢，适合新手练习'
    },
    2: {
        'name': '蝴蝶鱼',
        'condition': '温暖水域',
        'hp': 2,
        'desc': '成群出现，中等难度',
    },
    3: {
        'name': '章鱼鱼',
        'condition': '深海环境',
        'hp': 3,
        'desc': '大型鱼，需要强大的攻击',
    },
    4: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 4,
        'desc': '大型鱼，需要强大的攻击',
    },
    5: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 5,
        'desc': '大型鱼，需要强大的攻击',
    },
    6: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 6,
        'desc': '大型鱼，需要强大的攻击',
    },
    7: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 7,
        'desc': '大型鱼，需要强大的攻击',
    },
    8: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 8,
        'desc': '大型鱼，需要强大的攻击',
    },
    9: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 9,
        'desc': '大型鱼，需要强大的攻击',
    },
    10: {
        'name': '鲨鱼',
        'condition': '深海环境',
        'hp': 10,
        'desc': '大型鱼，需要强大的攻击',
    },
}
def get_fish_detail(fish_type):
    base = fish.loc[fish_type].to_dict()
    detail = fish_details.get(fish_type, {})
    return {
        **base,
        **detail,
        'full_img': pygame.image.load(f'images/fishi{fish_type}.png')  # 加载全身图
    }

cols=['width','height','space','live','score','hp']
idx=list(i for i in range(1,11))
fish=pd.DataFrame(data,columns=cols,index=idx)



class Fish(pygame.sprite.Sprite):
    def __init__(self):
        super(Fish, self).__init__()

        # 必须先初始化 type 属性
        self.type = random.randint(1,10)  # 此句必须放在最前面

        self.fish = fish
        self.fish_w = fish.loc[self.type]['width']
        self.fish_h = fish.loc[self.type]['height']/fish.loc[self.type]['space']

        # 血量初始化应放在类型确定之后
        self.max_hp = fish.loc[self.type]['hp']
        self.current_hp = self.max_hp

        self.fish_l=self.fish_h*fish.loc[self.type]['live']

        self.image_all=pygame.image.load('images/fish'+str(self.type)+'.png')
        self.y=0
        ###0,---》 1,<<---分别代表2个方向，随机旋转
        self.direction=random.randint(0,1)
        ##如果由左向右，X坐标为0 ，反之，即x=1024
        if self.direction==0:
            self.rect_x=0
        else:
            self.rect_x=1024
        self.rect_y=random.randint(0,768)
        ##这里宽高固定 设置动态的
        self.image = self.image_all.subsurface((0, self.y, self.fish_w, self.fish_h))
        self.rect=self.image.get_rect(center=(self.rect_x,self.rect_y))

        self.isDestory=False
        self.isAttack=False
        self.speed=0.3
        self.net=None
        ##设置鱼奖励分数
        self.reward= fish.loc[self.type]['score']
        self.bshape=1
        self.cointext=None
        self.coin=None
        self.count=0
        self.k=1

    def display(self,screen):
        if not self.isAttack:
            if self.y<self.fish_h*(self.fish.loc[self.type]['live']-1):
                if self.y%self.fish_h==0:

                    self.image=self.image_all.subsurface((0,self.y,self.fish_w, self.fish_h))
                    ##0的时候图片正常，1的时候即镜像
                    if self.direction==1:
                        self.image=pygame.transform.flip(self.image,True,False)
                self.y+=1
                # print(self.y)
            else:
                self.y=0
        else:
            if self.k<4:
                if self.count%40==0:
                    self.image=self.image_all.subsurface((0,self.y,self.fish_w, self.fish_h))
                    if self.direction==1:
                        self.image=pygame.transform.flip(self.image,True,False)
                    self.k+=1
                self.count+=1
            else:
                self.isDestory=True
        screen.blit(self.image,self.rect)

    def move(self):
        ##0:+ 1:-
        if not self.isAttack:
            if self.direction==0:
                self.rect_x+=self.speed
                if self.rect_x>1024:
                    self.isDestory=True
            else:
                self.rect_x-=self.speed
                if self.rect_x<0:
                    self.isDestory=True
        self.rect=self.image.get_rect(center=(self.rect_x,self.rect_y))






