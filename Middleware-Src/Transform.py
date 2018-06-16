import time
import sys
import subprocess
import datetime
import HelperScript
from googletrans import Translator

def check_appostrophy(row):
    new_row=[]
    for r in row:
        if("'" in r):
            r=r.replace("'","$")
            new_row.append(r)
        else:
            new_row.append(r)
    return new_row

def check_case(row1,row2):
	count=0
	for a,b in zip(row1,row2):
		a.replace('\ufeff','')
		b.replace('\ufeff','')
		if(a.lower()==b.lower() or b.lower() in a.lower() or a.lower() in b):
			count=count+1
	if(count>=3):
		return True
	else:
		return False

def find_position(data,row):
    i=0
    for r in data:
        if(check_case(r[0:3],row[0:3])):
            return i
        i=i+1
    return -1

def translate_text(text):
    translator=Translator()
    result=translator.translate(text,dest='en')
    return result.text


print(sys.argv[1] + " JCL Munging Started ")
start=time.time()
HelperScript.check_and_deleteFile(sys.argv[1]+"_Munging_"+str(datetime.date.today())+".csv")
filename=sys.argv[1]+"_Scraping_"+str(datetime.date.today())+".csv"
scraped_data=[]
scraped_data=HelperScript.read_from_file(filename)
merged_data=[]
for row in scraped_data:
    position=find_position(merged_data,row)
    if(position==-1):
        merged_data.append(row)
    else:
        merged_data[position][3]=str(merged_data[position][3])+','+HelperScript.getDiff(merged_data[position][3],row[3])

cleaned_data=[]
for row in merged_data:
    cleaned_row=check_appostrophy(row)
    cleaned_data.append(cleaned_row)

translated_data=[]
for row in cleaned_data:
    translated_row=[]
    for r in row:
        try:
            translated_text=translate_text(r)
        except ConnectionError:
            translated_text=r
        translated_row.append(translated_text)
    translated_data.append(translated_row)

filename=sys.argv[1]+"_Munging_"+str(datetime.date.today())+".csv"        
HelperScript.write_to_file(filename,translated_data)
end=time.time()
print(sys.argv[1] + " JCL Munging Ended : " + str(end-start))
subprocess.run(["python","Compare.py",sys.argv[1]])