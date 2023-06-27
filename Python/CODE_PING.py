

import os

from Info_connection import ip_v4 ,url ,db ,username,password

response = os.system("ping -c 1 " + ip_v4)

while response != 0:
    response = os.system("ping -c 1 " + ip_v4)
    if response == 0:
        pingstatus = "Network Active"
        print( '\n' ,'Tu es co Simon   OH OUI  OH OUI  OH OUI OH OUI  OH OUI')
        Connection = True
        break
    else:
        pingstatus = "Network Error"
        print( '\n' ,'Error de connection Simon')
        Connection = False
        

