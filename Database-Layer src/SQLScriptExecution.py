# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 11:08:58 2018
@author: Ashish Chouhan
"""

import HelperScript  
import time
 
def run_sql_file(filename, db_connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''
    try:
        file = open(filename, 'r')
        sqlfile = file.read()
        
        sqlcommands = sqlfile.split('#')
        cursor = db_connection.cursor()
        
        for command in sqlcommands:
            if len(command)==0:
                continue
            cursor.execute(command)
            
    except:
        print("Error during execution of Ingestion Query")
        raise
        
    finally:
        file.close()
        cursor.close()

def main():    
    try:
        db_connection = HelperScript.connection_to_database()
        run_sql_file("Ingestion_Script.sql", db_connection)
        db_connection.commit()
        
    except:
        db_connection.rollback()
        print("Error during Connection to Database in SQL Scripts Execution Module")
        
    finally:
        db_connection.close()
    
if __name__ == "__main__":
    print ("Ingestion into Master Files Started")
    start = time.time()
    main()
    end = time.time()
    print ("Time elapsed to run the query:")
    print (end - start)
    print ("Ingestion into Master File Ended")