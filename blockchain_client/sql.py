import dbm


def insertDB(db_name,key,value):
	db=dbm.open(db_name,'c')
	db[key]=value
	db.close()

def queryDB(db_name,key):
	db=dbm.open(db_name,'c')
	if key in db:
		value=db[key].decode("utf-8")
	else:
		value=None
	db.close()
	return value

def delDB(db_name):
	db=dbm.open(db_name,'c')
	for key in db:
		del(db[key])
	

def queryAllDB(db_name):
	value=[]
	db=dbm.open(db_name,'c')
	for key in db:
		one={}
		one["id"]=key
		one["value"]=db[key].decode('utf-8')
		value.append(one)
	db.close()
	return value
