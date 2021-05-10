""" -*- coding: utf-8 -*-  
 @Author : life-0 
 @File : test.py 
 @Time : 2021/5/3 10:12
 TODO @desc: 数据转换
                
"""
import os
import re


# 获取文件路径
def findAndInput(path, targetFile):  # 相对路径
    files = os.listdir(path)  # 获取所有歌单文件
    count = 0  # 歌总个数
    for f in files:
        print("文件名:", f)
        file = open(path + '/' + f, 'r', encoding='UTF-8-sig')  # 获得指定文件
        line = file.readline()  # 按行读取
        while line:
            lineStr = "".join(line.split(" "))  # 文本空格异常处理
            # print(lineStr, end="")
            adaptation(lineStr, targetFile)  # 文本适配
            count += 1
            line = file.readline()
    print("成功匹配次数为:", count)


# fileName : 歌单的一行数据
# targetFile : 需要进行匹配的文件
def adaptation(fileName, targetFilePath):
    target_File = open(targetFilePath, encoding="UTF-8-sig")
    target = target_File.readline()
    name = re.split(r'[& \\()/（）-]',
                    "".join(fileName.split()).lower())  # 风居住的街道（Piano ver） (翻自 磯村由紀子）  - 饭碗的彼岸 分割文本 好进行匹配
    # print(fileName,end="")
    while "" in name:  # 去除列表中的空字符串
        name.remove("")
    match = 0  # 设置匹配度 歌名与歌单=路径搜索结果的匹配程度
    while target:
        targetAtr = re.split(r'[=]', target)  # 分割目标文本 : Jam - 七月上.mp3=F:/缓存音乐/Music1/Jam - 七月上.mp3
        Music = re.split(r'[()（）-]', "".join(targetAtr[0].split()).lower())  # 切割为歌名 作者名.mp3
        while "" in Music:  # 去除列表中的空字符串
            Music.remove("")
        Reg_name = r'' + "".join(name[0].lower().split())  # 正则表达式  匹配歌名
        pattern = re.compile(Reg_name, re.I)
        if pattern.search("".join(Music)):
            matched = 0
            match = 0
            for i in name:  # 进行歌名 作者名匹配
                for j in Music:
                    if i.lower() in j.lower() or j.lower() in i.lower():
                        match += 1
            if match >= 2:
                # fileSize = os.path.getsize(targetAtr[-1])  # 匹配度文件查找
                print("匹配度:", match, name, targetAtr)

        target = target_File.readline()
    if match == 0:  # 设置匹配度为0的情况 也就是说歌单有,而本地文件的路径没有的歌
        # failedAdapt.append(fileName.strip('\n'))
        print(fileName.strip('\n'), "数据未找到!")
    target_File.close()
    # print(fileName)


if __name__ == '__main__':
    findAndInput('./data', 'MusicPath.txt')
