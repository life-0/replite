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

def findAndInput(path, matchedMusicPath, targetPathFile):  # 相对路径
    """
    :param path: 歌单文件夹
    :param matchedMusicPath: 歌名路径文件
    :param targetPathFile: 匹配成功后存放的文件路径
    """
    matchedMusic = open(matchedMusicPath, encoding="UTF-8-sig")
    matchedMusicLine = matchedMusic.readline()
    matchedMusic_list = {}  # 受匹配的音乐集合
    success_musicPath_list = []  # 成功匹配到的数据
    matchedKey = 1  # 匹配键

    while matchedMusicLine:
        # matchedMusicLine = matchedMusicLine.replace(u'\xa0', ' ').replace("\n", "")  # 去除 nbsp的现象
        matchedMusicLine = matchedMusicLine.replace("\n", "")  # 去除 nbsp的现象
        targetAtr = re.split(r'[=]', matchedMusicLine)  # 分割目标文本 : Jam - 七月上=F:/缓存音乐/Music1/Jam - 七月上.mp3
        # Music = re.split(r'[\s.、&:_\\/ ()（）-]', targetAtr[0].lower())  # 切割为歌名 作者名.mp3
        while "" in targetAtr:  # 去除列表中的空字符串
            targetAtr.remove("")
        # targetAtr.pop(0)
        targetAtr[0] = targetAtr[0].replace(u'\xa0', ' ')  # 仅去除歌名 nbsp的现象,而不是路径的
        targetAtr[0] = zhconv.convert(targetAtr[0], 'zh-hans')  # 将文本转为中文简体 以防万一
        matchedMusic_list[matchedKey] = targetAtr
        matchedKey += 1
        matchedMusicLine = matchedMusic.readline()
    files = os.listdir(path)  # 获取所有歌单文件
    # files = ['acivii.txt']

    musicCount = 0  # 歌单总个数
    for f in files:
        print("文件名:", f)  # 歌单文件里的数据
        file = open(path + '/' + f, 'r', encoding='UTF-8-sig')  # 获得指定文件
        line = file.readline()  # 按行读取
        while line:
            line = line.replace(u'\xa0', ' ').replace('\n', "")  # 去除 nbsp的现象
            targetMusicLine = zhconv.convert(line, 'zh-hans')  # 将目标歌单的数据也转为中文简体 以防万一
            success_path = adaptation(targetMusicLine, matchedMusic_list)  # 文本适配 返回成功匹配到的路径
            if success_path:
                success_musicPath_list.append(success_path)  # 添加进入列表中
            musicCount += 1
            line = file.readline()
        outPutM3u(success_musicPath_list, targetPathFile, f)  # 写入
        success_musicPath_list = []  # 数据清空
    print("匹配次数为:", musicCount)


def adaptation(musicName, matchedMusic_list):
    """
    :param musicName:  歌单的一行数据 歌名 - 作者名
    :param matchedMusic_list: 被匹配的数据集合 歌名 - 作者=路径=文件大小
    :return: 返回成功找到的数据 直接给路径
    """
    match_musicName = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "",
                             musicName)
    print(musicName)
    # while "" in matchName:  # 去除列表中的空字符串
    #     matchName.remove("")
    dict_matchDegree = {}  # 只有匹配度最高的5个数据
    matchFlag = 0  # 设置是否匹配到数据
    for matchedKey, matchedValue in matchedMusic_list.items():
        matchedValues = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "",
                               matchedValue[0])
        matched_music = matchedValues[:matchedValues.find('-')]  # 从左往右 只要到第一个"-" 视为歌名
        matched_author = matchedValues[matchedValues.rfind('-'):]  # 从右往左 只要到第一个"-" 视为作者
        matched_author_music = matched_music + matched_author  # 匹配值: 歌名-作者
        matchValue = difflib.SequenceMatcher(None, match_musicName.lower(),  # 获得匹配值
                                             matched_author_music.lower()).quick_ratio()  # matchedValue[0].lower()

        if matchValue > 0.4:  # 匹配程度必须大于0.4 低于0.4 则匹配不上
            matchFlag += 1  # 确认匹配到数据
            if len(dict_matchDegree) < 4:  # 限定dict_matchDegree个数
                dict_matchDegree[matchedKey] = [matchValue, match_musicName, matched_author_music, matchedValue[-2:]]
            elif len(dict_matchDegree) == 4:  # 超过dict_matchDegree个数4后,只保留matchValue最高的数据
                min_matchValue = min(dict_matchDegree.values())[0]
                if matchValue > min_matchValue:  # 比对匹配最小值进而替换 从而保留匹配度最高的数据
                    key = list(dict_matchDegree.keys())[
                        list(dict_matchDegree.values()).index(min(dict_matchDegree.values()))]  # 按值反向查找键
                    dict_matchDegree.pop(key)  # 去掉最小值数据
                    dict_matchDegree[matchedKey] = [matchValue, match_musicName, matched_author_music,
                                                    matchedValue[-2:]]

    sorted_dict_matchDegree = sorted(dict_matchDegree.items(), key=lambda kv: (kv[1], kv[0]))  # 升序排序
    highest_tuple = sorted_dict_matchDegree[-2:]  # 获取最高匹配的两个数据
    if len(highest_tuple) == 2:
        first_match_list = highest_tuple.pop()
        second_match_list = highest_tuple.pop()
        first_match_degree = float((first_match_list[-1])[0])  # 获取文件匹配程度
        second_match_degree = float((second_match_list[-1])[0])  # 获取文件匹配程度
        first_match_size = float(((first_match_list[-1])[-1])[-1])  # 获取文件大小
        second_match_size = float(((second_match_list[-1])[-1])[-1])  # 获取文件大小
        first_match_path = ((first_match_list[-1])[-1])[-2]  # 获取文件路径
        second_match_path = ((second_match_list[-1])[-1])[-2]  # 获取文件路径
        # 匹配度大小比较
        if first_match_degree > second_match_degree:
            print(first_match_path)
            return first_match_path  # 装入列表
        elif first_match_degree < second_match_degree:
            print(second_match_path)
            return second_match_path  # 装入列表
        # 匹配度相等的情况
        elif first_match_degree == second_match_degree:
            if first_match_size > second_match_size:
                print(first_match_path)
                return first_match_path  # 装入列表
            else:
                print(second_match_path)
                return second_match_path  # 装入列表
    elif len(highest_tuple) == 1:
        first_match_list = highest_tuple.pop()
        first_match_path = ((first_match_list[-1])[-1])[-2]  # 获取文件路径
        print(first_match_path)
        return first_match_path  # 装入列表
    # 未找到的情况
    if matchFlag == 0:
        failedMatch.append(musicName)
        return False


def outPutM3u(music_path_list, targetPath, file):
    """
    :param music_path_list: 成功匹配上的路径集合
    :param targetPath: 放入数据的路径
    :param file: 写入数据的文件名
    """
    # 写入新文件  防止同名的旧文件影响,从而进行重复追加
    open(targetPath + '/' + file[:file.rfind(".")] + '.m3u', 'w').close()
    targetFile = open(targetPath + '/' + file[:file.rfind(".")] + '.m3u', 'a+', encoding='UTF-8-sig')  # 指定写入的目标文件
    for success in music_path_list:
        targetFile.write(success)  # 写入目标文件中
        targetFile.write('\n')
    targetFile.close()


if __name__ == '__main__':
    failedMatch = []  # 匹配失败音乐集合
    findAndInput('./data', './data/MusicPath.txt', './m3uFile')  # './t从网易云上扒歌单,在本地配对好数据'
    failedMatch = list(dict.fromkeys(failedMatch))

    open("./data/failedMatch.txt", 'w').close()
    failedFile = open("./data/failedMatch.txt", 'a+', encoding='UTF-8-sig')

    print("数据未找到个数:", len(failedMatch))
    for i in failedMatch:
        failedFile.write(i)
        failedFile.write('\n')
        print(i)

    failedFile.close()
