# С��Ϸ
---

## ��Ŀ����
����Pythonʵ����2048С��Ϸ��pdfתΪword��С����
����URL���ɶ�ά���ʵ�ù��ߣ���������Pyinstaller���(pack.py)
�õ�exe�ļ���˫���������С����������С���
---

## ���ֹ���չʾ
### 2048
![2048С��Ϸ���н�ͼ](introduction/2048.png)
��������������ƶ����˸��BackSpace���޴λ���
### pdftoword
![pdftoword](introduction/pdftoword.png)
### ��ά������С����
![qr](introduction/qr.png)
�Լ��õ��Ķ�ά��

![myqr](introduction/code.png)

### ԭ�����
2048������Python��numpy��PyGame��pdftoword�����ɶ�ά�붼��ֱ�ӵ�������ص�Python�⡣
������˵����ֱ�ӰѴ�����Ӧ�ĸ���һ����
### ��
pack.py������Pyinstaller���н�һ����װ�����ڴ����ʹ��ʾ�����£�
```
from pack import pack
from os import getcwd
p=pack(getcwd())
p.base('My_QRcode.py',name='��ά������С����',icon=r"sl.jpg")
```
Ŀǰ��֧�ּ򵥵Ĵ��