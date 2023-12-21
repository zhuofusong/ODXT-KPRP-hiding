import sys
from util.ODXTServer import ODXTKPRPServerV2, serverReqHandlerV2

HOST = 'localhost'
PORT = 50057

if __name__ == "__main__":
    # HOST = sys.argv[1]
    # PORT = int(sys.argv[2])
    
    server = ODXTKPRPServerV2((HOST, PORT), serverReqHandlerV2)
    server.serve_forever()