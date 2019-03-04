import os.path
import json

from .export_error import ExportError
from .utils import Utils

class BooleanConverter(object):
    @staticmethod
    def convert(value, config_name):
        value = str(value).lower()
        if value == "true" or value == "1":
            return True
        elif value == "false" or value == "0":
            return False
        else:
            raise ExportError("Invalid Data Type for parameter: '" + config_name + "': Value must be a string, boolean or, 1 or 0")

class NumberConverter(object):
    @staticmethod
    def convert(value, config_name):
        value = str(value).lower()
        try:
            return int(value)
        except Exception:
            raise ExportError("Invalid Data Type for parameter: '" + config_name + "': Value must be a string, number")

class ChartConfigConverter(object):
    @staticmethod
    def convert(value):
        if (type(value) == type({})):
            value = json.dumps(value)
        valueToLower = str(value).lower()
        if valueToLower.endswith(".json"):
            if os.path.isfile(value) == False :
                print(os.path.isfile(value))
                raise ExportError("chartConfig [URL] not found. Please provide an appropriate path")
            return Utils.read_text_file(value)
        else:
            try:
                json.loads(value)
                return value
            except Exception:
                raise ExportError("Invalid Data Type for parameter 'chartConfig': Data should be a valid JSON string")

class EnumConverter(object):
    @staticmethod
    def convert(value, dataset, config_name):
        if value in dataset:
            return value
        else:
            raise ExportError("Invalid value for parameter '" + config_name + "': Accepted values are "  + ", ".join(dataset))

class FileConverter(object):
    @staticmethod
    def convert(value, config_name):
        if (type(value) == type("")):
            if os.path.isfile(value) == False :
                raise ExportError("URL/File Path in '" + config_name + "' not found. Please provide an appropriate path")
            return value
        else:
            raise ExportError("Invalid Data Type for parameter '" + config_name +"': Data should be a string")

class HtmlConverter(object):
    @staticmethod
    def convert(value, config_name):
        if (type(value) == type("")):
            if value.startswith("<") == False or value.lower().endswith("</html>") == False :
                raise ExportError(config_name + ": String should be a valid HTML template")
            return value
        else:
            raise ExportError("Invalid Data Type for parameter '" + config_name +"': Data should be a string")
