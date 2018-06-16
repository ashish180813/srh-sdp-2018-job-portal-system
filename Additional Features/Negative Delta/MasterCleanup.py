# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 16:17:19 2018
@author: Ashish Chouhan
"""
import HelperScript 
import time
 
def cleanup_processing(db_connection):
    '''
    The function take connection as input
    and will run the SQL query on the given connection for cleanup activity
    '''
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT Unique_Job_Value FROM Job_LIST")
        Job_results = cursor.fetchall()

        for row in Job_results:
            cursor.execute("SELECT COUNT(*) FROM Job_URL_List WHERE Unique_Job_Value = '{}'".format(row[0]))
            count = cursor.fetchone()
            if count[0] == 0:
                cursor.execute("DELETE FROM Job_List WHERE Unique_Job_Value = '{}'".format(row[0]))   
    except:
        print("Error Occurred during Deleting Record from Master table")
        raise
        
    finally:
        cursor.close()
        
def main():    
    try:
        db_connection = HelperScript.connection_to_database()
        cleanup_processing(db_connection)
        db_connection.commit()
    
    except:
        db_connection.rollback()
        print("Error During Opening Connection to Database for Master File Cleanup Module")
        raise
        
    finally:
        db_connection.close()
    
if __name__ == "__main__":
    print ("Master File Cleanup Started")
    start = time.time()
    main()
    end = time.time()
    print ("Time elapsed to run the script:")
    print (end - start)
    print ("Master File Cleanup Ended")
