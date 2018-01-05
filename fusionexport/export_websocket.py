# -*- coding: utf-8 -*-


from ws4py.client.threadedclient import WebSocketClient


class ExportWebSocket(WebSocketClient):
    def __init__(self, host, port, conn_opened_callback, conn_closed_callback, message_received_callback):
        WebSocketClient.__init__(self, "ws://%s:%s/" % (host, port))
        self.__conn_opened_callback = conn_opened_callback
        self.__conn_closed_callback = conn_closed_callback
        self.__message_received_callback = message_received_callback

    def opened(self):
        self.__conn_opened_callback()

    def closed(self, code, reason=None):
        self.__conn_closed_callback(code, reason)

    def received_message(self, message):
        self.__message_received_callback(message)
