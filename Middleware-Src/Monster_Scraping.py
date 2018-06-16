# -*- coding: utf-8 -*- 
"""
Created on Tue May 15 23:44:41 2018

@author: Chinmay
"""
import urllib
import HelperScript
from bs4 import BeautifulSoup
import subprocess
import time
import datetime
import threading
import detailed_tech
import multiprocessing
class myThread(threading.Thread):
    def __init__(self,tech_name,city_name):
        threading.Thread.__init__(self)
        self.tech_name=tech_name
        self.city_name=city_name
    def run(self):
        print("Starting "+self.tech_name+","+self.city_name)
        get_jobs_list(self.tech_name,self.city_name)
        print("Exiting thread "+self.tech_name+","+self.city_name)

def get_jobs_list(tech,city):
    i=1
    while(True):
        try:
            url='https://www.monster.de/jobs/suche/?q='+tech+'&where='+city+'&cy=de&rad=2&page='+str(i)
            page=urllib.request.urlopen(url).read()
            soup=BeautifulSoup(page,'html.parser')
            stop_text=soup.find('h1').text.strip()
            if stop_text[0:6] == "Leider":
                break
            list_of_jobs=soup.find_all('div',attrs={'class':"primary"})
            get_job_details(list_of_jobs,tech,city)
            print("%s page completed",str(i),tech,city)
            i=i+1
        except:
            break
    
def getCities(tech,city):
    thread_list=[]
    for c in city:
        new_thread=myThread(tech,c)
        thread_list.append(new_thread)
        new_thread.start()
        time.sleep(5)
    for t in thread_list:
        t.join()

def get_job_details(list_of_jobs,tech,city):
    data=[]
    for job in list_of_jobs:
        try:
            job_name=job.find("div",attrs={'class':'js_result_details-left'}).div.h2.a.text.strip()
            job_url=job.find("div",attrs={'class':'js_result_details-left'}).div.h2.a["href"]
            company_name=job.find("div",attrs={'class':'js_result_details-left'}).span.text.strip()
            location=job.find("div",attrs={'class':'js_result_details-left'}).p.text.strip()
            try:
                tech_all=tech+","+detailed_tech.find_technologies(job_url)
            except:
                tech_all=tech
        except AttributeError as e:
            location=city
        data.append((job_name,company_name,location,tech_all,job_url))
    filename="Monster_Scraping_"+str(datetime.date.today())+".csv"
    HelperScript.write_to_file(filename,data)
    

if __name__=="__main__":
    start=time.time()
    HelperScript.check_and_deleteFile("Monster_Scraping_"+str(datetime.date.today())+".csv")
    tech=[]
    city=[]
    tech_city=HelperScript.read_from_file('tech_city.csv')
    for t,c in tech_city:
        tech.append(t)
        city.append(c)
    process_list=[]
    for t in tech:
        new_process=multiprocessing.Process(target=getCities,args=(t,city))
        process_list.append(new_process)
        new_process.start()
        time.sleep(5)
    for p in process_list:
        p.join()
    end=time.time()        
    print(end-start)
    subprocess.run(["python","Transform.py","Monster"])
        
            
    
    
        
        
        
            
        
        
        
           
        
        
		
			
		
			
