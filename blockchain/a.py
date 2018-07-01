#!/usr/bin/python3 
import json

if __name__=='__main__':
	dic={
			"name":"123",
			"score":100
		}
	fp=open("./a.bat","wb")
	fp.write(json.dumps(dic).encode('UTF-8'))
	#json.dump(dic, open('./a.bat','wb'))   

	fp=open("./a.bat","rb")
	#line=fp.readline()
	value=json.loads(fp.read())
	print(value)

	#res=json.load(open('./a.bat','rb'))
	#print(res)
	fp.close()

	exit(0)
