import os
import pymongo
from urllib.parse import quote
import time
import psutil
import platform
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://servMonitor:" + quote("a1A!b2B@") + "@cluster0.jgbeb.mongodb.net/ServerStats?retryWrites=true&w=majority")
# for database_name in client.list_database_names():  
#     print("Database - "+database_name)
collection = client.ServerStats.stats

IP_ADDR = ""
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for address in if_addrs['Wi-Fi']:
    if str(address.family) == 'AddressFamily.AF_INET':
        IP_ADDR = address.address
# print("IP Address: ", IP_ADDR)

uname = platform.uname()
HOST_NAME = str(uname.node)
# print("Host Name: ", HOST_NAME)

while(1):
    
    CPU_USAGE = psutil.cpu_percent()
    # print("CPU Usage:", CPU_USAGE)

    MEM_USAGE = psutil.virtual_memory().percent
    # print("Memory Usage:", MEM_USAGE)

    disk_total = 0
    disk_used = 0
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        disk_total += partition_usage.total
        disk_used += partition_usage.used
        
    DISK_USAGE = round((disk_used/disk_total)*100, 1)
    # print("Disk Usage: ", DISK_USAGE)

    date = str(datetime.now())
    date = date[:10]+"T"+date[11:19]+"Z"
    # print(date)
    
    records = {
		"ip": IP_ADDR,
		"hostname": HOST_NAME,
		"date": date,
		"cpu": int(CPU_USAGE),
		"memory": int(MEM_USAGE),
		"disk": int(DISK_USAGE)
	}
	
    # print(collection.insert_one(records))
    collection.insert_one(records)
    time.sleep(60)
