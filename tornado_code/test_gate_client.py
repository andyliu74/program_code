# -*- coding: utf-8 -*-

import time
import tornado.ioloop
from gameserver.tcp_client import TCPClient
from gameserver.client_entity import ClientEntity


class TestGateClientEntity(ClientEntity):

    def __init__(self, conn, stub):
        super(TestGateClientEntity, self).__init__(conn, stub)
        self.count = 1

    def add_count(self):
        self.call_server('add_count', self.count)

    def on_connect(self):
        super(TestGateClientEntity, self).on_connect()
        self.add_count()

    def on_connect_close(self):
        super(TestGateClientEntity, self).on_connect_close()
        tornado.ioloop.IOLoop.instance().stop()

    def on_add_count(self, result):
        print 'on_add_count:', result
        self.count = result
        tornado.ioloop.IOLoop.instance().stop()

def main():
    c1 = TCPClient("127.0.0.1", 8880, TestGateClientEntity)
    c1.connect()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(5)
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)