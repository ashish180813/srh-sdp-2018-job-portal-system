import urllib
from bs4 import BeautifulSoup
import time
import datetime
import subprocess
import threading
import multiprocessing
import HelperScript
import detailed_tech

class myThread(threading.Thread):
    def __init__(self,tech_name,city_name):
        threading.Thread.__init__(self)
        self.tech_name=tech_name
        self.city_name=city_name
    def run(self):
        print("Starting "+self.tech_name+","+self.city_name)
        get_jobs_list(self.tech_name,self.city_name)
        print("Exiting thread "+self.tech_name+","+self.city_name)

def getCities(tech,city):
    thread_list=[]
    for c in city:
        new_thread=myThread(tech,c)
        thread_list.append(new_thread)
        new_thread.start()
        time.sleep(5)
    for t in thread_list:
        t.join()
        
def get_jobs_list(tech,city):
    i = 0
    while True:
        url = 'https://www.stepstone.de/5/ergebnisliste.html?ke='+tech+'&ws='+city+'&of='+str(i)+'&ra=5'
        page=urllib.request.urlopen(url).read()
        soup=BeautifulSoup(page,'html.parser')
        try:
            soup.find('p', attrs={'class': 'm--none'})
            number_of_jobs = total_jobs(soup)
            if number_of_jobs == 0:
                break
            else:
                list_of_jobs = soup.find_all('article',
                            attrs={'class': 'job-element'
                            })[0:number_of_jobs]
        except:

            list_of_jobs = soup.find_all('article',
                        attrs={'class': 'job-element'})

        get_job_details(list_of_jobs, tech, city)

        print ('%s page completed', str(i), tech, city)

        try:

            currentPage = soup.find('span',
                        attrs={'class': 'count'}).text.strip()
            totalPages = soup.find_all('span',
                        attrs={'class': 'count'})[1].text.strip()
            if int(currentPage) >= int(totalPages):
                break
        except TypeError:
            break
        i = i + 25

def get_job_details(list_of_jobs, tech, city):
    data = []
    for job in list_of_jobs:
        try:
            job_name = job.h2.text.strip()
            company = job.find_all('div')[1].div.text.strip()
            location = job.find_all('li')[1].text.strip()
            url_job = job.find_all('div')[1].a['href']
            try:
                tech_all=tech+","+detailed_tech.find_technologies(url_job)
            except:
                tech_all=tech
        except IndexError:
            location = city
        data.append((job_name, company, location, tech_all, url_job))
    filename = "Stepstone_Scraping_"+str(datetime.date.today())+".csv"
    HelperScript.write_to_file(filename,data)

def total_jobs(a):
    total = len(a.findAll('article', attrs={'class': 'job-element'}))
    outside = len(a.findAll('article',
                  attrs={'class': 'job-element_regionalextended'}))
    recommend = len(a.findAll('article',
                    attrs={'class': 'job-element_recommended'}))
    actual = total - (outside + recommend)
    return actual

if __name__ == '__main__':
    start = time.time()
    HelperScript.check_and_deleteFile("Stepstone_Scraping_"+str(datetime.date.today())+".csv")
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
    subprocess.run(["python","Transform.py","Stepstone"])

            


			