import sys
import subprocess
import datetime
from pathlib import Path
import os
import HelperScript
HelperScript.check_and_deleteFile(sys.argv[1]+"_delta.csv")
todayfile=sys.argv[1]+"_Munging_"+str(datetime.date.today())+".csv"
yesterdayfile=sys.argv[1]+"_Munging_"+str(datetime.date.today()-datetime.timedelta(1))+".csv"
fname=Path(os.getcwd()+"\\"+yesterdayfile)
if(fname.exists()):
    data_old=HelperScript.read_from_file(yesterdayfile)
    data_new=HelperScript.read_from_file(todayfile)
    delta=[]
    for row_new in data_new:
        flag=0
        for row_old in data_old:
            if(row_new==row_old):
                flag=1
                break
            else:
                if(row_new[0:3]==row_old[0:3]):
                    row_new[3]=HelperScript.getDiff(row_new[3],row_old[3])
                    break
        if flag==0:
            delta.append(row_new)
    filename=sys.argv[1]+"_delta.csv"
    HelperScript.write_to_file(filename,delta)
else:
    os.rename(todayfile,sys.argv[1]+"_delta.csv")
subprocess.run(["python","DeltatoSQL.py",sys.argv[1]])

    
