
from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from datetime import datetime

import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from blockchain import *
import dbm
from sql import insertDB,queryDB,delDB


# Instantiate the DataBase
user_db='../DB/users_info'
device_db='../DB/device_info'
transaction_db='../DB/transaction_info'
block_db='../DB/block_info'


# Instantiate the Node
app = Flask(__name__)
CORS(app)

# Instantiate the Blockchain
blockchain = Blockchain()



@app.route('/')


@app.route('/index')
def index():
	return render_template('./index.html')


@app.route('/configure')
def configure():
    return render_template('./configure.html')



@app.route('/transactions/new', methods=['POST'])
def new_transaction():
	values = request.form
	print(values)	
	# Check that the required fields are in the POST'ed data
	required = ['sender_address', 'recipient_address', 'amount','signature']
	#if not all(k in values for k in required):
	#	return 'Missing values', 400
	# Create a new Transaction
	
	#valid Transaction,so delete deviceID
	deviceID=values['amount']
	senderID=values['senderID']
	receiverID=values['receiverID']
	#print('%s->%s:%s'%(senderID,receiverID,deviceID))
	
	transaction_result = blockchain.submit_transaction(values['sender_address'],\
			values['recipient_address'], values['amount'], values['signature'],\
			senderID,receiverID)
	print(transaction_result)


	if transaction_result == False:
		response = {'message': 'Invalid Transaction!'}
		return jsonify(response), 406
	else:

		#sender delete device
		value=queryDB(user_db,senderID)
		info=json.loads(value)
		print(info["device"])
		info["device"].remove(deviceID)
		info=json.dumps(info,ensure_ascii=False).encode(encoding="utf-8")
		insertDB(user_db,senderID,info)
		
		
		#receiver append device
		value=queryDB(user_db,receiverID)
		info=json.loads(value)
		print(info["device"])
		info["device"].append(deviceID)
		info=json.dumps(info,ensure_ascii=False).encode(encoding="utf-8")
		insertDB(user_db,receiverID,info)
		
	

		response = {'message': 'Transaction will be added to Block '+ str(transaction_result)}
		return jsonify(response), 201

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    #Get transactions from transactions pool
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.chain[-1]
    nonce = blockchain.proof_of_work()

    # We must receive a reward for finding the proof.
    
	#blockchain.submit_transaction(sender_address=MINING_SENDER, recipient_address=blockchain.node_id, value=MINING_REWARD, signature="")

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)
	
    current_hash=blockchain.hash(block)
	
	
	#save transactions info
    for i in range(len(block["transactions"])):
        trans={}
        trans["block_hash"]=current_hash
        trans["transaction_number"]=i
        trans_info=json.dumps(trans,ensure_ascii=False).encode(encoding="utf-8")
        md5=hashlib.md5(trans_info).hexdigest()
        deviceID=block["transactions"][i]["value"]
        print(deviceID)
        key=str(deviceID)+":"+str(md5)
        insertDB(transaction_db,key,trans_info)
        print(block["transactions"][i])

	#save block info
    key=current_hash
    index=str(block['block_number']).zfill(5)
    insertDB(block_db,key,index)


    response = {
        'message': "New Block Forged",
        'block_number': block['block_number'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash'],
		'ctime':datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
	
	#save bat file
    filename="../blocks/blk"+index +".dat"
    fp=open(filename,'wb')
    fp.write(json.dumps(response).encode('UTF-8'))
    fp.close()

    
    return jsonify(response), 200



@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.form
    nodes = values.get('nodes').replace(" ", "").split(',')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': [node for node in blockchain.nodes],
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
	
	







