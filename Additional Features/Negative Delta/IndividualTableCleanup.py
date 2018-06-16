# -*- coding: utf-8 -*-
"""
Created on Wed Jun  13 23:08:58 2018

@author: Ashish Chouhan
"""

import HelperScript  
import time
import csv
import sys
 
def cleanup_query_execution(cursor,csv_file,filename):
    try:
        csv_file_read = csv.reader(csv_file)
        for row in csv_file_read:
            
            cursor.execute("SELECT Technology FROM {} WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}' AND Technology LIKE '%{}%'".format(filename,row[0],row[1],row[2],row[3]))
            currentTechnology = cursor.fetchone()
            
            techList = currentTechnology[0].split(',')
            removalList = row[3].split(',')
            
            if (len(techList) == len(removalList)):
                result = cursor.execute("DELETE FROM {} WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}' AND Technology = '{}'".format(filename,row[0],row[1],row[2],row[3]))
                
                if result == 1:
                    cursor.execute("SELECT Unique_Job_Value FROM Job_List WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}' AND Technology = '{}'".format(row[0],row[1],row[2],row[3]))
                    KeyValue = cursor.fetchone()
                    cursor.execute("DELETE FROM Job_URL_List WHERE Unique_Job_Value = '{}' AND Job_URL = '{}'".format(KeyValue[0],row[4]))
                
            elif (len(techList) > len(removalList)):
                techToRemove = row[3].replace(",", "")
                techList.remove(techToRemove)
                updatedTechnology = ','.join(techList)
                
                result = cursor.execute("UPDATE {} SET Technology = '{}' WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}'".format(filename,updatedTechnology,row[0],row[1],row[2]))
                
                if result == 1:
                    result = cursor.execute("UPDATE Job_List SET Technology = '{}' WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}'".format(filename,updatedTechnology,row[0],row[1],row[2]))
            
    except:
        print("Error during execution of Delete Query for Indvidual Table")
        raise
               
def individual_cleanup_processing(db_connection):
    '''
    The function take a connection as input
    and will run the SQL query on the given connection to cleanup the individual table  
    '''    
    try:
        
        entry_parameter =sys.argv[1]
         
        cursor = db_connection.cursor()
        csv_file_name = entry_parameter +"_Negdelta.csv"
        
        if entry_parameter == 'Monster':
            csv_file = open(csv_file_name,'r', encoding = "latin-1")
            filename = entry_parameter + '_Table'
        
        if entry_parameter == 'Stepstone':
            csv_file = open(csv_file_name,'r', encoding = "latin-1")
            filename = entry_parameter + '_Table'
        
        cleanup_query_execution(cursor,csv_file,filename) 
            
    except:
        print("Error During Cursor Setup for Individual Table Cleanup Script")
        raise
        
    finally:
        csv_file.close()
        cursor.close()

def main():    
    try:
        db_connection = HelperScript.connection_to_database()
        individual_cleanup_processing(db_connection)
        db_connection.commit()
        
    except:
        db_connection.rollback()
        print("Error during Connection to Database in Individual Table Cleanup Execution Module")
        
    finally:
        db_connection.close()
    
if __name__ == "__main__":
    print(sys.argv[1] + " SQL Table Cleanup Started.")
    start_time = time.time()
    main()
    end_time = time.time()
    print ("Time elapsed to run the query:")
    print (end_time - start_time)
    print(sys.argv[1] + " SQL Table Cleanup Ended.")