# -*- coding: utf-8 -*-


import os
import base64

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

    @staticmethod
    def save_exported_files(dir_path, exported_output):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for exported_data in exported_output["data"]:
            with open(os.path.join(dir_path, exported_data["realName"]), "wb") as f:
                f.write(base64.b64decode(exported_data["fileContent"]))

    @staticmethod
    def get_exported_file_names(exported_output):
        return [x["realName"] for x in exported_output["data"]]