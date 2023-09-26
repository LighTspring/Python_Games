#coding:gbk
import numpy as np
import matplotlib.pyplot as plt
class MUSIC():
    def __init__(self,num_ele=8,num_signal=2,SNR=100,signal_amplitude=[4,4],signal_frequency=20000,signal_phase0=[np.pi/6,np.pi/3],theta_i=[0,50],sample_frequency=50000,distance_lam=0.5):
        #signal_frequency�ȿ��ǵ�һƵ�ʵ�����
        #SNR��Ӱ����
        from numpy import array as ar
        self.M=num_ele
        self.d=num_signal
        self.theta=np.deg2rad(ar(theta_i))
        self.SNR=SNR
        self.noise_sigma2=min(signal_amplitude)**2*0.5/SNR#��������
        self.d_l=distance_lam
        s=lambda t:ar(signal_amplitude)[:,None]*np.cos(2*np.pi*signal_frequency*t+ar(signal_phase0)[:,None])
        start=0
        end=2
        self.sample_points=(end-start)*sample_frequency
        t=np.tile(np.linspace(start,end,self.sample_points),(num_signal,1))#���źų���ʱ���-1~2s֮�����,np.tie �����ظ�
        self.st=s(t)

    def array_manifolds(self,theta):
        prime=np.exp(-1j*2*np.pi*self.d_l*np.sin(theta))
        vander=np.vander(prime,self.M)
        return vander.T[::-1,:]#���������α任Ϊ����Ҫ����ʽ

    def autocorrelation_matrix(self):
        x=self.array_manifolds(self.theta)@self.st+self.noise_sigma2*np.random.randn(self.M,self.sample_points)
        R=x@x.conjugate().T/self.sample_points#���Կ��������൱��ȡ��ѧ����
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
        plt.rcParams['font.sans-serif']=['SimHei']#���������������
        plt.rcParams["font.size"]=10#���������С
        plt.rcParams['axes.unicode_minus']=False#��ʾ��������
        theta,P=self.search()
        P=np.abs(P) #��ֹ���������󾯸�
        if dB:
            P=10*np.log10(P)
            ys=r'P_{MUSIC}(\theta)=10log_{10}(\frac{1}{a^H(\theta)U_nU_n^Ha(\theta)})'
        else:ys=r'P_{MUSIC}(\theta)=\frac{1}{a^H(\theta)U_nU_n^Ha(\theta)}'
        xs=r'\theta^{\circ}'
        plt.figure(figsize=(18,9))
        illustration=f'��Ԫ����:{self.M}\n Ԥ���趨�Ĳ��﷽��:{", ".join(np.rad2deg(self.theta).astype(int).astype(str))}\n �����SNR:{self.SNR}\n ��Ԫ����벨���ı�ֵ:{self.d_l}\n SNR={self.SNR}'
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
        self.draw(r'C:\Users\73582\Desktop\temp\ͨ���źŴ���\��ʮһ����ҵ-������-2020301902\4\��������0��',dB=1)
