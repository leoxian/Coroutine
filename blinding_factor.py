# from gevent import monkey;monkey.patch_all()
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

#from random import SystemRandom
import random
import string
# import gevent
import datetime

##using to produce 5 private key and public key
class Smart_Contract(object):
    def __init__(self):
        self.priv = RSA.generate(3072)
        self.pub = self.priv.publickey()
    
    def produce_priv(self):
        return self.priv

    def produce_pub(self):
        return self.pub


class Blinded_Signature(object):

    def __init__(self,pub):
        # self.priv = RSA.generate(number)
        self.pub = pub
        self.r = random.SystemRandom().randrange(self.pub.n >> 10, self.pub.n)
        
    ##msg is a address
    def Blind(self,msg):
        # # # Signing authority (SA) key
        # priv = RSA.generate(3072)
        # pub = priv.publickey()
        ## Protocol: Blind signature ##
        # must be guaranteed to be chosen uniformly at random
        # large message (larger than the modulus)
        # hash message so that messages of arbitrary length can be signed
        hash = SHA256.new()
        msg = str.encode(msg)
        hash.update(msg)
        msgDigest = hash.digest()
        # user computes
        msg_blinded = self.pub.blind(msgDigest,self.r)
        #print('-----msg_blinded-------')
        #print(msg_blinded)
        return msg_blinded

    def eliminate(self,msg_blinded_signature):
        # user computes
        msg_signature = self.pub.unblind(msg_blinded_signature[0], self.r)
        return msg_signature
        
    def verifies(self,msg,msg_signature):
        # Someone verifies
        # print('-------msg----------')
        # print(msg)
        msg = str.encode(msg)
        hash = SHA256.new()
        hash.update(msg)
        msgDigest = hash.digest()
        # print('--------msg_signature---------')
        # print(msgDigest)
        if self.pub.verify(msgDigest, (msg_signature,)) == True:
            #print("Message is authentic: " + str(self.pub.verify(msgDigest, (msg_signature,))))
            return True
        else:
            return False

class Sa_Computer(object):

    def __init__(self,priv):
        # print('初始化')
        # print(priv)
        self.priv = priv


    def sa_computes(self,msg_blinded):
        # SA computes
        msg_blinded_signature = self.priv.sign(msg_blinded, 0)
        return msg_blinded_signature


def Start():
    now = datetime.datetime.now()
    members = set()
    ##用于生成地址列表，与环:
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    while len(members)<200:
        if ran_str not in members:
            #print(ran_str)
            members.add(ran_str)
        else:
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    members = list(members)
    count = {}
    smart_contract = Smart_Contract()
    pub = smart_contract.produce_pub()
    priv = smart_contract.produce_priv()

    Blind_List =[]
    Sa_List =[]

    blinded_signature=Blinded_Signature(pub)

    for i in members[0:5]:
        Blind_List.append(blinded_signature.Blind(i))

    sa_computer = Sa_Computer(priv)
    for s in range (len(members)-1):
        msg_blinded=Blind_List[random.randint(0,len(Blind_List)-1)]
        Sa_List.append(sa_computer.sa_computes(msg_blinded))


    for s in Sa_List:
        # print('这里是s')
        # print(s)
        key = blinded_signature.eliminate(s)
        # print('这里是key')
        # print(key)
        if key not in count:
            count[key] = 1
        else:
            count[key] +=1
        
    key = max(count,key=count.get)
    # print('这个是最大的key')
    # print(key)
    for i in members[0:5]:
        #rint(i)
        if blinded_signature.verifies(i,key) == True:
            #gevent.sleep(1)
            print('胜利节点为:{}'.format(i))
            return [i,0,(datetime.datetime.now()-now).seconds]
    print((datetime.datetime.now()-now).seconds)

#start(200)

# def ring_consensus(n):

#     members = set()
#     ##用于生成地址列表，与环:
#     ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#     while len(members)<n:
#         if ran_str not in members:
#             #print(ran_str)
#             members.add(ran_str)
#         else:
#             ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
#     members = list(members)
#     print('-----members数-------')
#     print(len(members))
#     now_time = datetime.datetime.now()
#     temp =[]
#     n = 0
#     #temp.append(gevent.spawn(pow_goroutine,Id,difficult,sleep_time))
#     while n<len(members):
#         if (n+200)<len(members):
#             temp.append(gevent.spawn(start,members[n:n+200]))
#             n = n+200
#         else:
#             temp.append(gevent.spawn(start,members[n:n+200]))
#             break
            
#     gevent.joinall(temp)
#     print('盲签名共识时间')
#     print((datetime.datetime.now()-now_time).seconds)
#     temp_x=[]
#     if len(temp)>2:
#         for _,g in enumerate(temp):
#             print('g的值为')
#             print(g.value)
#             temp_x.append([g.value,0])

#         print('进行PBFT算法所需时间')
#         print((datetime.datetime.now()-now_time).seconds)
#     else:
#         print((datetime.datetime.now()-now_time).seconds)

# ring_consensus(200)