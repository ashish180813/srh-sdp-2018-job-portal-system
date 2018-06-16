# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 09:17:39 2018

@author: Ashish Chouhan
"""
import HelperScript
import csv
import sys
import time

def select_query(cursor,queryParameter):

    try:
        selectParameter = queryParameter[0]
        filename = queryParameter[1]
        if (len(queryParameter) == 2):
            cursor.execute("SELECT {} FROM {}".format(selectParameter,filename))
        else:
            values = queryParameter[2]
            cursor.execute("SELECT {} FROM {} WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}'".format(selectParameter,filename,values[0],values[1],values[2]))
        
        return cursor
    
    except:
        print("Error While Selecting Record from Database")
        raise

def update_query(cursor,queryParameter):

    try:
        filename = queryParameter[0]
        newTechnologyValue = queryParameter[1]
        values = queryParameter[2]
        cursor.execute("UPDATE {} SET Technology = '{}' WHERE Job_Title = '{}' AND Company_Name = '{}' AND Job_Location = '{}'".format(filename,newTechnologyValue,values[0],values[1],values[2]))
        
    except:
        print("Error While Updating Record in Database")
        raise

def insert_query(cursor,queryParameter):

    try:
        filename = queryParameter[0]
        values = queryParameter[1]
        cursor.execute("INSERT INTO {} VALUES ('{}', '{}', '{}', '{}', '{}')".format(filename,values[0],values[1],values[2],values[3],values[4]))
        
    except:
        print("Error While Inserting Record in Database")
        raise
        
def inserting_record_execution(cursor,csv_file,filename):
    
    try:
        csv_file_read = csv.reader(csv_file)
        queryParameter = []
        queryParameter.insert(0,'COUNT(*)')
        queryParameter.insert(1,filename)
        newCursor = select_query(cursor,queryParameter)
        
        filecount = newCursor.fetchone()
        
        if filecount[0] == 0:
            
            for row in csv_file_read:
                queryParameter = []
                queryParameter.insert(0,filename)
                queryParameter.insert(1,row)
                insert_query(cursor,queryParameter)
               
        else:
            for row in csv_file_read:
                queryParameter = []
                queryParameter.insert(0,'COUNT(*),Technology')
                queryParameter.insert(1,filename)
                queryParameter.insert(2,row)
                newCursor = select_query(cursor,queryParameter)
                record = newCursor.fetchone()
                
                if record[0] == 0:
                    queryParameter = []
                    queryParameter.insert(0,filename)
                    queryParameter.insert(1,row)
                    insert_query(cursor,queryParameter)
                else:
                    queryParameter = []
                    updatedTechnology = record[1] + row[3] + ','
                    queryParameter.insert(0,filename)
                    queryParameter.insert(1,updatedTechnology)
                    queryParameter.insert(row)
                    update_query(cursor,queryParameter)
    except:
        print("Error while inserting records in Database")
        raise
               
def Deltarecord_SQLDatabase_processing(db_connection):
    '''
    The function take a connection as input
    and will execute the script inorder to insert record in database 
    '''
    try:
        entry_parameter = sys.argv[1]
        
        cursor = db_connection.cursor()
        csv_file_name = entry_parameter +"_delta.csv"
        
        if entry_parameter == 'Monster':
            csv_file = open(csv_file_name,'r', encoding = "latin-1")
            filename = entry_parameter + '_Table'
        
        if entry_parameter == 'Stepstone':
            csv_file = open(csv_file_name,'r', encoding = "latin-1")
            filename = entry_parameter + '_Table'
        
        inserting_record_execution(cursor,csv_file,filename)            
            
    except:
        print("Error During Cursor Setup for Delta to SQL Database Script")
        raise
        
    finally:
        csv_file.close()
        cursor.close()

def main():    
    try:
        db_connection = HelperScript.connection_to_database()
        Deltarecord_SQLDatabase_processing(db_connection)
        db_connection.commit()
        
    except:
        db_connection.rollback()
        print("Error during Connection to Database in Delta to SQL Database Module")
        
    finally:
        db_connection.close()
    
if __name__ == "__main__":
    
    print(sys.argv[1] + " SQL Table Ingestion Started.")
    start_time = time.time()
    main()
    end_time = time.time()
    print ("Time elapsed to run the query:")
    print (end_time - start_time)
    print(sys.argv[1] + " SQL Table Ingestion Ended.")
    