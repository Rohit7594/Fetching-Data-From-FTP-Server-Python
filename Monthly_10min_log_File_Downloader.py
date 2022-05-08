from ftplib import FTP
import os
from datetime import date, timedelta

# Line to find the total days or last day of the previous month.
last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)


lastday=int(last_day_of_prev_month.strftime('%d'))
month=last_day_of_prev_month.strftime('%m')
year=int(last_day_of_prev_month.strftime('%Y'))

# Host details stored in dictionary to access it easliy with the help of key/host name(In my case its wind turbine names).
turbine_ips={"WHR":"host ip address","Haspielaw":"host ip address","Blaencilgoed":"host ip address",
             "Redlands":"host ip address","JJ":"host ip address","Heathlands":"host ip address"}

turbine_usrnm={"WHR":"username","Haspielaw":"username","Blaencilgoed":"username",
               "Redlands":"username","JJ":"username","Heathlands":"username"}

turbine_pw={"WHR":"password","Haspielaw":"password","Blaencilgoed":"password",
            "Redlands":"password","JJ":"password","Heathlands":"password"}

# Defining Fuction to download single file for previous month from particular folder.
# In my case file name is day_log_04_2022.csv from daylog folder.
def daylogs(turbine_nm):
    
    # Changing directory to the target folder PW_data to download file.
    # You can write your target folder path, where you want to download the file.
    os.chdir("C:/Users/r.saroj/Desktop/PD/Data Science/Rough/PW_data/{}".format(turbine_nm))
    
    # You can write your target folder path.
    daylog_dir_name='/cfc0/PW_Data/DAY_LOGS'
    # Changing directory on FTP to select the file from DAY_LOGS folder.
    ftp.cwd(daylog_dir_name)

    # file name ex: day_log_04_2022.csv
    daylog_startnm=' day_log_'
    
    # Since my target file name keeps changing each month because it includes month and year in it.
    daylog_file_name=daylog_startnm + str(month)+'_'+str(year)+'.csv'
    
    # It will download your file as per you specified name.(Note change directory before this step as I have done above)
    file=open(daylog_file_name, "wb")
    ftp.retrbinary("RETR"+ daylog_file_name, file.write)

# Defining Fuction to download multiple file for previous month from particular folder.
# In my case file name for previou month is varying from 10min_log_1_04.csv to 10min_log_30_04.csv.
def _10minlogs(turbine_nm):
    
    # Changing directory to the target folder PW_data to download file.
    # You can write your target folder path, where you want to download the file.
    os.chdir('C:/Users/r.saroj/Desktop/PD/Data Science/Rough/PW_data/{}/10min'.format(turbine_nm))
    _10min_dir_name='/cfc0/PW_Data/10min_logs'
    ftp.cwd(_10min_dir_name)

    # file name ex: 10min_log_1_04.csv
    _10min_startnm=' 10min_log_'
    for day in range(1,lastday+1):
        _10min_file_name=_10min_startnm + str(day) + '_' + str(month) + '.csv'
        file=open(_10min_file_name, "wb")
        ftp.retrbinary("RETR"+ _10min_file_name, file.write)
    # Closing the connection.   
    ftp.close() 


# Executing it by taking turbing name as an input. 
turbine=input("""Type turbine name form the list("WHR","Haspielaw","Blaencilgoed","Redlands","JJ","Heathlands"): """).split(",")

# Using for loop to loop around multiple turbine in my case as per input given. 
for name in turbine:
    # fetching data from turbine_ips dictionary for particular turbine 
    ip_=turbine_ips[name]
    # fetching data from turbine_usrnm dictionary for particular turbine 
    usrnm_=turbine_usrnm[name]
    # fetching data from turbine_pw dictionary for particular turbine 
    pw_=turbine_pw[name]
    
    # feeding ip/host address to the FTP funtion
    ftp=FTP(ip_)
    # Setting Transfer mode to Active, By default it is set to Passive.(In my case it wasn't working with Passive setting)
    ftp.set_pasv(False)
    # logging into the host
    ftp.login(usrnm_,pw_)
    
    # Calling function
    daylogs(name)
    _10minlogs(name)
