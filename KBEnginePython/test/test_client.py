#-- coding: utf-8 -*-

import sys
sys.path.append('../')

from endpoint import EndPoint


def main():
	end_point = EndPoint()
	end_point.create_socket()
	end_point.connect(8888, '127.0.0.1')
	if end_point.good():
		end_point.send('Client')

		print end_point.recv(100)


if __name__ == "__main__":
	try:
		main()
	except:
		import traceback
		print traceback.format_exc()