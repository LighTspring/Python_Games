#coding:gbk
import numpy as np
import matplotlib.pyplot as plt
class MUSIC():
    def __init__(self,num_ele=8,num_signal=2,SNR=100,signal_amplitude=[4,4],signal_frequency=20000,signal_phase0=[np.pi/6,np.pi/3],theta_i=[0,50],sample_frequency=50000,distance_lam=0.5):
        #signal_frequency先考虑单一频率的来波
        #SNR不影响吗
        from numpy import array as ar
        self.M=num_ele
        self.d=num_signal
        self.theta=np.deg2rad(ar(theta_i))
        self.SNR=SNR
        self.noise_sigma2=min(signal_amplitude)**2*0.5/SNR#噪声功率
        self.d_l=distance_lam
        s=lambda t:ar(signal_amplitude)[:,None]*np.cos(2*np.pi*signal_frequency*t+ar(signal_phase0)[:,None])
        start=0
        end=2
        self.sample_points=(end-start)*sample_frequency
        t=np.tile(np.linspace(start,end,self.sample_points),(num_signal,1))#在信号持续时间的-1~2s之间采样,np.tie 数据重复
        self.st=s(t)

    def array_manifolds(self,theta):
        prime=np.exp(-1j*2*np.pi*self.d_l*np.sin(theta))
        vander=np.vander(prime,self.M)
        return vander.T[::-1,:]#将阵列流形变换为所需要的形式

    def autocorrelation_matrix(self):
        x=self.array_manifolds(self.theta)@self.st+self.noise_sigma2*np.random.randn(self.M,self.sample_points)
        R=x@x.conjugate().T/self.sample_points#除以快拍数，相当于取数学期望
        eigvalue,eigvec=np.linalg.eigh(R)
        return eigvalue,eigvec

    def search(self):
        step=0.1
        #theta=np.linspace(-np.pi,np.pi,int(180/step))
        theta=np.linspace(-np.pi/2,np.pi/2,int(180/step))
        vander=self.array_manifolds(theta)#shape=(self.M,theta.shape[0])
        Un=self.autocorrelation_matrix()[1][:,:-2]
        U=Un@Un.conjugate().T
        aH_U_a=np.array([vander.conjugate().T[i]@U@vander[:,i] for i in range(vander.shape[1])])
        return theta,1/aH_U_a
    def draw(self,save='',dB=False):
        plt.rcParams['font.sans-serif']=['SimHei']#解决中文乱码问题
        plt.rcParams["font.size"]=10#设置字体大小
        plt.rcParams['axes.unicode_minus']=False#显示负号问题
        theta,P=self.search()
        P=np.abs(P) #防止报叙述矩阵警告
        if dB:
            P=10*np.log10(P)
            ys=r'P_{MUSIC}(\theta)=10log_{10}(\frac{1}{a^H(\theta)U_nU_n^Ha(\theta)})'
        else:ys=r'P_{MUSIC}(\theta)=\frac{1}{a^H(\theta)U_nU_n^Ha(\theta)}'
        xs=r'\theta^{\circ}'
        plt.figure(figsize=(18,9))
        illustration=f'阵元个数:{self.M}\n 预先设定的波达方向:{", ".join(np.rad2deg(self.theta).astype(int).astype(str))}\n 信噪比SNR:{self.SNR}\n 阵元间距与波长的比值:{self.d_l}\n SNR={self.SNR}'
        ax=plt.subplot(121)
        ax.plot(np.rad2deg(theta),P)
        ax.set_title(illustration)
        ax.grid()
        plt.xlabel(f'${xs}$')
        plt.ylabel(f'${ys}$'+'  dB'*dB)
        ax=plt.subplot(122,projection='polar')
        ax.plot(theta,P)
        ax.set_title(illustration)
        if save:
            from os import path
            from re import sub
            tempattern=r'[\s*|:]'
            plt.savefig(path.join(save,f'MUSIC_{sub(tempattern,"",illustration)}.png'))
            plt.close()
            #plt.show()
        else:plt.show()
    def play(self):
        self.draw(r'C:\Users\73582\Desktop\temp\通信信号处理\第十一次作业-辛文祺-2020301902\4\单个来波0°',dB=1)
