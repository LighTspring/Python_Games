from MyQR import myqr
url=input('二维码所链接的URL：\n')
picture=input('所要生成的二维码背景图片路径：\n')
print('生成的二维码名称是code.png')
myqr.run(
    words=url, # 包含信息
    picture=picture,   # 背景图片
    colorized=True,   # 是否有颜色，如果为False则为黑白
    save_name='code.png' # 输出文件名
)
