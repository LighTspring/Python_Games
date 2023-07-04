#coding:gbk
import numpy as np
import pygame
import sys
class py2048(object):
    def __init__(self,n):
        self.n=n #n*n�汾��
        while True:
            inia=np.random.choice([0,2,4],(n,n),replace=True,p=[0.8,0.175,0.025])#�������0��2��4
            if (inia==np.zeros((n,n))).sum()==n*n-(n-2): #�ж������Ƿ���Ч
                self.init=inia
                break
        self.temp=self.init.copy() #copy��ֵ����ֹ�����޸ģ�python��ֵ����˼�Ƕ�ͬһ��������������֣������copy��һ���仯��һ�����ű仯
        self.record=[self.init] #��ʷ��¼�б�
        # ʹ��pygame֮ǰ�����ʼ��
        pygame.init()
        # ������������
        self.screen = pygame.display.set_mode((1200,600))
        self.screen.fill('white')
        # ���ô��ڵı��⣬����Ϸ����
        pygame.display.set_caption('2048')
        self.face = pygame.Surface((600,500),flags=pygame.HWSURFACE)
        #�����ɫ
        self.f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',100) #������Ҫ�޸�����·����
        self.color=(255,218,185) #������ɫ
        self.linewidth=10 #�������
        self.ground=(176,224,230)
        self.values=0
        self.scores=[self.values]
        self.text(self.init)
        self.regretcount=0
        self.pro=[]
        print(self.init)
    def removezero(self,matrix): #ȥ�������ж����0��Ϊ������ƶ����̵�
        temp=[]
        for i in range(self.n):
            temp.append((matrix[i][matrix[i]!=0]).tolist())
        for k,i in enumerate(temp):
            for j in range(len(i),self.n):
                temp[k].append(0)
        res=np.array(temp)
        return res
    def move(self,matrix):#����Ϊ��׼
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
    def judge(self,matrix):#����Ϊ��׼
        #ÿһ������Ԫ�ص���߶������㣬�򷵻�False
        res=(np.sort(matrix!=0)[:,::-1]==(matrix!=0)).all()==0#matrix!=0�õ��ľ����������Ϊ�������������ڸ÷�������ƶ�,����Ҫ���Ǵ����ظ����ֶ���Ҫ��ȥ��
        temp=matrix.copy().astype('float')#תΪfloat,��np.nan���,������������0��˵�������ƶ���
        temp[temp==0]=np.nan
        if (0 in np.diff(temp)) or res:
            return True
    def left(self,matrix): #��
        res=self.move(matrix)
        return res
    def right(self,matrix): #�һ���ͨ����΢�ı䴫��������ʽ����Ӧmove����
        res=self.move(matrix[:,::-1])[:,::-1]
        return res
    def up(self,matrix):
        res=self.move(matrix.T).T
        #print(res)
        return res
    def down(self,matrix):
        res=self.move(matrix.T[:,::-1])[:,::-1].T
        return res
    def new(self,matrix): #������֮������λ�ó���2��4
        add=np.zeros((self.n,self.n))
        itm=np.random.choice(np.where(matrix.ravel()==0)[0])
        add[itm//self.n,itm%self.n]=np.random.choice([2,4],p=[0.9,0.1])
        return add
    def result(self): #չʾ���
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
        f = pygame.font.Font('C:/Windows/Fonts/ARLRDBD.TTF',75) #�����ļ�·��
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
    def refresh(self): #ʵʱ���£�ˢ����Ļ
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
        
    def regret(self): #����
        del self.record[-1]
        self.temp=self.record[-1]
        del self.scores[-1]
        self.values=self.scores[-1]
        del self.pro[-1]
        self.refresh()
    def interface(self): #������Ϸ
        #����ʱ�Ӷ��󣨿�����Ϸ��FPS��
        clock = pygame.time.Clock()
        # �̶�����Σ�ʵ�ֵ��"X"���˳�����Ĺ���
        while True:
            self.refresh()
            #ͨ��ʱ�Ӷ���ָ��ѭ��Ƶ�ʣ�ÿ��ѭ��60��
            clock.tick(60)
            # ѭ����ȡ�¼��������¼�״̬
            for event in pygame.event.get():
                # �ж��û��Ƿ����"X"�رհ�ť,��ִ��if�����
                if event.type == pygame.QUIT:
                    #ж������ģ��
                    pygame.quit()
                    #��ֹ����ȷ���˳�����
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.judge(self.temp.T):
                            temp=self.up(self.temp)
                            self.temp=temp+self.new(temp)
                            self.record.append(temp)
                            print(self.temp)#������̨��ӡ��Ϊ�ڽ�������ʾ
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
            pygame.display.flip() #������Ļ����
a=py2048(4)
a.interface()