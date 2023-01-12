"""
@author: Duong Vu Tuan Minh
"""

import datetime
import time
import hashlib
import json
import names
from random import randint
from urllib import response
from flask import Flask, jsonify

# Part 1: Building a Blockchain
class Block:
    def __init__(self, nonce: int, previous_hash: str, len_of_chain: int):
        self.index = len_of_chain + 1
        self.timestamp = str(datetime.datetime.now())
        self.content = self.create_content()
        self.previous_hash = previous_hash
        #need update field 
        self.nonce = nonce
        
    def __str__(self) -> str:
        output = f"index = {self.index}, timestamp = {self.timestamp}, nonce = {self.nonce}, previous hash = {self.previous_hash}, content = {self.content}"
        return output
    
    def hash(self):
        return hashlib.sha256(json.dumps(str(self), sort_keys=True).encode()).hexdigest()
    
    def create_content(self):
        def create_transaction():
            sender = names.get_full_name()
            amount = randint(1, 100) * 100
            receiver = names.get_full_name()
            return f"{sender} sends {amount} coins to {receiver}"

        transactions = [create_transaction() for _ in range(3)]
        return "\r".join(transactions)
        
        
class Blockchain:
    def __init__(self):
        self.level_of_difficulty = 4
        self.chain = []
        self.create_block(1, '0')
        
    def __str__(self):
        output = "["
        for item in self.chain:
            output += str(item)
            output += "\n"
        output += "]"
        return output

    def get_list_chain(self):
        return [str(item).replace('\n', '\\n') for item in self.chain]
    
    def create_block(self, nonce: int, previous_hash: str):
        block = Block(nonce, previous_hash, len(self.chain))
        self.chain.append(block)
        return block
    
    def get_previous_block(self) -> Block:
        return self.chain[-1]
    
    def proof_of_work(self, nonvalid_new_block: Block) -> int:
        check_proof = False 
        while check_proof is False:
            hash_operation = nonvalid_new_block.hash()
            if hash_operation.startswith("0"*self.level_of_difficulty):
                check_proof = True
            else: 
                nonvalid_new_block.nonce += 1
        return hash_operation

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1
        while (block_index < len(self.chain)):
            block = self.chain[block_index]
            if block.previous_hash != previous_block.hash():
                return False
            hash_operation = block.hash()
            if not hash_operation.startswith("0"*self.level_of_difficulty):
                return False
            previous_block = block
            block_index += 1
        return True


#Part 2 - Mining our blockchain


#Create a Web App
app = Flask(__name__)


#Create a Blockchain
blockchain = Blockchain()   
    
#Getting the full blockchain
@app.route('/get_chain', methods = ["GET"])
def get_chain():
    response = {
        'chain': blockchain.get_list_chain(),
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

#Mining a new block
@app.route('/mine_block', methods = ["GET"])
def mine_block():
    last_block_in_chain = blockchain.get_previous_block()
    previous_block_hash = last_block_in_chain.hash()
    block = blockchain.create_block(1, previous_block_hash)
    new_hash = blockchain.proof_of_work(block)
    print(new_hash)
    response = {
        'message': 'Congratulations, you have just mined a new block',
        'index': block.index,
        'timestamp': block.timestamp,
        'proof': block.nonce,
        'previous_hash': block.previous_hash
    }
    return jsonify(response), 200

    
#Verify the chain is valid 
@app.route('/valid_chain', methods = ["GET"])
def is_valid():
    #try to alter chain
    #blockchain.chain[3].nonce = 100

    if blockchain.is_chain_valid():
        response = {'message': 'The chain is valid!'}
    else:
        response = {'message': 'The chain is not valid!'}
    return jsonify(response), 200

#Running the app
app.run(host = '0.0.0.0', port = 5000)