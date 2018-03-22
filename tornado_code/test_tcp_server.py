# -*- coding: utf-8 -*-

from gameserver.tcp_server import TcpServer
from gameserver.rpc_service import ServerService

def main():
    tcpserver = TcpServer('0.0.0.0', 8888, ServerService)
    tcpserver.start()


if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()
