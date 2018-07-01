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

