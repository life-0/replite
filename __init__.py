""" -*- coding: utf-8 -*-  
 @Author : life-0 
 @File : mp3.py
 @Time : 2021/5/3 11:24
 TODO @desc:

"""
import os
import re

allFileNum = 0
# 所有文件名以及路径地址
filePathList = {}


def printPath(level, path):
    global filePathList
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(文件名和文件夹名)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if os.path.isdir(path + '/' + f):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if f[0] == '.':
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if os.path.isfile(path + '/' + f):
            # 添加文件
            fileList.append(path + f)
            # print(re.split(r'\..*', f))
            # 当一个标志使用，文件夹列表第一个级别不打印
            # 添加成字典模式: 歌名 : 路径
            filePathList[f] = path + f

    i_dl = 0
    for dl in dirList:
        if i_dl == 0:
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            # print('-' * (int(dirList[0])), dl)
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + dl + '/')


# 文件写入
def writeFile(fileAndPathList):
    global allFileNum
    # 写入新文件
    open("./data/MusicPath.txt", 'w').close()
    newFile = open("data/MusicPath.txt", 'a+', encoding="UTF-8")  # MusicPath.txt文件，没有则创建
    # 通过遍历keys()来获取所有的键
    for k, v in fileAndPathList.items():
        size = os.path.getsize(v)
        size = size / (1024 * 1024)
        # 查看结果
        print(k[:k.rfind('.')] + "=" + v + "=" + size.__str__())
        # print(f[:f.rfind('.')])
        newFile.write(k[:k.rfind('.')] + "=" + v + "=" + size.__str__())
        newFile.write('\n')  # 实现换行的功能
        allFileNum = allFileNum + 1

    newFile.close()


if __name__ == '__main__':
    printPath(1, 'F:/缓存音乐/')
    writeFile(filePathList)
    print('总文件数 =', allFileNum)
