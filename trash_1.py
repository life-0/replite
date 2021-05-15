""" -*- coding: utf-8 -*-  
 @Author : life-0 
 @File : trash_1.py 
 @Time : 2021/5/10 14:54
 TODO @desc: 
                
"""
import re
import difflib

list1 = ['a', 'b', 'c', 'd']
list2 = ['a', 'b', 'e']

list1_not_in_list2 = [i for i in list1 if i not in list2]
print(list1_not_in_list2)
list2_not_in_lis1 = [i for i in list2 if i not in list1]
print(list2_not_in_lis1)
str_1 = "书hi(45646)(翻自矶村由纪子）333（Piano ver）（我）4{564}《无涯》(樱散零乱)1 是 P.I.A.N.O.Reno&&《无涯》&vation.-DAISHI/DANCE/吉田兄弟 &:_\\/- 姐妹"
str_2 = "风居住的街道(翻自矶村由纪子）333（Piano ver）-饭碗的彼岸"
print(re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "", str_1))
#
print(re.sub(u"\\(.*?）|", "", str_2))
# match_music = musicName[:musicName.find('-')]  # 从左往右 只要到第一个"-" 视为歌名
# match_author = musicName[musicName.rfind('-'):]  # 从右往左 只要到第一个"-" 视为作者
# match_author_music = match_music + match_author  # 匹配值: 歌名-作者
str_3 = "The Nights (UK Version) - Avicii"
str_4 = '粘心 - 风小筝'
str_5 = '上心 - 郑欣宜'

str_3 = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "", str_3)
str_4 = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "", str_4)
str_5 = re.sub(u"\\(.*?\\)|\\(.*?）|\\（.*?\\)|\\{.*?}|\\[.*?]|（.*?）|《.*?》|\s|/|\.|&|\\\|:|_", "", str_5)

str_3_split = re.split(r'[\s.、&:_\\/ ()（）-]', str_3)
str_4_split = re.split(r'[\s.、&:_\\/ ()（）-]', str_4)

Degree = 0  # 匹配成功个数
print(difflib.SequenceMatcher(None, str_4.lower(), str_5.lower()).ratio())

for matched in str_3_split:
    for match in str_4_split:
        if difflib.SequenceMatcher(None, matched.lower(), match.lower()).quick_ratio() > 0.85:
            Degree += 1
print(Degree)
# matchValue = difflib.SequenceMatcher(None, str_4.lower(),
#                                      str_3.lower()).quick_ratio()
# print(matchValue)

"""
TheNights-AviciiNicholasFurlong
The Nights (UK Version) - Avicii=F:/缓存音乐/Music1/The Nights (UK Version) - Avicii.flac=22.01817035675049
WakeMeUp-AviciiAloeBlacc
Wake Me Up - Avicii=F:/缓存音乐/Music1/Wake Me Up - Avicii.flac=30.364601135253906

PIANORenovation-DAISHIDANCE吉田兄弟

Champion-BarnsCourtney
Champion=F:/缓存音乐/Music1/Champion.mp3=2.906047821044922
Centuries-FallOutBoy
Centuries.mp3=F:/缓存音乐/Music1/Centuries.mp3=8.71359920501709
友谊之光-玛莉亚
友谊之光 - Maria.flac=F:/缓存音乐/Music1/友谊之光 - Maria.flac=11.279719352722168
风居住的街道(翻自矶村由纪子）-饭碗的彼岸
饭碗的彼岸 - 风居住的街道（Piano ver）.mp3=F:/缓存音乐/Music1/饭碗的彼岸 - 风居住的街道（Piano ver）.mp3=10.941781997680664
防弹少年团-春日中文改词版-FrankJiang
Frank_Jiang _SS_ROU AEllse - 防弹少年团 - 春日(feat. _SS_ROU)(FRANKOWO Remix)中文改词版.mp3=F:/缓存音乐/Music1/Frank_Jiang _SS_ROU AEllse - 防弹少年团 - 春日(feat. _SS_ROU)(FRANKOWO Remix)中文改词版.mp3=9.155595779418945

刚好遇见你-风小筝
青玉案-云の泣
"""
key_value = {}
key_value[2] = [56, 'sjid', 55]
key_value[1] = [2, 'sj56465', 33]
key_value[5] = [12, '654654', 1]
key_value[4] = [24, 'sadas', 10]
key_value[6] = [18, '546', 16]
key_value[3] = [323, 'sadsada', 13]
print(key_value.values())
print(max(key_value.values())[0])
if 0.46516 > 0.32654894198:
    print("123")
