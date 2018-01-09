# -*- coding: utf-8 -*-


import base64
import json
import os

from .constants import Constants


class Utils(object):
    """Contains utility methods"""

    __export_metadata = None

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

    @staticmethod
    def get_export_metadata_file_path():
        return {
            "meta": os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), Constants.EXPORT_METADATA_FILES["meta"])),
            "typings": os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), Constants.EXPORT_METADATA_FILES["typings"]))
        }

    @staticmethod
    def get_export_metadata():
        metadata_file_path = Utils.get_export_metadata_file_path()
        if Utils.__export_metadata is None:
            Utils.__export_metadata = {
                "meta": Utils.json_parse(Utils.read_text_file(metadata_file_path["meta"])),
                "typings": Utils.json_parse(Utils.read_text_file(metadata_file_path["typings"]))
            }
        return Utils.__export_metadata
