# -*- coding: utf-8 -*-


import base64
import json


class Utils(object):
    """Contains utility methods"""

    @staticmethod
    def read_file_in_base64(file_path):
        base64_content = base64.b64encode(Utils.read_binary_file(file_path))
        if (not isinstance(base64_content, str)) and isinstance(base64_content, bytes):
            base64_content = base64_content.decode("utf-8")
        return base64_content

    @staticmethod
    def read_binary_file(file_path):
        with open(file_path, "rb") as f:
            return f.read()

    @staticmethod
    def read_text_file(file_path):
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def json_stringify(value):
        try:
            return json.dumps(value)
        except Exception:
            return None

    @staticmethod
    def json_parse(value):
        try:
            return json.loads(value)
        except Exception:
            return None
