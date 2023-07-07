'''
游戏玩法：
    回车开始游戏；
    空格暂停/继续游戏；
    方向键/wsad键控制小蛇走向

    黄色为食物，红色为炸弹
    吃到食物蛇长加一截
    吃到炸弹/碰壁/碰到自己游戏结束
'''

#导包
import sys
import time
import random
import pygame

def start_music():
    # 加载背景音乐并播放
    file = r"C:\Users\Rose_Vanderboom\Desktop\贪吃蛇（炸弹 课设终版）-rv\开始.mp3"
    pygame.init()  # 进行全部模块的初始化，
    pygame.mixer.init()  # 只初始化音频部分
    pygame.mixer.music.load(file)  # 使用文件名作为参数载入音乐
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)  # 播放载入的音乐。该函数立即返回，音乐播放在后台进行。   -1:循环播放


def eat_music():
    file = r"C:\Users\Rose_Vanderboom\Desktop\贪吃蛇（炸弹 课设终版）-rv\eat.wav"
    eat_sound = pygame.mixer.Sound(file)
    eat_sound.set_volume(2)
    eat_sound.play()


def dead_music():
    # 加载背景音乐并播放
    file = r"C:\Users\Rose_Vanderboom\Desktop\贪吃蛇（炸弹 课设终版）-rv\Toby Fox - Shop.mp3"
    pygame.mixer.init()  # 只初始化音频部分
    pygame.mixer.music.load(file)  # 使用文件名作为参数载入音乐
    pygame.mixer.music.set_volume(2)
    pygame.mixer.music.play(-1)  # 播放载入的音乐。该函数立即返回，音乐播放在后台进行。   -1:循环播放

    time.sleep(6)


class Point:   #希望每一个点都是由行和列组成
    row = 0
    col = 0
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def copy(self):    #蛇身操作要用
        return Point(row=self.row, col=self.col)


#生成点
def creat_point():
    '''
    randint 产生的随机数区间包含左右极限
    即左右都闭：[x,y]
    randrange 产生的随机数只包含左极限
    即左闭右开：[x,y)
    randint 产生的随机数是在指定的某一个区间内的一个值
    randrange 产生的随机数可以设定一个步长，也就是一个间隔。
    '''
    point = Point(0, 0)
    flag = True
    while flag:
        point_row = random.randint(0, ROW-1)
        point_col = random.randint(0, COL-1)
        point = Point(point_row, point_col)

        #如果点随机产生在蛇身上，重新创造点
        flag = False
        if point.row == head.row and point.col == head.col:
            flag = True
        for snake in snakes:
            if point.row == snake.row and point.col == snake.col:
                flag = True
                break
    return point


def creat_bomb(food):
    flag = True
    while flag:
        bomb = creat_point()
        if bomb.col != food.col or bomb.row != food.row:
            flag = False
    return bomb


#初始化
pygame.init()
H = 600  #长
W = 800  #宽
ROW = 30  #行
COL = 40  #列

size = (W, H)  #屏幕大小
window = pygame.display.set_mode(size)
pygame.display.set_caption("李玥的第一条贪吃蛇")
bg_color = (255, 255, 255)  #背景颜色 白

#初始化 蛇头、蛇身、食物
head = Point(row=int(ROW/2), col=int(COL/2))  #蛇头
head_color = (0, 128, 128)  #浅蓝色
snakes = [
    Point(row=head.row, col=head.col+1),
    Point(row=head.row, col=head.col+2),
    Point(row=head.row, col=head.col+3),
]
snakes_color = (200, 200, 200)  #灰色
food = creat_point()        #食物
food_color = (255, 255, 0)  #黄色
bomb = creat_bomb(food)     #炸弹
bomb_color = (255, 0, 0)    #红色


def check():
    '''
    检测
    1.撞墙
    2.撞炸弹
    3.撞自己
    '''
    dead = False
    if head.col < 0 or head.col >= COL or head.row < 0 or head.row >= ROW:
        dead = True
    elif head.col == bomb.col and head.row == bomb.row:
        dead = True
    else:
        for snake in snakes:
            if head.col == snake.col and head.row == snake.row:
                dead = True
                break
    return dead


def rect(point, color):   #画出来
    cell_width = W / COL  #-每个小方块的宽
    cell_height = H / ROW
    left = cell_width * point.col  #left--离左边界有多远
    top = cell_height * point.row  #top--离上边界有多远
    #画
    pygame.draw.rect(window, color, (left, top, cell_width, cell_height))


def draw():  # 渲染
    window.fill(bg_color)  # 填充背景
    # pygame.draw.rect(window,(255,255,255),(0,0,W,H))   另一种画全屏背景方法
    # 蛇头
    rect(head, head_color)
    # 蛇身
    for snake in snakes:
        rect(snake, snakes_color)
    # 食物
    rect(food, food_color)
    # 炸弹
    rect(bomb, bomb_color)


def move(direct):
    if direct == 'left':
        head.col -= 1
    if direct == 'right':
        head.col += 1
    if direct == 'up':
        head.row -= 1
    if direct == 'down':
        head.row += 1


def body(eat):
    '''
    处理身子
    1.把原来的头插入到snakes的头上
    2.如果未吃到食物，把snakes的最后一个删除
    '''
    snakes.insert(0, head.copy())
    if not eat:
        snakes.pop()

def is_dead():
    print("游戏结束")
    dead_music()
    pygame.quit()
    sys.exit(0)

def main():
    global food, bomb
    #游戏循环
    #启动游戏时的相关变量初始化
    start_music()   #放音乐
    direct = 'left'
    game_start = False  #当start = True，over = True 时 -- GAME OVER
    game_over = True
    game_pause = False
    clock = pygame.time.Clock()
    draw()  #画出来
    while True:
        for event in pygame.event.get():  # 获取当前发生的事件（队列）
            #print(event)
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:    #键盘
                if event.key == 13:   #回车键
                    if game_over is True:
                        game_start = True
                        game_over = False
                elif event.key == 32:
                    if not game_over:
                        game_pause = not game_pause
                elif game_start is True and game_over is False and game_pause is False:
                    if event.key == 1073741906 or event.key == 119:   # wasd 和 上下左右 都可操作
                        if direct == 'left' or direct == 'right':
                            direct = 'up'
                    elif event.key == 1073741905 or event.key == 115:
                        if direct == 'left' or direct == 'right':
                            direct = 'down'
                    elif event.key == 1073741904 or event.key == 97:
                        if direct == 'up' or direct == 'down':
                            direct = 'left'
                    elif event.key == 1073741903 or event.key == 100:
                        if direct == 'up' or direct == 'down':
                            direct = 'right'

        if game_start is True and game_over is False and game_pause is False:
            #吃东西
            eat = head.row == food.row and head.col == food.col
            if eat:
                food = creat_point()
                bomb = creat_bomb(food)
                eat_music()
            #处理蛇身
            body(eat)
            #移动/处理蛇头
            move(direct)
            #判断蛇是否死亡
            dead = check()
            if dead:
                is_dead()
            draw()  #画出来
        pygame.display.flip()  #让出控制系统
        clock.tick(15)  # 设置帧频(锁帧)  (1000ms/15)sleep

if __name__ == '__main__':
    main()

