# -*- coding: utf-8 -*-

from gameserver.tcp_server import TcpServer
from gameserver.server_entity import ServerEntity


class TestServerEntity(ServerEntity):

	def test_rpc(self, param1, param2):
		print param1, param2
		self.call_client('on_test_rpc', param1)


def main():
    tcpserver = TcpServer('0.0.0.0', 8888, TestServerEntity)
    tcpserver.start()


if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
        quit()
