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
import difflib


# 获取文件路径
def findAndInput(path, matchedMusicPath):  # 相对路径
    matchedMusic = open(matchedMusicPath, encoding="UTF-8-sig")
    matchedMusicLine = matchedMusic.readline()
    matchedMusic_list = {}  # 受匹配的音乐集合
    matchedKey = 1  # 匹配键
    while matchedMusicLine:
        matchedMusicLine = matchedMusicLine.replace(u'\xa0', ' ').replace("\n", "")  # 去除 nbsp的现象
        matchedMusicLine = zhconv.convert(matchedMusicLine, 'zh-hans')  # 将文本转为中文简体 以防万一
        targetAtr = re.split(r'[=]', matchedMusicLine)  # 分割目标文本 : Jam - 七月上=F:/缓存音乐/Music1/Jam - 七月上.mp3
        # Music = re.split(r'[\s.、&:_\\/ ()（）-]', targetAtr[0].lower())  # 切割为歌名 作者名.mp3
        while "" in targetAtr:  # 去除列表中的空字符串
            targetAtr.remove("")
        # targetAtr.pop(0)
        matchedMusic_list[matchedKey] = targetAtr
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
# matchedMusic_list : 被匹配的数据集合 歌名 - 作者=路径=文件大小
def adaptation(musicName, matchedMusic_list):
    musicName = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "",
                       musicName)
    match_music = musicName[:musicName.find('-')]  # 从左往右 只要到第一个"-" 视为歌名
    match_author = musicName[musicName.rfind('-'):]  # 从右往左 只要到第一个"-" 视为作者
    match_author_music = match_music + match_author  # 匹配值: 歌名-作者
    # matchName = re.split(r'[\s.、()（）&:_\\/-]',  # "".join(musicName.split()).lower()
    #                      musicName.lower())  # 一丝不挂 - 陈奕迅 分割文本 好进行匹配
    print(musicName)
    # while "" in matchName:  # 去除列表中的空字符串
    #     matchName.remove("")

    dict_matchDegree = {}  # 只有匹配度最高的5个数据
    matchFlag = 0  # 设置匹配度 歌名与歌单=路径搜索结果的匹配程度
    for matchedKey, matchedValue in matchedMusic_list.items():
        # print(musicName.lower(),matchedValue[0].lower())
        matchedValues = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "",
                               matchedValue[0])
        matched_music = matchedValues[:matchedValues.find('-')]  # 从左往右 只要到第一个"-" 视为歌名
        matched_author = matchedValues[matchedValues.rfind('-'):]  # 从右往左 只要到第一个"-" 视为作者
        matched_author_music = matched_music + matched_author  # 匹配值: 歌名-作者

        matchValue = difflib.SequenceMatcher(None, match_author_music.lower(),
                                             matched_author_music.lower()).quick_ratio()  # matchedValue[0].lower()

        if matchValue > 0.4:
            matchFlag += 1
            if len(dict_matchDegree) < 5:  # 限定dict_matchDegree个数
                dict_matchDegree[matchedKey] = [matchValue, match_author_music, matched_author_music, matchedValue[-2:]]
            elif len(dict_matchDegree) == 5:  # 超过dict_matchDegree个数5后,只保留matchValue最高的数据
                min_matchValue = min(dict_matchDegree.values())[0]
                if matchValue > min_matchValue:  # 比对匹配最小值进而替换 从而保留匹配度最高的数据
                    key = list(dict_matchDegree.keys())[
                        list(dict_matchDegree.values()).index(min(dict_matchDegree.values()))]  # 按值反向查找键
                    dict_matchDegree.pop(key)  # 去掉最小值数据
                    dict_matchDegree[matchedKey] = [matchValue, match_author_music, matched_author_music,
                                                    matchedValue[-2:]]

    for matchedKey, matchedValue in dict_matchDegree.items():
        print(matchedValue)

    if matchFlag == 0:
        failedMatch.append(musicName)


# failedMatch_list: 失败匹配的音乐集合 歌名 - 作者
# matchedMusic_list:被匹配的数据集合 [歌名 - 作者,路径,文件大小]
def failedMusicSearch(failedMatch_list, matchedMusic_list):
    # for music in failedMatch_list:
    match_authors = re.split(r'[-]', failedMatch_list.lower())  # 目的: 分割出作者名
    match_authors = re.split(r'[\s.、()（）&:_\\/-]', match_authors[-1])  # 细化多个作者
    match_music = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]|（.*?）", "", failedMatch_list)  # 去除带括号或注释的字符,否则影响判断
    while "" in match_authors:  # 去除列表中的空字符串
        match_authors.remove("")

    # matchName = re.split(r'[\s.、()（）&:_\\/-]',  # "".join(musicName.split()).lower()
    #                      failedMatch_list.lower())  # 一丝不挂 - 陈奕迅 分割文本 好进行匹配
    # while "" in matchName:  # 去除列表中的空字符串
    #     matchName.remove("")
    for matchedMusicKey, matchedMusicValue in matchedMusic_list.items():
        matched_music_author = re.split(r'[-]', matchedMusicValue[0].lower())
        matched_authors = re.split(r'[\s.、()（）&:_\\/-]', matched_music_author[-1].lower())  # 分割出被匹配的作者
        # matched = re.split(r'[\s.、()（）&:_\\/-]',  # "".join(musicName.split()).lower()
        #                    matchedMusicValue[0].lower())
        while "" in matched_authors:  # 去除列表中的空字符串
            matched_authors.remove("")
        # matchDegree = len(matchName) if len(matchName) <= len(matched) else len(matched)
        # check_list = matchName if len(matchName) <= len(matched) else matched

        # for music_author in matched_music_author:
        #     # unique_matchName = [i for i in matchName if i not in matched]  # 找到
        #     # unique_matched = [i for i in matched if i not in matchName]
        #     # if len(unique_matchName) == 0 or len(unique_matched) == 0:
        #     #     print("匹配度:", matchName, matched, matchedMusic_list)
        #     # else:
        #     failedMatch.append(failedMatch_list)


def outputM3u():
    print()


if __name__ == '__main__':
    failedMatch = []
    # matchedMusic_list={}
    findAndInput('./data', 'MusicPath.txt')  # './t从网易云上扒歌单,在本地配对好数据,生成本地歌单m3u文件rash_data/test_DAISHI DANCE.txt'
    failedMatch = list(dict.fromkeys(failedMatch))
    print("数据未找到个数:", len(failedMatch))
    for i in failedMatch:
        print(i)
