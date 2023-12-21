import pickle
import socket
import random
import sys
import time
from .ODXTutil import *

MAXINT = sys.maxsize

class ODXTKPRPClientV2:
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
        Kx = gen_key_F(λ+1)
        Ky = gen_key_F(λ+2)
        Kz = gen_key_F(λ+3)
        Kid = gen_key_F(λ+4)
        Kstar = gen_key_F(λ+5)
        UpdateCnt, TSet, XSet = dict(), dict(), dict()

        self.sk, self.st = (Kt, Kx, Ky, Kz, Kid, Kstar), UpdateCnt

        with open(keywords_file,"r") as f:
            keywords = f.readlines()
        keywords = [kk.strip("\n") for kk in keywords]
        print("# of keywords: " + str(len(keywords)))
        
        with open(ids_file,"r") as f:
            ids = f.readlines()
        ids = [ii.strip("\n") for ii in ids]
        print("# of files: " + str(len(ids)))

        # Generate \hat{w_i}
        self.w_hat = dict()
        for w in keywords:
            self.w_hat[w] = prf_Fp(Kx, str(w).encode(), self.p, self.g)
            self.w_hat[w] = int.from_bytes(self.w_hat[w], 'little')
        print("w_hat generated")

        # Generate \hat{id_j}
        id_hat = dict()
        for i in ids:
            id_hat[i] = prf_Fp(Kid, str(i).encode(), self.p, self.g)
            id_hat[i] = int.from_bytes(id_hat[i], 'little')
        print("id_hat generated")

        # Generate XSet
        self.wop_hat = dict()
        for w in keywords:
            self.wop_hat[w + "del"] = prf_Fp(Kstar, str(w+"del").encode(), self.p, self.g)
            self.wop_hat[w + "del"] = int.from_bytes(self.wop_hat[w + "del"], 'little')
            for i in ids:
                XSet[pow(self.g, self.w_hat[w]*id_hat[i], self.p)] = pow(self.g, self.wop_hat[w + "del"],self.p)
        EDB = (TSet, XSet)
        print("EDB generated")
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        initial_message = pickle.dumps(("Prepare sending setup data",))
        conn.send(initial_message)
        data = pickle.loads(conn.recv(4096))
        if data == ("ok",):
            po = pickle.dumps((0, (EDB, self.p)))
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
        Kt, Kx, Ky, Kz, Kid, Kstar = self.sk
        if(not w in self.st):
            self.st[w] = 0
        self.st[w] += 1
        w_wc = str(w)+str(self.st[w])
        addr = prf_F(Kt, (w_wc+str(0)).encode())

        b1 = (str(op)+str(i)).encode()
        b2 = prf_F(Kt, (w_wc+str(1)).encode())
        val = bytes_XOR(b1, b2)

        mask = prf_Fp(Kz, (w_wc).encode(), self.p,self.g)
        mask = int.from_bytes(mask, 'little')
        mask_inv = mul_inv(mask,self.p-1)
        idop_hat = prf_F(Ky, (str(i) + op).encode())
        idop_hat = int.from_bytes(idop_hat, 'little')

        id_hat = prf_Fp(Kid, str(i).encode(), self.p, self.g)
        id_hat = int.from_bytes(id_hat, 'little')

        alpha = id_hat*mask_inv
        
        xset_1 = pow(self.g, self.w_hat[w]*id_hat,self.p)
        if w + op not in self.wop_hat.keys():
            self.wop_hat[w + op] = prf_Fp(Kstar, str(w+op).encode(), self.p, self.g)
            self.wop_hat[w + op] = int.from_bytes(self.wop_hat[w + op], 'little')
        xset_2 = pow(self.g, self.wop_hat[w+op],self.p)

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps((1, (addr, val, alpha, [xset_1,xset_2], self.upCnt))))
        data = pickle.loads(conn.recv(1024))
        # if(data == (1,)):
        #     print("Update completed")
        conn.close()

    def Search(self, q):
        ts = time.time()
        n = len(q)
        Kt, Kx, Ky, Kz, Kid, Kstar = self.sk
        w1_uc = MAXINT
        w1 = ""
        for x in q:
            if x in self.st and self.st[x] < w1_uc:
                w1 = x
                w1_uc = self.st[x]
        stokenlist = []
        xtokenlists = []
        xtoken_conj_cond = None

        if(w1 in self.st):
            for j in range(w1_uc):
                saddr_j = prf_F(
                    Kt, (str(w1)+str(j+1)+str(0)).encode())
                stokenlist.append(saddr_j)
                mask = prf_Fp(Kz, (w1 + str(j+1)).encode(), self.p,self.g)
                mask = int.from_bytes(mask, 'little')
                xtl = []
                for cross in range(n):
                    if q[cross] != w1:
                        xij = pow(self.g, self.w_hat[q[cross]]*mask,self.p)
                        xtl.append(xij)
                random.shuffle(xtl)
                xtokenlists.append(xtl)

            for cross in range(n):
                if q[cross] != w1:
                    temp = q[cross] + "add"
                    if temp not in self.wop_hat:
                        self.wop_hat[temp] = prf_Fp(Kstar, str(temp).encode(), self.p, self.g)
                        self.wop_hat[temp] = int.from_bytes(self.wop_hat[temp], 'little')
                    if xtoken_conj_cond is None:
                        xtoken_conj_cond = pow(self.g, self.wop_hat[temp],self.p)
                    else:
                        xtoken_conj_cond ^= pow(self.g, self.wop_hat[temp],self.p)     
                
        res = (stokenlist, xtokenlists, xtoken_conj_cond)
        t1 = time.time()-ts
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        payload = pickle.dumps((2, res))
        print("client sends " + str(len(payload)))
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
        sEOpList = resp_tup[0]
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
        t2 = time.time() - ts
        print("Client search time : " + str(t1) + "   " + str(t1+t2))
        # print(IdList)
        conn.close()
        return IdList

    def close_server(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps(("q",)))
        conn.close()
