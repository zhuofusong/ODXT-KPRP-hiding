import sys
from util.ODXClient import ODXTClientV2
import time

MAXINT = sys.maxsize
HOST = 'localhost'
PORT = 50058


if __name__ == "__main__":

    D = 20000 # Number of documents

    # HOST = sys.argv[1]
    # PORT = int(sys.argv[2])
    client_obj = ODXTClientV2((HOST, PORT))
    t = time.time()
    client_obj.Setup(100)
    print("Setup time: " + str(time.time()-t))

    with open("test/updates.txt","r") as f:
        key_id_pairs = f.readlines()
    t = time.time()
    for e in key_id_pairs:
        e = e.strip("\n")
        op, idd, keyword = e.split(" ")
        client_obj.Update(op, (int(idd), keyword))
    print("Update time: " + str(time.time()-t))

    with open("test/keywords.txt","r") as f:
        keys = f.readlines()
    keys = [kk.strip("\n") for kk in keys]

    #######
    # Make sure each of the keywords in search below appears at least ONCE in the test/updates.txt file. If a keyword has only been initialized but not updated, the search function will return error 
    #######

    # Single keyword search
    # print("############Single keyword search")
    # for k in keys:
    #     print("Search for " + k)
    #     t = time.time()
    #     client_obj.Search([k])
    #     print("End-to-End search time: " + str(time.time()-t))
    
    # Conjunctive 2 keyword search, changing DB(w_1)
    print("############2 keyword search, changing DB(w_1)")
    for k in range(3,38,2):
        print("Search for " + str(keys[(k-2):k]))
        t = time.time()
        res = client_obj.Search(keys[(k-2):k])
        print("End-to-End search time: " + str(time.time()-t))
        # check correctness
        i = int(keys[k-2].lstrip("@keyword").strip("@"))
        res1 = [jj for jj in range(D//2-i//2,D//2+i//2)]
        try:
            assert set(res)==set(res1)
        except:
            print("Search result wrong!!! for " + str(keys[(k-2):k]))
            print(set(res)^set(res1))

    # Conjunctive 2 keyword search, fixed DB(w_1)
    print("############2 keyword search, fixed DB(w_1)")
    for k in range(3,38,2):
        print("Search for " + str([keys[1],keys[k-1]]))
        t = time.time()
        res = client_obj.Search([keys[1],keys[k-1]])
        print("End-to-End search time: " + str(time.time()-t))
        # check correctness
        i = int(keys[1].lstrip("@keyword").strip("@"))
        res1 = [jj for jj in range(D//2-i//2,D//2+i//2)]
        try:
            assert set(res)==set(res1)
        except:
            print("Search result wrong!!! for " + str([keys[1],keys[k-1]]))
            print(set(res)^set(res1))

    # Conjunctive 6 keyword search, changing DB(w_1)
    print("############6 keyword search, changing DB(w_1)")
    for k in range(7,36,7):
        print("Search for " + str(keys[(k-6):k]))
        t = time.time()
        res = client_obj.Search(keys[(k-6):k])
        print("End-to-End search time: " + str(time.time()-t))
        # check correctness
        i = int(keys[k-6].lstrip("@keyword").strip("@"))
        res1 = [jj for jj in range(D//2-i//2,D//2+i//2)]
        try:
            assert set(res)==set(res1)
        except:
            print("Search result wrong!!! for " + str(keys[(k-6):k]))
            print(set(res)^set(res1))

    # Conjunctive 6 keyword search, fixed DB(w_1)
    print("############6 keyword search, fixed DB(w_1)")
    for k in range(7,36,7):
        print("Search for " + str([keys[1]] + keys[(k-5):k]))
        t = time.time()
        res = client_obj.Search([keys[1]] + keys[(k-5):k])
        print("End-to-End search time: " + str(time.time()-t))
        # check correctness
        i = int(keys[1].lstrip("@keyword").strip("@"))
        res1 = [jj for jj in range(D//2-i//2,D//2+i//2)]
        try:
            assert set(res)==set(res1)
        except:
            print("Search result wrong!!! for " + str([keys[1]] + keys[(k-5):k]))
            print(set(res)^set(res1))

    client_obj.close_server()
