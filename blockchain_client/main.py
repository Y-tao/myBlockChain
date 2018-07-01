
from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import session,Flask, jsonify, request, render_template
import hashlib
import dbm
import json

from sql import insertDB,queryDB,delDB,queryAllDB

from blockchain_client import Transaction

# Instantiate the DataBase
user_db='../DB/users_info'
device_db='../DB/device_info'
transaction_db='../DB/transaction_info'
block_db='../DB/block_info'

#delDB(user_db)


app = Flask(__name__)
app.secret_key='\xf1\x92Y\xdf\x8ejY\x04\x96\xb4V\x88\xfb\xfc\xb5\x18F\xa3\xee\xb9\xb9t\x01\xf0\x96'



@app.route('/')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route("/sign_out")
def sign_out():
	session.pop("username",None)
	session.clear;
	return login();

@app.route('/apply')
def apply():
	return render_template('sign-up.html')


@app.route("/check",methods=["POST","GET"])
def check():
	if request.method == "POST":
		userID=request.form.get('id')
		tempPsw=request.form.get('password').encode(encoding="utf-8")
		passWord=hashlib.md5(tempPsw).hexdigest()
		#print('%s,%s,%s'%(UserName,tempPsw,PassWord))
		value=queryDB(user_db,userID)
		if value:
			info=json.loads(value)
			print(info)
			passw=info["password"]
			if passWord == passw:
				session["userID"]=userID
				if userID == "manager":
					return """<script>location.replace("/manager");</script>"""
				else:
					return """<script>location.replace("/make/transaction");</script>"""
		return """<script>alert('studentID or password error');location.replace("/login");</script>"""


@app.route("/createUser",methods=["POST","GET"])
def createUser():
	userName=request.args.get('name')
	userID=request.args.get('id')
	tempPsw=request.args.get('password').encode(encoding="utf-8")
	userPsw=hashlib.md5(tempPsw).hexdigest()
	if userID in user_db:
		return """<script>alert('student ID exist');location.replace("/apply");</script>"""
	else:
		value={}
		value["username"]=userName
		value["password"]=userPsw
		value["device"]=[]
		value["public_key"]=""
		#value=json.dumps(value)
		value=json.dumps(value,ensure_ascii=False).encode(encoding="utf-8")
		insertDB(user_db,userID,value)
		session["userID"]=userID
		return """<script>location.replace("/key");</script>"""

@app.route('/key')
def key():
	if session.get("userID") != None:
		return render_template('./key.html')
	else:
		return login()

@app.route('/manager')
def manager():
	if session.get("userID") != None:
		return render_template('./manager.html')
	else:
		return login()

@app.route('/input_device')
def input_device():
	userID = session.get("userID")
	device={}
	deviceID=request.args.get('device_id')
	deviceName=request.args.get('device_name')
	buyTime=request.args.get('buy_time')
	device["name"]=deviceName
	device["id"]=deviceID
	device["date"]=buyTime
	device_info=json.dumps(device,ensure_ascii=False).encode(encoding="utf-8")
	md5=hashlib.md5(device_info).hexdigest()
	device["md5"]=md5
	device_info=json.dumps(device,ensure_ascii=False).encode(encoding="utf-8")
	if md5 in device_db:
		return """<script>alert('device exist');location.replace("/manager");</script>"""
	else:
		insertDB(device_db,deviceID,device_info)
		value=queryDB(user_db,userID)
		info=json.loads(value)
		info["device"].append(deviceID)
		info=json.dumps(info,ensure_ascii=False).encode(encoding="utf-8")
		insertDB(user_db,userID,info)
	    	
		return """<script>alert('submit success');location.replace("/manager");</script>"""
	


#@app.route('/index')
#def index():
#	return render_template('./index.html')

@app.route('/make/transaction')
def make_transaction():
	userID=session.get("userID")
	value=queryDB(user_db,userID)
	info=json.loads(value)
	device=info["device"]

	if userID != None:	
		users=queryAllDB(user_db)
		result=[]
		if len(users) != 0:
			for user in users:
				one={}
				one["id"]=user["id"].decode("utf-8")
				if one["id"] == userID:
					continue
				value=json.loads(user["value"])
				one["public_key"]=value["public_key"]
				one["device"]=device
				#value=queryDB(device_db,deviceID)
				#info=json.loads(value)
				#device_hash=info["md5"]
				#one["deviceID"]=deviceID
				#one["md5"]=device_hash
				result.append(one)
		print(result)
		json_value=json.dumps(result)
		#devices=[]
		#for device in device_db:
		#	d={}
		#	info=eval(device_db[device].decode("utf-8"))
		#	d['name']=info["name"]
		#	d['md5']=device.decode("utf-8")
		#	devices.append(d)
		#	print(d)
		#json_value2=json.dumps(devices)
		return render_template('./make_transaction.html',userid=userID,users=json_value)
	else:
		return login()

@app.route('/view/transactions')
def view_transaction():
	if session.get("userID") != None:
		return render_template('./view_transactions.html')
	else:
		return login()

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
	userID=session.get("userID")
	random_gen = Crypto.Random.new().read
	private_key = RSA.generate(1024, random_gen)
	public_key = private_key.publickey()
	response = {
		'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
		'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
	}
	print(userID)
	print(queryDB(user_db,str(userID)))
	value=json.loads(queryDB(user_db,userID))
	value["public_key"]=response["public_key"]
	value=json.dumps(value,ensure_ascii=False).encode(encoding="utf-8")
	insertDB(user_db,userID,value)
	#print(user_db[username])
	#user_db.close()
	#user_db.open("DB/users_info")
	#user_db=dbm.open('DB/users_info','c') 
	return jsonify(response), 200

@app.route('/generate/transaction', methods=['POST'])
def igenerate_transaction():
	
	sender_address = request.form['sender_address']
	sender_private_key = request.form['sender_private_key']
	recipient_address = request.form['address']
	value = request.form['device']

	#print('AAAAAAAAAAA')
	#print('%s,%s,%s,%s'%(sender_address,sender_private_key,recipient_address,value))

	transaction = Transaction(sender_address, sender_private_key, recipient_address, value)

	response = {'transaction': transaction.to_dict(), 'signature': transaction.sign_transaction()}
	
	#print(response)
	
	return jsonify(response), 200


@app.route('/searchDevice',methods=['POST'])
def searchDevice():
	data=json.loads(request.form.get('data'))
	deviceID=data['id']
	#print(deviceID)
	trans=queryAllDB(transaction_db)
	t=[]
	for item in trans:
		key=str(item["id"], encoding='utf-8')
		if key[:key.find(':')] == deviceID:
			t.append(item["value"])
	#print(t)
	result=[]
	for item in t:
		item=json.loads(item)
		block_hash=item["block_hash"]
		number=item["transaction_number"]
		block_num=queryDB(block_db,block_hash)
		#print(block_num)
		if block_num:
			one={}
			filename="../blocks/blk"+block_num+".dat"
			fp=open(filename,"rb")
			value=json.loads(fp.read())
			fp.close()
			#print(value)
			one["sender"]=value["transactions"][int(number)]["sender"]
			one["receiver"]=value["transactions"][int(number)]["receive"]
			one["ctime1"]=value["transactions"][int(number)]["ctime"]
			one["ctime2"]=value["ctime"]
			result.append(one)
	result=sorted(result,key=lambda x:x["ctime2"])
	print(result)
	return jsonify(result), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port,debug=True)

	#user_db.close()
	#device_db.close()
