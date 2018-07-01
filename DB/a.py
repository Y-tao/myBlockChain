#!/usr/bin/python3 

import dbm
from sql import insertDB,queryDB,delDB,queryAllDB

user_db='../DB/users_info'
device_db='../DB/device_info'
transaction_db='../DB/transaction_info'
block_db='../DB/block_info'



if __name__=='__main__':
	delDB(user_db)
	delDB(device_db)
	delDB(transaction_db)
	delDB(block_db)
	#value=queryAllDB(block_db)
	#print(value)



	exit(0)

