# -*- coding: utf-8 -*-

from event_dispatcher import EventDispatcher
from network_interface import NetworkInterface
from loginapp import LoginApp


def main():
	dispatcher = EventDispatcher()
	ninterface = NetworkInterface()
	login_app = LoginApp(dispatcher, ninterface, 1, 1)
	login_app.run()