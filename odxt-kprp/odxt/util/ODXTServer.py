import socketserver
import pickle
import logging
import time

class serverReqHandlerV2(socketserver.BaseRequestHandler):
    def __init__(self, request, addr, server):
        super().__init__(request, addr, server)

    def handle(self):
        resp_tup = self.request.recv(4096*2**5)
        try:
            resp_tup1 = pickle.loads(resp_tup)
            print("Received " + str(len(resp_tup)) + " client data")
        except:
            self.request.settimeout(0.5)
            while True:
                try:
                    pp = self.request.recv(4096*2**5)
                    resp_tup += pp
                except Exception as e:
                    print(e)
                    print("Received " + str(len(resp_tup)) + " client data")
                    resp_tup1 = pickle.loads(resp_tup)
                    break

        resp_tup = resp_tup1
        if resp_tup == ("Prepare sending setup data",):
            self.request.sendall(pickle.dumps(("ok",)))
            print("begin receiving database setup data...")
            self.request.settimeout(0.5)
            resp_tup = b""
            while True:
                try:
                    packet = self.request.recv(4096*2**5)
                    resp_tup += packet
                except Exception as e:
                    print(e)
                    break
            print("Setup data size : " + str(len(resp_tup)))
            resp_tup = pickle.loads(resp_tup)
            
        if(resp_tup[0] == 0):  # for setup
            self.server.Setup(resp_tup[1])
            data = (1,)
            logging.debug("setup completed")
        elif(resp_tup[0] == 1):
            self.server.Update(resp_tup[1])
            data = (1,)
            logging.debug("update completed")
        elif(resp_tup[0] == 2):
            data = self.server.Search(resp_tup[1])
            logging.debug("search completed")
        # elif(resp_tup[0] == 'q'):
        #     logging.debug("Close server")
        #     self.server.shutdown()
        #     self.server.server_close()

        if (resp_tup[0] != 'q'):
            if resp_tup[0]>=0 and resp_tup[0]<=2:
                self.request.sendall(pickle.dumps(data))
                logging.debug('handled')
        else:
            print("Search completed")



class ODXTKPRPServerV2(socketserver.TCPServer):
    def __init__(self, addr, handler_class=serverReqHandlerV2) -> None:
        self.EDB = None
        self.p = -1
        super().__init__(addr, handler_class)

    def Setup(self, res):
        self.EDB, self.p = res

    def Update(self, avax_tup):
        TSet, XSet = self.EDB
        addr, val, alpha, xtag, upCnt = avax_tup
        TSet[addr] = (val, alpha)
        XSet[xtag[0]] = xtag[1]
        self.EDB = (TSet, XSet)

    def Search(self, tknlists):
        ts = time.time()
        TSet, XSet = self.EDB
        stokenlist = tknlists[0]
        xtokenlists = tknlists[1]
        xtoken_conj_cond = tknlists[2]
        n = len(stokenlist)
        sEOpList = []
        for j in range(n):
            sval, alpha = TSet[stokenlist[j]]
            xtag_cond = None
            for xt0 in range(len(xtokenlists[j])):
                xtoken_ij = xtokenlists[j][xt0]
                xtag_ij = pow(xtoken_ij, alpha, self.p)

                if xtag_ij in XSet.keys():
                    if xt0==0:
                        xtag_cond = XSet[xtag_ij]
                    else:
                        xtag_cond ^= XSet[xtag_ij]
                else:
                    raise ValueError("Error in xtag")
            if xtag_cond == xtoken_conj_cond:
                sEOpList.append((j, sval))
        print("Server search time for DB(w_1)==" + str(n) + ", number of keywords: " + str(len(xtokenlists[0])+1) + ": " + str(time.time()-ts))
        return (sEOpList,)
