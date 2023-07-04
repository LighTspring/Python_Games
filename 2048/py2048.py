#coding:gbk
import numpy as np
import pygame
import sys
class py2048(object):
    def __init__(self,n):
        self.n=n #n*n版本的
        while True:
            inia=np.random.choice([0,2,4],(n,n),replace=True,p=[0.8,0.175,0.025])#随机生成0，2，4
            if (inia==np.zeros((n,n))).sum()==n*n-(n-2): #判断生成是否有效
                self.init=inia
                break
        self.temp=self.init.copy() #copy赋值但防止意外修改，python赋值的意思是对同一个对象绑定两个名字，如果不copy，一个变化另一个跟着变化
        self.record=[self.init] #历史记录列表
        # 使用pygame之前必须初始化
        pygame.init()
        # 设置主屏窗口
        self.screen = pygame.display.set_mode((1200,600))
        self.screen.fill('white')
        # 设置窗口的标题，即游戏名称
        pygame.display.set_caption('2048')
        self.face = pygame.Surface((600,500),flags=pygame.HWSURFACE)
        #填充颜色
        self.f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',100) #可能需要修改字体路径！
        self.color=(255,218,185) #背景颜色
        self.linewidth=10 #线条宽度
        self.ground=(176,224,230)
        self.values=0
        self.scores=[self.values]
        self.text(self.init)
        self.regretcount=0
        self.pro=[]
        print(self.init)
    def removezero(self,matrix): #去除矩阵中多余的0，为后面的移动做铺垫
        temp=[]
        for i in range(self.n):
            temp.append((matrix[i][matrix[i]!=0]).tolist())
        for k,i in enumerate(temp):
            for j in range(len(i),self.n):
                temp[k].append(0)
        res=np.array(temp)
        return res
    def move(self,matrix):#以左滑为基准
        print(self.scores)
        res=self.removezero(matrix).copy()
        temp=[]
        tempscore=0
        for k in range(self.n):
            t=[]
            
            for i,(a,b) in enumerate(zip(res[k][:-1:],res[k][1::])):
                if a!=b:
                    t.append(a)
                    
                else :
                    t.append(a*2)
                    tempscore+=a*2
                    
                    
                    res[k][i+1]=0
                if i==self.n-2:
                    t.append(res[k][-1]) if res[k][-1]!=0 else t.append(0)
            
            temp.append(t)
        self.values+=tempscore
        self.scores.append(self.values)
        return self.removezero(np.array(temp))
    def judge(self,matrix):#以左滑为基准
        #每一个非零元素的左边都不是零，则返回False
        res=(np.sort(matrix!=0)[:,::-1]==(matrix!=0)).all()==0#matrix!=0得到的矩阵如果本身为降序排列则不能在该方向继续移动,还需要考虑存在重复数字而需要消去的
        temp=matrix.copy().astype('float')#转为float,用np.nan标记,做差分如果出现0则说明可以移动。
        temp[temp==0]=np.nan
        if (0 in np.diff(temp)) or res:
            return True
    def left(self,matrix): #左划
        res=self.move(matrix)
        return res
    def right(self,matrix): #右划，通过稍微改变传入矩阵的形式以适应move函数
        res=self.move(matrix[:,::-1])[:,::-1]
        return res
    def up(self,matrix):
        res=self.move(matrix.T).T
        #print(res)
        return res
    def down(self,matrix):
        res=self.move(matrix.T[:,::-1])[:,::-1].T
        return res
    def new(self,matrix): #滑动完之后在新位置出现2，4
        add=np.zeros((self.n,self.n))
        itm=np.random.choice(np.where(matrix.ravel()==0)[0])
        add[itm//self.n,itm%self.n]=np.random.choice([2,4],p=[0.9,0.1])
        return add
    def result(self): #展示结果
        pr=self.temp
        if 2048 in pr:
            self.pro.append('Victory')
            return 'Victory'
        if 0 in pr:
            self.pro.append('Go')
            return 'GO'
        else:
            for i in range(self.n-1):
                if (True in (pr[i]==pr[i+1])) or (True in (pr.T[i]==pr.T[i+1])):
                    self.pro.append('Go')
                    return 'GO'
            self.pro.append('Game Over')
            return 'Game Over'
    def resdis(self):
        f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',75) #字体文件路径
        pygame.draw.rect(self.screen,'white',(650,50,500,150), 0)
        txt=f.render(self.result(),True,(0,206,209),'white')
        textRect=txt.get_rect()
        pos=(900,100)
        textRect.center=(pos)
        self.screen.blit(txt,textRect)
    def text(self,matrix):
        f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',50)
        for i in range(self.n):
            for j in range(self.n):
                pos=50+300/self.n+600/self.n*j,50+250/self.n+500/self.n*i
                if matrix[i][j]!=0:
                    txt=f.render(str(matrix[i][j]),True,'black',self.ground)
                    textRect=txt.get_rect()
                    textRect.center=(pos)
                    self.screen.blit(txt,textRect)
        f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',100)
        txtvalue=f.render(str(int(self.values)),True,(0,206,209),'white')
        txtvalueRect=txtvalue.get_rect()
        txtvalueRect.center=(900,400)
        self.screen.blit(txtvalue,txtvalueRect)
    def refresh(self): #实时更新，刷新屏幕
        self.screen = pygame.display.set_mode((1200,600))
        self.screen.fill('white')
        f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',75)
        txt=f.render('BackSpace',True,(210,180,140),'white')
        textRect=txt.get_rect()
        pos=(950,250)
        textRect.center=(pos)
        self.screen.blit(txt,textRect)
        self.face.fill(color=self.ground)
        for i in range(1,self.n):
            pygame.draw.line(self.face,self.color,(0,500/self.n*i),(600,500/self.n*i),self.linewidth)
            pygame.draw.line(self.face,self.color,(600/self.n*i,0),(600/self.n*i,500),self.linewidth)
        self.screen.blit(self.face,(50,50))
        self.text(self.temp.astype('int'))
        self.resdis()
        
    def regret(self): #悔棋
        del self.record[-1]
        self.temp=self.record[-1]
        del self.scores[-1]
        self.values=self.scores[-1]
        del self.pro[-1]
        self.refresh()
    def interface(self): #启动游戏
        #创建时钟对象（控制游戏的FPS）
        clock = pygame.time.Clock()
        # 固定代码段，实现点击"X"号退出界面的功能
        while True:
            self.refresh()
            #通过时钟对象，指定循环频率，每秒循环60次
            clock.tick(60)
            # 循环获取事件，监听事件状态
            for event in pygame.event.get():
                # 判断用户是否点了"X"关闭按钮,并执行if代码段
                if event.type == pygame.QUIT:
                    #卸载所有模块
                    pygame.quit()
                    #终止程序，确保退出程序
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.judge(self.temp.T):
                            temp=self.up(self.temp)
                            self.temp=temp+self.new(temp)
                            self.record.append(temp)
                            print(self.temp)#将控制台打印变为在界面上显示
                        else :continue
                    if event.key == pygame.K_DOWN:
                        if self.judge(self.temp.T[:,::-1]):
                            temp=self.down(self.temp)
                            self.temp=temp+self.new(temp)
                            self.record.append(temp)
                            print(self.temp)
                        else :continue
                    if event.key == pygame.K_LEFT:
                        if self.judge(self.temp):
                            temp=self.left(self.temp)
                            self.temp=temp+self.new(temp)
                            self.record.append(temp)
                            print(self.temp)
                        else :continue
                    if event.key == pygame.K_RIGHT:
                        if self.judge(self.temp[:,::-1]):
                            temp=self.right(self.temp)
                            self.temp=temp+self.new(temp)
                            self.record.append(temp)
                            print(self.temp)
                        else:continue
                    if event.key ==pygame.K_BACKSPACE and len(self.record)>=2:
                        self.regretcount+=1
                        self.regret()
                        print(self.regretcount)
            pygame.display.flip() #更新屏幕内容
a=py2048(4)
a.interface()