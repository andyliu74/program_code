# -*- coding: utf-8 -*-

import tornado.ioloop
from gameserver.tcp_client import TCPClient
from gameserver.client_entity import ClientEntity


class TestClientEntity(ClientEntity):

    def test_rpc(self, param1, param2):
        self.call_server('test_rpc', param1, param2)

    def on_connect(self):
        super(TestClientEntity, self).on_connect()
        self.test_rpc('hello world', 123)

    def on_connect_close(self):
        super(TestClientEntity, self).on_connect_close()
        tornado.ioloop.IOLoop.instance().stop()

    def on_test_rpc(self, result):
        print result
        self.disconnect()


def main():
    c1 = TCPClient("127.0.0.1", 8888, TestClientEntity)
    c1.connect()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main()
    except Exception, ex:
        print "Ocurred Exception: %s" % str(ex)
