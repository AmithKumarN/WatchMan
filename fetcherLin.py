import os
import pymongo
from urllib.parse import quote
import time

stream = os.popen("ifconfig -a | grep 'inet ' | awk '{print $2}' | head -n 1")
IP_ADDR = stream.read().strip()

stream = os.popen("whoami")
HOST_NAME = stream.read().strip()

client = pymongo.MongoClient("mongodb+srv://servMonitor:" + quote("a1A!b2B@") + "@cluster0.jgbeb.mongodb.net/ServerStats?retryWrites=true&w=majority")
# for database_name in client.list_database_names():  
#     print("Database - "+database_name)
collection = client.ServerStats.stats

while(1):
	stream = os.popen("date \"+%Y-%m-%d %H:%M:%S\"")
	date = stream.read().strip()
 	date = date[:10]+"T"+date[11:]+"Z"
	# print("Date: ", date)
	
	stream = os.popen("top -b -n 1 -d1 | grep 'Cpu(s)'| awk '{print $2+$4+$6}'")
	cpuUsage = stream.read().strip()
	# print("CPU Usage: ", cpuUsage)
	
	stream = os.popen("free -t")
	mem = stream.read().strip().split()
	memUsage = (int(mem[11])+int(mem[19]))*100/int(mem[18])
	memUsage = "{:.2f}".format(memUsage)
	# print("Memory Usage: ", memUsage)
	
	stream = os.popen("df -P | awk '{print $5}' | head -n 4 | tail -n 1")
	diskUsage = stream.read().strip()[:-1]
	# print("Disk Usage: ", diskUsage)
	
	
	records = {
		"ip": IP_ADDR,
		"hostname": HOST_NAME,
		"date": date,
		"cpu": int(cpuUsage),
		"memory": int(memUsage),
		"disk": int(diskUsage)
	}
	
	print(collection.insert_one(records))
	time.sleep(60)

