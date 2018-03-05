# -*- coding: utf-8 -*-

from event_dispatcher import EventDispatcher
from network_interface import NetworkInterface
from loginapp import LoginApp


def main():
	dispatcher = EventDispatcher()
	ninterface = NetworkInterface(dispatcher, 8888, 8888, "", 8889, "")
	login_app = LoginApp(dispatcher, ninterface, 1, 1)
	login_app.run()