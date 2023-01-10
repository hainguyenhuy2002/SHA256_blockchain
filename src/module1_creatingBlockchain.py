"""
@author: Duong Vu Tuan Minh
"""

import datetime
import time
import hashlib
import json
from urllib import response
from flask import Flask, jsonify

# Part 1: Building a Blockchain
class Block:
    def __init__(self, nonce: int, previous_hash: str, len_of_chain: int):
        self.index = len_of_chain + 1
        self.timestamp = str(datetime.datetime.now())
        self.nonce = nonce
        self.previous_hash = previous_hash
        
    def __str__(self) -> str:
        output = f"index = {self.index}, timestamp = {self.timestamp}, nonce = {self.nonce}, previous hash = {self.previous_hash}"
        return output
    
    def hash(self):
        return hashlib.sha256(json.dumps(str(self), sort_keys=True).encode()).hexdigest()
        
class Blockchain:
    def __init__(self):
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
    
    def proof_of_work(self, previous_nonce: int) -> int:
        new_nonce = 1 
        check_proof = False 
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else: 
                new_nonce += 1
        return new_nonce

    def hash(self, block: Block) -> str:
        encoded_block = hashlib.sha256(json.dumps(str(block), sort_keys=True).encode()).hexdigest()
        print(encoded_block)
        return encoded_block

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1
        while (block_index < len(self.chain)):
            block = self.chain[block_index]
            if block.previous_hash != previous_block.hash():
                return False
            previous_nonce = previous_block.nonce
            nonce = block.nonce
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
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
    last_block_nonce = last_block_in_chain.nonce
    valid_new_nonce = blockchain.proof_of_work(last_block_nonce)
    previous_hash = blockchain.hash(last_block_in_chain)
    block = blockchain.create_block(valid_new_nonce, previous_hash)
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
    if blockchain.is_chain_valid():
        response = {'message': 'The chain is valid!'}
    else:
        response = {'message': 'The chain is not valid!'}
    return jsonify(response), 200

#Running the app
app.run(host = '0.0.0.0', port = 5000)