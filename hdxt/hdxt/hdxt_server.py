import sys
from util.HDXTServer import HDXTServerV2, serverReqHandlerV2

HOST = 'localhost'
PORT = 50059

if __name__ == "__main__":
    # HOST = sys.argv[1]
    # PORT = int(sys.argv[2])
    
    server = HDXTServerV2((HOST, PORT), serverReqHandlerV2)
    server.serve_forever()