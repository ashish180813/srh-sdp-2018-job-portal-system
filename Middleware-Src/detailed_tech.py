# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 10:38:17 2018

@author: Chinmay
"""


import HelperScript
import requests

def find_technologies(url):
    content=requests.get(url)
    tech=HelperScript.read_from_file('Technologies.csv')   
    str1=''
    for l in tech[0]:
        if(l in content.text):
            str1=str1+l+","
    return str1


