import pickle
import socket
import random
import sys
import time
from .ODXTutil import *

MAXINT = sys.maxsize

class ODXTClientV2:
    def __init__(self, addr):
        self.sk: tuple = ()
        self.st: dict = None
        self.p: int = -1
        self.g: int = -1
        self.addr = addr
        self.upCnt = 0

    def opConj(self, op):
        if(op == 'add'):
            return 'del'
        if(op == 'del'):
            return 'add'

    def Setup(self, λ):
        self.p = 69445180235231407255137142482031499329548634082242122837872648805446522657159

        self.g = 65537
        self.w_hat = dict()

        Kt = gen_key_F(λ)
        Kx = gen_key_F(λ+1)
        Ky = gen_key_F(λ+2)
        Kz = gen_key_F(λ+3)
        UpdateCnt, Tset, XSet = dict(), dict(), dict()
        self.sk, self.st = (Kt, Kx, Ky, Kz), UpdateCnt
        EDB = (Tset, XSet)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps((0, (EDB, self.p))))
        data = pickle.loads(conn.recv(4096))
        if(data == (1,)):
            print("Setup completed")
        conn.close()

    def Update(self, op: str, id_w_tuple):
        self.upCnt += 1
        id, w = id_w_tuple
        Kt, Kx, Ky, Kz = self.sk
        if(not w in self.st):
            self.st[w] = 0
        self.st[w] += 1
        w_wc = str(w)+str(self.st[w])
        addr = prf_F(Kt, (w_wc+str(0)).encode())
        b1 = (str(op)+str(id)).encode()
        b2 = prf_F(Kt, (w_wc+str(1)).encode())
        b3 = (str(self.opConj(op))+str(id)).encode()
        val = bytes_XOR(b1, b2)
        A0 = prf_Fp(Ky, b1, self.p, self.g)
        A = int.from_bytes(A0, 'little')
        A_inv = mul_inv(A, self.p-1)
        A1 = prf_Fp(Ky, b3, self.p, self.g)
        A_p = int.from_bytes(A1, 'little')
        B0 = prf_Fp(Kz, (w_wc).encode(), self.p, self.g)
        B = int.from_bytes(B0, 'little')
        B_inv = mul_inv(B, self.p-1)

        if w not in self.w_hat.keys():
            self.w_hat[w] = prf_Fp(Kx, str(w).encode(), self.p, self.g)
            self.w_hat[w] = int.from_bytes(self.w_hat[w], 'little')

        α = (A*B_inv)
        beta = (A_inv*A_p)
        xtag = pow(self.g, self.w_hat[w]*A, self.p)

        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps((1, (addr, val, (α, beta), xtag, self.upCnt))))
        data = pickle.loads(conn.recv(1024))
        # if(data == (1,)):
        #     print("Update completed")
        conn.close()

    def Search(self, q):
        ts = time.time()
        n = len(q)
        Kt, Kx, Ky, Kz = self.sk
        w1_uc = MAXINT
        w1 = ""
        for x in q:
            if x in self.st and self.st[x] < w1_uc:
                w1 = x
                w1_uc = self.st[x]
        stokenlist = []
        xtokenlists = []
        if(w1 in self.st):
            for j in range(w1_uc):
                saddr_j = prf_F(
                    Kt, (str(w1)+str(j+1)+str(0)).encode())
                stokenlist.append(saddr_j)
                xtl = []
                B0 = prf_Fp(
                    Kz, (str(w1)+str(j+1)).encode(), self.p, self.g)
                B = int.from_bytes(B0, 'little')
                for i in range(n):
                    if(q[i] != w1):
                        xtoken = pow(self.g, self.w_hat[q[i]]*B, self.p)
                        xtl.append(xtoken)
                random.shuffle(xtl)
                xtokenlists.append(xtl)
        res = (stokenlist, xtokenlists)
        t1 = time.time() - ts

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
            j, sval, cnt_i, cnt_j = l
            X0 = prf_F(Kt, (str(w1)+str(j+1)+str(1)).encode())
            op_id = bytes_XOR(sval, X0)
            op_id = op_id.decode().rstrip('\x00')
            if(op_id[:3] == 'add' and cnt_i == n and cnt_j == 0):
                IdList.append(int(op_id[3:]))
            elif(op_id[:3] == 'del' and cnt_i > 0 and int(op_id[3:]) in IdList):
                IdList.remove(int(op_id[3:]))
        t2 = time.time() - ts
        print("Client search time : " + str(t1) + "   " + str(t1+t2))
        # print(list(set(IdList)))
        conn.close()
        return list(set(IdList))

    def close_server(self):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(self.addr)
        conn.send(pickle.dumps(("q",)))
        conn.close()
