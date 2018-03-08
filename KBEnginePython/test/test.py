# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

# from endpoint import EndPoint
# from event_dispatcher import EventDispatcher
# from listener_receiver import ListenerReceiver


def main():
	# end_point = EndPoint()
	# end_point.create_socket()
	# end_point.bind(8888, '0.0.0.0')
	# end_point.listen()

	# dispatcher = EventDispatcher()
	# receiver = ListenerReceiver(end_point, None)
	# dispatcher.registerReadFileDescriptor(end_point.fd, receiver)
	# dispatcher.processUtilBreak()

	import test_pb2

	# 为 all_person 填充数据
	device = test_pb2.CDevice()
	device.devId = 1001
	device.name = 'test_device'

	data = device.SerializeToString()

	print 'the protobuf data:', data

	# 对已经序列化的数据进行反序列化
	target = test_pb2.CDevice()
	target.ParseFromString(data)
	print target


if __name__ == "__main__":
	try:
		main()
	except:
		import traceback
		print traceback.format_exc()