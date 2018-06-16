# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 23:17:23 2018
@author: Chinmay/Ashish
"""
import MySQLdb
import io
import csv
from pathlib import Path
import os

def connection_to_database():
    connection =  MySQLdb.connect(host ="localhost",
                                  user ="Ashish",
                                  passwd ="A123456789",
                                  db ="final_exam_demo",
                                  use_unicode = True,
                                  charset = "utf8")
    return connection


def write_to_file(filename,data):
    with io.open(filename, "a", encoding="utf-8", newline='') as f:
        writer=csv.writer(f)
        for job_name,company_name,location,tech,job_url in data:
            writer.writerow([job_name,company_name,location,tech,job_url])
    f.close()
    
def read_from_file(filename):
    data=[]
    with io.open(filename,"r",encoding="utf-8") as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            data.append(row)
    csvfile.close()
    return data

    
def getDiff(new,old):
    str1=""
    old_list=old.split(",")
    new_list=new.split(",")
    
    for n in new_list:
        flag=False
        for o in old_list:
            if(n==o):
                flag=True
                break
        if(flag==False):
            if(len(str1)<1):
                str1=str1+n
            else:
                str1=str1+","+n
    return str1

def check_and_deleteFile(filename):
    fname=Path(os.getcwd()+"\\"+filename)
    if(fname.exists()):
        os.remove(fname)