from MyQR import myqr
url=input('��ά�������ӵ�URL��\n')
picture=input('��Ҫ���ɵĶ�ά�뱳��ͼƬ·����\n')
print('���ɵĶ�ά��������code.png')
myqr.run(
    words=url, # ������Ϣ
    picture=picture,   # ����ͼƬ
    colorized=True,   # �Ƿ�����ɫ�����ΪFalse��Ϊ�ڰ�
    save_name='code.png' # ����ļ���
)
