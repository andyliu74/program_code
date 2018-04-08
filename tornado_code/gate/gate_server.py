# -*- coding: utf-8 -*-

import sys
import random

sys.path.append('../')

from gameserver.tcp_server import TcpServer
from gameserver.tcp_client import TCPClient
from gameserver.client_entity import ClientEntity
from gameserver.server_entity import ServerEntity


GlobalGateServer = None
OtherPorts = []
CurPort = 0

def choice_port():
	global CurPort
	if OtherPorts and len(OtherPorts) > 2:
		port = random.choice([port for port in OtherPorts if port != CurPort])
		CurPort = port
	return CurPort

class GateServerEntity(ServerEntity):

	def add_count(self, count):
		if not GlobalGateServer:
			return
		addr = self.get_address()
		if addr is None:
			return
		ip, port = addr
		GlobalGateServer.gate2game_client.get_entity().call_server('add_count', ip, port, count)


class GateClientEntity(ClientEntity):

	def on_add_count(self, ip, port, result):
		if not GlobalGateServer:
			return
		entity = GlobalGateServer.get_entity((ip, port))
		entity and entity.call_client('on_add_count', result)

	def reconnect(self, port=0):
		if not GlobalGateServer:
			return
		if port == 0:
			port = choice_port()
		print 'port ', port
		GlobalGateServer.gate2game_client = TCPClient('127.0.0.1', port, GateClientEntity)
		GlobalGateServer.gate2game_client.connect()

	def on_connect(self):
		super(GateClientEntity, self).on_connect()
		self.call_server('check_leader')

	def on_connect_close(self):
		super(GateClientEntity, self).on_connect_close()
		self.reconnect()

class GateServer(TcpServer):

	def __init__(self, ip, port, game_ip, game_port):
		super(GateServer, self).__init__(ip, port, GateServerEntity)
		self.gate2game_client = TCPClient(game_ip, game_port, GateClientEntity)
		self.gate2game_client.connect()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: %s server_port, game_port ...' % sys.argv[0])
		sys.exit(-1)

	port = int(sys.argv[1])
	OtherPorts = [int(p) for p in sys.argv[2:]]
	GlobalGateServer = GateServer('0.0.0.0', port, '127.0.0.1', choice_port())
	try:
		GlobalGateServer.start()
	except:
		print('GateServer error!')
		sys.exit(-1)