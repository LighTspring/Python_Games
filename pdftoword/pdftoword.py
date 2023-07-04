#coding: gbk
from pdf2docx import Converter
import PySimpleGUI as sg
def pdf2word(file_path):
    file_name=file_path.split('.')[0]
    doc_file=f'{file_name}.docx'
    p2w=Converter(file_path)
    p2w.convert(doc_file,start=0,end=None)
    p2w.close()
    return doc_file
def main():
    #ѡ������
    sg.theme('LightBlue')
    layout=[
        [sg.Text('pdfToword',font=('΢���ź�',12)),sg.Text('',key='filename',size=(50,1),font=('΢���ź�',10),text_color='blue')],
        [sg.Output(size=(80,10),font=('΢���ź�',10))],
        [sg.FilesBrowse('ѡ���ļ�',key='file',target='filename'),sg.Button('��ʼת��'),sg.Button('�˳�ת��')]
        ]
    #��������
    window=sg.Window('pdftoword',layout,font=('΢���ź�',15),default_element_size=(50,1))
    while True:
        event,values=window.read()#�¼���ֵ�Ķ�ȡ
        print(event,values)
        if event=='��ʼת��':
            if values['file'] and values['file'].split('.')[1]=='pdf':
                filename=pdf2word(values['file'])
                print('�ļ�������1')
                print('\n'+'ת���ɹ���'+'\n')
                print('�ļ�����λ�ã�',filename)
            elif values['file'] and values['file'].split(';')[0].split('.')[1]=='pdf':
                print(f"�ļ�������{len(values['file'].split(';'))}")
                for f in values['file'].split(';'):
                    filename=pdf2word(f)
                    print('\n'+'ת���ɹ�'+'\n')
                    print('�ļ�����λ�ã�'+filename)
            else:
                print('error!'*50)
        if event in (None,'�˳�'):
                break
        window.close()
main()
