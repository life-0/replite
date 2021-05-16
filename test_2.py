""" -*- coding: utf-8 -*-  
 @Author : life-0 
 @File : test_2.py
 @Time : 2021/5/3 20:41
 TODO @desc:
             正则匹配
"""
import os
import re
import zhconv


# 获取文件路径
def findAndInput(path, matchedMusicPath):  # 相对路径
    matchedMusic = open(matchedMusicPath, encoding="UTF-8-sig")
    matchedMusicLine = matchedMusic.readline()
    matchedMusic_list = {}  # 受匹配的音乐集合
    matchedKey = 1  # 匹配键
    while matchedMusicLine:
        matchedMusicLine = matchedMusicLine.replace(u'\xa0', ' ').replace("\n", "")  # 去除 nbsp的现象
        matchedMusicLine = zhconv.convert(matchedMusicLine, 'zh-hans')  # 将文本转为中文简体 以防万一
        targetAtr = re.split(r'[=]', matchedMusicLine)  # 分割目标文本 : Jam - 七月上.mp3=F:/缓存音乐/Music1/Jam - 七月上.mp3
        Music = re.split(r'[\s.、&:_\\/ ()（）-]', targetAtr[0].lower())  # 切割为歌名 作者名.mp3
        while "" in Music:  # 去除列表中的空字符串
            Music.remove("")
        targetAtr.pop(0)
        matchedMusic_list[matchedKey] = Music + targetAtr
        matchedKey += 1
        matchedMusicLine = matchedMusic.readline()
    files = os.listdir(path)  # 获取所有歌单文件
    # files = ['DAISHI DANCE.txt']
    musicCount = 0  # 歌单总个数
    for f in files:
        print("文件名:", f)  # 歌单文件里的数据
        file = open(path + '/' + f, 'r', encoding='UTF-8-sig')  # 获得指定文件
        line = file.readline()  # 按行读取
        while line:
            line = line.replace(u'\xa0', ' ').replace('\n', "")  # 去除 nbsp的现象
            # targetMusicLine = "".join(line.split(" "))  # 文本空格异常处理
            targetMusicLine = zhconv.convert(line, 'zh-hans')  # 将目标歌单的数据也转为中文简体 以防万一
            # print(lineStr, end="")
            adaptation(targetMusicLine, matchedMusic_list)  # 文本适配
            musicCount += 1
            line = file.readline()
    print("匹配次数为:", musicCount)


# musicName : 歌单的一行数据 歌名 - 作者名
# matchedMusicPath : 需要进行匹配的文件
def adaptation(musicName, matchedMusic_list):

    matchName = re.split(r'[\s.、()（）&:_\\/-]',  # "".join(musicName.split()).lower()
                         musicName.lower())  # 一丝不挂 - 陈奕迅 分割文本 好进行匹配
    print(musicName)
    while "" in matchName:  # 去除列表中的空字符串
        matchName.remove("")

    matchDegree = 0  # 设置匹配度 歌名与歌单=路径搜索结果的匹配程度
    for matchedKey, matchedValue in matchedMusic_list.items():
        matched = matchedValue[0:-3]
        for matchedValuePrecisely in matched:  # 精细化歌名进行匹配
            Reg_name = r'' + matchedValuePrecisely  # 正则表达式  匹配歌名
            pattern = re.compile(Reg_name, re.I)
            if pattern.search("".join(musicName.lower())):
                matchDegree = 0
                for value in matchName:  # 进行歌名 作者名匹配
                    if matched.count(value) != 0:
                        matchDegree += 1
                    else:
                        continue
                    # for j in matched:
                    #     if i.lower() in j.lower() or j.lower() in i.lower():
                    #         match += 1

        if len(matchName) <= matchDegree <= len(matched):
            # fileSize = os.path.getsize(targetAtr[-1])  # 匹配度文件查找
            print("匹配度:", matchDegree, matchName, matched, matchedValue)

    if matchDegree == 0:  # 设置匹配度为0的情况 也就是说歌单有,而本地文件的路径没有的歌
        # failedAdapt.append(fileName.strip('\n'))
        # print(musicName.strip('\n'), "数据未找到!")
        failedMatch.append(musicName)


# 输出已经匹配号的歌及路径
def outputM3u():
    print()


if __name__ == '__main__':
    failedMatch = []
    findAndInput('./data', './data/MusicPath.txt')
    failedMatch = list(dict.fromkeys(failedMatch))
    print("数据未找到个数:", len(failedMatch))
    for i in failedMatch:
        print(i)
