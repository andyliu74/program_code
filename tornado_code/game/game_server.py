# -*- coding: utf-8 -*-

import sys
from pysyncobj import SyncObj
from pysyncobj.batteries import ReplCounter

sys.path.append('../')

from gameserver.tcp_server import TcpServer
from gameserver.server_entity import ServerEntity


GlobalGameServer = None
OtherPorts = []


class GameServerEntity(ServerEntity):

	def add_count(self, ip, port, count):
		if not GlobalGameServer:
			return

		if GlobalGameServer.syncObj._isLeader():
			GlobalGameServer.data.add(count, sync=True)
			self.call_client('on_add_count', ip, port, GlobalGameServer.data.get())
		else:
			self.call_client('reconnect')

	def check_leader(self):
		if not GlobalGameServer.syncObj._isLeader():
			print 'not leader'
			leader = GlobalGameServer.syncObj._getLeader()
			port = leader.split(':')[1] if leader else 0
			new_port = {
				8881:8885,
				8882:8886,
				8883:8887,
			}.get(port, 0)
			self.call_client('reconnect', new_port)
		else:
			print 'leader'


class GameServer(TcpServer):

	def __init__(self, ip, port, selfnode, othernodes):
		super(GameServer, self).__init__(ip, port, GameServerEntity)
		self.data = ReplCounter()
		self.syncObj = SyncObj(selfnode, othernodes, consumers=[self.data, ])


if __name__ == '__main__':
	if len(sys.argv) < 4:
		print('Usage: %s server_port, self_port partner1_port partner2_port ...' % sys.argv[0])
		sys.exit(-1)

	port = int(sys.argv[1])
	selfnode = '127.0.0.1:%d' % int(sys.argv[2])
	othernodes = ['127.0.0.1:%d' % int(p) for p in sys.argv[3:]]
	OtherPorts = [int(p) for p in sys.argv[3:]]

	GlobalGameServer = GameServer('0.0.0.0', port, selfnode, othernodes)
	try:
		GlobalGameServer.start()
	except:
		print('GameServer error!')
		sys.exit(-1)