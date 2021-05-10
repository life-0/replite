""" -*- coding: utf-8 -*-  
 @Author : life-0 
 @File : example.py 
 @Time : 2021/5/6 16:04
 TODO @desc: 
         列表测试
"""
import re

lists = ['张学友', '刘德华', '33123', '黎明', '郭富城'];
print(lists[0:-2])
string_ = "if... - DAISHI DANCE if... - DAISHI DANCE.ape"
string_.replace(u'\xa0', ' ')
print(string_)
string_=re.split(r'[ -]',"".join(string_.split()).lower())
print(string_)