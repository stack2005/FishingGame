# *_* coding : UTF-8 *_*


import pygame
import math
from net import Net
from coinText import Cointext
from coin import Coin

class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,angle,enemtlist,shape):
        super().__init__()
        # 新增子弹攻击力属性（根据炮弹等级1-7）
        self.damage = shape  # 攻击力等于炮弹等级
        self.shape=shape
        self.image=pygame.image.load('images/bullet'+str(self.shape)+'.png')
        self.org_image=self.image.copy()
        self.angle=angle
        self.image=pygame.transform.rotate(self.org_image,self.angle)
        self.distance=50
        self.pos_x=math.sin(math.radians(-self.angle))*self.distance+pos[0]
        self.pos_y=pos[1]-math.cos(math.radians(math.fabs(self.angle)))*self.distance
        self.pos=(self.pos_x,self.pos_y)

        self.rect=self.image.get_rect(center=self.pos)

        self.speed=3
        self.isDestory=False
        self.enemtlist=enemtlist

    def display(self, screen):
        screen.blit(self.image, self.rect)
        self.move()

    def move(self):
        self.pos_x+=math.sin(math.radians(-self.angle))*self.speed
        self.pos_y-=math.cos(math.radians(math.fabs(self.angle)))*self.speed

        self.pos = (self.pos_x, self.pos_y)
        self.rect = self.image.get_rect(center=self.pos)

        if self.pos_y<0 or self.pos_x<0 or self.pos_x>1024:
            self.isDestory=True
        self.attack(self.enemtlist)

    def attack(self,enemtlist):
        for enemy in enemtlist:
            if pygame.sprite.collide_circle_ratio(0.5)(enemy,self):
                # 每次命中减少鱼的血量
                enemy.current_hp -= self.damage

                # 当血量归零时执行捕获逻辑
                if enemy.current_hp <= 0:
                    enemy.isAttack = True
                    enemy.y = enemy.fish_l

                    # 生成渔网和奖励
                    x,y,w,h = enemy.rect
                    net = Net((x,y), self.shape)
                    enemy.net = net
                    enemy.cointext = Cointext(enemy.rect, enemy.reward, self.shape)
                    enemy.coin = Coin(enemy.rect)
                    enemy.bshape = self.shape

                # 命中后子弹销毁（无论是否击毙）
                self.isDestory = True
                break  # 一颗子弹只攻击一条鱼        ##子弹攻击小鱼，子弹消失，小鱼消失
        # 先将子弹和小鱼都变成pygame的精灵类，可以使用边界碰撞判断
        ###将要攻击的鱼作为参数传入