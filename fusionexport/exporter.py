# -*- coding: utf-8 -*-


import re
import socket
from threading import Thread

from .constants import Constants
from .export_error import ExportError


class Exporter(object):
    """Handles individual chart export request generated by ExportManager"""

    def __init__(self, export_config=None, export_done_listener=None, export_state_changed_listener=None):
        self.__export_config = export_config
        self.__export_done_listener = export_done_listener
        self.__export_state_changed_listener = export_state_changed_listener
        self.__export_server_host = Constants.DEFAULT_HOST
        self.__export_server_port = Constants.DEFAULT_PORT
        self.__socket = None
        self.__socket_connection_thread = None

    def set_export_connection_config(self, host, port):
        self.__export_server_host = host
        self.__export_server_port = port

    def export_config(self):
        return self.__export_config

    def export_done_listener(self):
        return self.__export_done_listener

    def export_state_changed_listener(self):
        return self.__export_state_changed_listener

    def export_server_host(self):
        return self.__export_server_host

    def export_server_port(self):
        return self.__export_server_port

    def start(self):
        self.__socket_connection_thread = Thread(target=self.__handle_socket_connection)
        self.__socket_connection_thread.start()

    def cancel(self):
        if self.__socket is not None:
            try:
                self.__socket.close()
            except Exception as e:
                pass

    def __handle_socket_connection(self):
        try:
            sock = self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.__export_server_host, self.__export_server_port))
            sock.sendall(self.__get_formatted_export_configs().encode("utf-8"))

            data_received = ""
            while 1:
                read = sock.recv(4096)
                if (not isinstance(read, str)) and isinstance(read, bytes):
                    read = read.decode("utf-8")

                if not read: break
                data_received += read
                data_received = self.__process_data_received(data_received)
        except Exception as e:
            self.__on_export_done(None, ExportError(str(e)))
        finally:
            if self.__socket is not None:
                try:
                    self.__socket.close()
                except Exception as e:
                    pass

    def __process_data_received(self, data):
        parts = data.split(Constants.UNIQUE_BORDER, -1)
        for i in range(len(parts) - 1):
            part = parts[i]
            if part.startswith(Constants.EXPORT_EVENT):
                self.__process_export_state_changed_data(part)
            elif part.startswith(Constants.EXPORT_DATA):
                self.__process_export_done_data(part)
        return parts[len(parts) - 1]

    def __process_export_state_changed_data(self, data):
        state = data[len(Constants.EXPORT_EVENT):]
        export_error = self.__check_export_error(state)
        if export_error is None:
            self.__on_export_sate_changed(state)
        else:
            self.__on_export_done(None, ExportError(export_error))

    def __check_export_error(self, state):
        error_pattern = "^\\s*\\{\\s*\"error\"\\s*:\\s*\"(.+)\"\\s*}\\s*$"
        found = re.match(error_pattern, state, re.S)
        if found is not None:
            return found.group(1)
        else:
            return None

    def __process_export_done_data(self, data):
        export_result = data[len(Constants.EXPORT_DATA):]
        self.__on_export_done(export_result, None)

    def __on_export_sate_changed(self, state):
        if self.__export_state_changed_listener is not None:
            self.__export_state_changed_listener(state)

    def __on_export_done(self, result, error):
        if self.__export_done_listener is not None:
            self.__export_done_listener(result, error)

    def __get_formatted_export_configs(self):
        return "%s.%s<=:=>%s" % ("ExportManager", "export", self.__export_config.get_formatted_configs())
