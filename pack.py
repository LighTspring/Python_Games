#coding:gbk
from subprocess import run,Popen
from PyInstaller import __file__
from os import path,remove,getcwd
class pack():
    def __init__(self,fatherpath=getcwd()):
        '''所用的PyInstaller所要打包的文件都在工作路径下'''
        self.fpath=fatherpath#需要打包的工作目录os.getcwd()
        self.inspath=path.join(self.fpath,r'env\Scripts\pyinstaller.exe')#支持所要打包的文件的pyinstaller目录
    def base(self,docname,name=True,one=True,control=True,icon=False,sfiles=[]):

        '''name是好听的名字，docname是所要打包的文件名'''
        l=[self.inspath]
        l.append(docname)
        if one:l.append('-F')
        if not control:l.append('-w')
        if icon:
            from imp import find_module
            found=False
            try:
                find_module('pillow')
                found=True
            except:
                #安装Pillow会自动转换为ico文件
                if not found:
                    self.dlpillow() 
            l.append('-i '+icon)
        if name:l.append('-n '+name)
        #l.append(path.join(self.fpath,docname))

        #l.append('-p '+docname)

        print(l)
        if sfiles:
            l.append(' -p '+' -p '.join(sfiles))
        cmd_str=' '.join(l)
        print('*'*5,cmd_str+'*'*5)
        if path.exists(name+'.spec'):
            remove(name+'.spec')
        run(cmd_str,cwd=self.fpath,shell=True)
        #Popen('nvidia-smi',cwd=r'C:\Users\73582', shell=True, stdout=None, stderr=None).wait()
    def dlpillow(self):
        p='pillow'
        cmd_str=f'pip install --upgrade {p}'
        run(cmd_str,cwd=path.join(self.fpath,r'env\Scripts'),shell=True)
        