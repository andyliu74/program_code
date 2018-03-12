# -*- coding: utf-8 -*-

from serverapp import ServerApp


class LoginApp(ServerApp):

	def __init__(self, dispatcher, ninterface, component_type, component_id):
		super(LoginApp, self).__init__(dispatcher, ninterface, component_type, component_id)