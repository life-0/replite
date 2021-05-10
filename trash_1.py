""" -*- coding: utf-8 -*-  
 @Author : life-0 
 @File : trash_1.py 
 @Time : 2021/5/10 14:54
 TODO @desc: 
                
"""
list1 = ['a','b','c','d']
list2 = ['a','b','e']

list1_not_in_list2 = [i for i in list1 if i not in list2]
print(list1_not_in_list2)
list2_not_in_lis1 = [i for i in list2 if i not in list1]
print(list2_not_in_lis1)
