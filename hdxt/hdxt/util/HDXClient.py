import pickle
import socket
import random
import sys
import time
from .HDXTutil import *

MAXINT = sys.maxsize

class HDXTClientV2:
    def __init__(self, addr):
        self.sk: tuple = ()
        self.st: dict = None
        self.p: int = -1
        self.g: int = -1
        self.addr = addr
        self.upCnt = 0

    def Setup(self, λ, keywords_file, ids_file):

        self.p = 69445180235231407255137142482031499329548634082242122837872648805446522657159

        self.g = 65537

        Kt = gen_key_F(λ)
        K1 = gen_key_F(λ+1)
        K2 = gen_key_F(λ+2)
        K3 = gen_key_F(λ+3)
        UpdateCnt, TSet, XSet = dict(), dict(), dict()

        self.sk, self.st = (Kt,K1,K2,K3), UpdateCnt

        with open(keywords_file,"r") as f:
            keywords = f.readlines()
        keywords = [kk.strip("\n") for kk in keywords]
        print("# of keywords: " + str(len(keywords)))
        
        with open(ids_file,"r") as f:
            ids = f.readlines()
        ids = [ii.strip("\n") for ii in ids]
        print("# of files: " + str(len(ids)))

        # Initialization of XSet
        for w in keywords:
            for i in ids:
                kk = prf_Fp(K1,(w+str(i)).encode(),self.p,self.g)
                XSet[kk] = bytes_XOR(prf_Fp(K2,(str(kk)+"0").encode(),self.p,self.g),prf_Fp(K3,(str(kk)+"0").encode(),self.p,self.g))
        EDB = (TSet, XSet)
        print("EDB generated")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        initial_message = pickle.dumps(("Prepare sending setup data",))
        conn.send(initial_message)
        data = pickle.loads(conn.recv(4096))
        if data == ("ok",):
            po = pickle.dumps((0, EDB))
            print("pick dumped EDB")
            conn.send(po)
            print("setup EDB sent to server")
            data = pickle.loads(conn.recv(4096))
            if(data == (1,)):
                print("Setup completed")
        else:
            print("Connection broken")
        conn.close()

    def Update(self, op: str, id_w_tuple):
        self.upCnt += 1
        i, w = id_w_tuple
        Kt, K1, K2, K3 = self.sk
        if(not w in self.st):
            self.st[w] = 0
        self.st[w] += 1
        w_wc = str(w)+str(self.st[w])
        addr = prf_F(Kt, (w_wc+str(0)).encode())

        b1 = (str(op)+str(i)).encode()
        b2 = prf_F(Kt, (w_wc+str(1)).encode())
        val = bytes_XOR(b1, b2)

        xset_1 = prf_Fp(K1,(w+str(i)).encode(),self.p,self.g)
        if op == "add":
            xset_2 = bytes_XOR(prf_Fp(K2,(str(xset_1)+"1").encode(),self.p,self.g),prf_Fp(K3,(str(xset_1)).encode(),self.p,self.g))
        else:
            xset_2 = bytes_XOR(prf_Fp(K2,(str(xset_1)+"0").encode(),self.p,self.g),prf_Fp(K3,(str(xset_1)).encode(),self.p,self.g))
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps((1, (addr, val, [xset_1,xset_2], self.upCnt))))
        data = pickle.loads(conn.recv(1024))
        # if(data == (1,)):
        #     print("Update completed")
        conn.close()

    def Search(self, q):
        ts = time.time()
        n = len(q)
        Kt, K1, K2, K3 = self.sk
        w1_uc = MAXINT
        w1 = ""
        for x in q:
            if x in self.st and self.st[x] < w1_uc:
                w1 = x
                w1_uc = self.st[x]
        stokenlist = []

        if(w1 in self.st):
            for j in range(w1_uc):
                saddr_j = prf_F(
                    Kt, (str(w1)+str(j+1)+str(0)).encode())
                stokenlist.append(saddr_j)
        t1 = time.time()-ts
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        payload = pickle.dumps((2, stokenlist))
        print("client sends stoken (length): " + str(len(payload)))
        conn.send(payload)

        #
        # SERVER WORK
        #

        resp_tup = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            resp_tup += packet
        resp_tup = pickle.loads(resp_tup)
        sEOpList = resp_tup
        IdList = []

        ts = time.time()
        for l in sEOpList:
            j, sval = l
            X0 = prf_F(Kt, (str(w1)+str(j+1)+str(1)).encode())
            op_id = bytes_XOR(sval, X0)
            op_id = op_id.decode().rstrip('\x00')
            if(op_id[:3] == 'add'):
                IdList.append(int(op_id[3:]))
            elif(op_id[:3] == 'del' and int(op_id[3:]) in IdList):
                IdList.remove(int(op_id[3:]))
        IdList = list(set(IdList))
        random.shuffle(IdList)
        conn.close()

        # Round 2 
        xtokenlist = []
        for idd in IdList:
            L = []
            xors = None
            for w in q:
                if w != w1:
                    kk = prf_Fp(K1,(w+str(idd)).encode(),self.p,self.g)
                    L.append(kk)
                    if xors is None:
                        xors = bytes_XOR(prf_Fp(K2,(str(kk)+"1").encode(),self.p,self.g),prf_Fp(K3,(str(kk)).encode(),self.p,self.g))
                    else:
                        xors = bytes_XOR(xors,bytes_XOR(prf_Fp(K2,(str(kk)+"1").encode(),self.p,self.g),prf_Fp(K3,(str(kk)).encode(),self.p,self.g)))
            random.seed(10)
            r = random.getrandbits(256).to_bytes(32, 'little')
            d = prf_F(r,xors)
            xtokenlist.append([L,r,d])
        t2 = time.time() - ts
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        payload = pickle.dumps((3, xtokenlist))
        print("client sends xtoken (length): " + str(len(payload)))
        conn.send(payload)

        #
        # SERVER WORK
        #

        resp_tup = b""
        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            resp_tup += packet
        resp_tup = pickle.loads(resp_tup)     

        ts = time.time()
        IdList = [IdList[jj] for jj in resp_tup]
        t3 = time.time() - ts
        print("Client search time : " + str(t1) + "   " + str(t1+t2+t3))
        conn.close()

        return IdList

    def close_server(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps(("q",)))
        conn.close()
