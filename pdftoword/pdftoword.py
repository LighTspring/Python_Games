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
    #选择主题
    sg.theme('LightBlue')
    layout=[
        [sg.Text('pdfToword',font=('微软雅黑',12)),sg.Text('',key='filename',size=(50,1),font=('微软雅黑',10),text_color='blue')],
        [sg.Output(size=(80,10),font=('微软雅黑',10))],
        [sg.FilesBrowse('选择文件',key='file',target='filename'),sg.Button('开始转换'),sg.Button('退出转换')]
        ]
    #创建窗口
    window=sg.Window('pdftoword',layout,font=('微软雅黑',15),default_element_size=(50,1))
    while True:
        event,values=window.read()#事件和值的读取
        print(event,values)
        if event=='开始转换':
            if values['file'] and values['file'].split('.')[1]=='pdf':
                filename=pdf2word(values['file'])
                print('文件个数：1')
                print('\n'+'转换成功：'+'\n')
                print('文件保存位置：',filename)
            elif values['file'] and values['file'].split(';')[0].split('.')[1]=='pdf':
                print(f"文件个数：{len(values['file'].split(';'))}")
                for f in values['file'].split(';'):
                    filename=pdf2word(f)
                    print('\n'+'转化成功'+'\n')
                    print('文件保存位置：'+filename)
            else:
                print('error!'*50)
        if event in (None,'退出'):
                break
        window.close()
main()
