# -*- coding: utf-8 -*-


from .constants import Constants
from .exporter import Exporter


class ExportManager(object):
    """Exports charts using specified host and port of Export Server"""

    def __init__(self, host=None, port=None):
        if host is not None:
            self.__host = host
        else:
            self.__host = Constants.DEFAULT_HOST

        if port is not None:
            self.__port = port
        else:
            self.__port = Constants.DEFAULT_PORT

    def port(self, port=None):
        if port is not None:
            self.__port = port
        else:
            return self.__port

    def host(self, host=None):
        if host is not None:
            self.__host = host
        else:
            return self.__host

    def export(self, export_config=None, export_done_listener=None, export_state_changed_listener=None):
        exporter = Exporter(export_config, export_done_listener, export_state_changed_listener)
        exporter.set_export_connection_config(self.__host, self.__port)
        exporter.start()
        return exporter
