#!/usr/bin/python3 
import dbm
from sql import insertDB,queryDB


def deleteall(db):
	if db is not None:
		for key in db.keys():
			del db[key]
			#print(db[key])

def insert(db_name,key,value):
	db=dbm.open(db_name,'c')
	db[key]=value
	db.close()

def query(db_name,key):
	db=dbm.open(db_name,'c')
	return db[key].decode("utf-8")
	db.close()


#user_db=dbm.open('DB/users_info','c') 
#device_db=dbm.open('DB/device_info','c')

#user_db['test']='#'*10000


#deleteall(user_db)
#deleteall(device_db)

#user_db.close() 
#device_db.close()


if __name__=="__main__":
	insertDB('./users','test','#'*1000)
	print(queryDB('./users','test2'))	
