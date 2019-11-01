from hashlib import sha256
import time
class Block:
     
    def __init__(self,index,timestamp,data,previousHash=""):
        
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previousHash = previousHash
        self.nonce = 0 //代表当前计算了多少次hash计算
        self.hash = self.calculateHash()
        
    
    def calculateHash(self):
        plainData = str(self.index)+str(self.timestamp)+str(self.data)+str(self.nonce)
        return sha256(plainData.encode('utf-8')).hexdigest()
    #挖矿 difficulty代表复杂度 表示前difficulty位都为0才算成功
    def minerBlock(self,difficulty):
        while(self.hash[0:difficulty]!=str(0).zfill(difficulty)):
            self.nonce+=1
            self.hash = self.calculateHash()
    
    def __str__(self):
        return str(self.__dict__)
    
    
class BlockChain:
    
    def __init__(self):
        self.chain = [self.createGenesisBlock()]
        self.difficulty = 5

    def createGenesisBlock(self):
        return Block(0,"01/01/2018","genesis block")
    
    def getLatestBlock(self):
        return self.chain[len(self.chain)-1]
    #添加区块前需要 做一道计算题😶,坐完后才能把区块加入到链上
    def addBlock(self,newBlock):
        newBlock.previousHash = self.getLatestBlock().hash
        newBlock.minerBlock(self.difficulty)
        self.chain.append(newBlock)
        
        
    
    def __str__(self):
        return str(self.__dict__)    
    
    def chainIsValid(self):
        for index in range(1,len(self.chain)):
            currentBlock = self.chain[index]
            previousBlock = self.chain[index-1]
            if (currentBlock.hash != currentBlock.calculateHash()):
                return False
            if previousBlock.hash != currentBlock.previousHash:
                return False
        return True