USE final_exam_demo;#
DELETE FROM Job_List;#
DELETE FROM Job_URL_List;#
INSERT INTO Job_List 
(SELECT CONCAT(TRIM(Job_Title),TRIM(COMPANY_NAME),TRIM(JOb_LOCATION), TRIM(TECHNOLOGY)) As Unique_Job_value,Job_Title, Company_Name, Job_Location, Technology FROM Monster_Table 
UNION
SELECT CONCAT(TRIM(Job_Title),TRIM(COMPANY_NAME),TRIM(JOb_LOCATION), TRIM(TECHNOLOGY)) As Unique_Job_value,Job_Title, Company_Name, Job_Location, Technology FROM Stepstone_Table
);#
INSERT INTO Job_URL_List
(SELECT CONCAT(TRIM(Job_Title),TRIM(COMPANY_NAME),TRIM(JOb_LOCATION), TRIM(TECHNOLOGY)) As Unique_Job_value, Job_Url FROM Monster_Table 
UNION ALL
SELECT CONCAT(TRIM(Job_Title),TRIM(COMPANY_NAME),TRIM(JOb_LOCATION), TRIM(TECHNOLOGY)) As Unique_Job_value, Job_Url FROM Stepstone_Table
);#