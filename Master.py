# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:30:57 2018
@author: Chinmay/Ashish
"""
import threading
import time
import subprocess

class myThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name
    def run(self):
        print("Starting "+self.name)
        subprocess.run(["python",self.name+"_Scraping.py"])
        print("Exiting thread "+self.name)

start=time.time()
monster_thread=myThread("Monster")
stepstone_thread=myThread("Stepstone")
monster_thread.start()
stepstone_thread.start()
monster_thread.join()
stepstone_thread.join()

subprocess.run(["python","SQLScriptExecution.py"])

end=time.time()
print(end-start)
print("Finished execution")

