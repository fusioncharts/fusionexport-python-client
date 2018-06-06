# -*- coding: utf-8 -*-


from .export_error import ExportError


class BooleanConverter(object):
    @staticmethod
    def convert(value):
        value = str(value).lower()
        if value == "true" or value == "1":
            return True
        elif value == "false" or value == "0":
            return False
        else:
            raise ExportError("Value must be boolean value or 1 or 0")


class NumberConverter(object):
    @staticmethod
    def convert(value):
        value = str(value).lower()
        try:
            return int(value)
        except Exception:
            raise ExportError("Value must be number value")
