import os.path
import json
from .export_error import ExportError
from .utils import Utils
from jsmin import jsmin
from html_minifier.minify import Minifier
class BooleanConverter(object):
    @staticmethod
    def convert(value, config_name):
        value_lower = str(value).lower()
        if value_lower == "true" or value == "1":
            return True
        elif value_lower == "false" or value == "0":
            return False
        else:
            raise ExportError("'%s' of type '%s' is unsupported. Supported data types are string, boolean, 1 or 0" % (config_name, type(value).__name__))

class NumberConverter(object):
    @staticmethod
    def convert(value, config_name):
        try:
            return int(str(value))
        except Exception:
            raise ExportError("'%s' of type '%s' is unsupported. Supported data types are string, number" % (config_name, type(value).__name__))

class ChartConfigConverter(object):
    @staticmethod
    def convert(value, minify_resources=False):
        if (type(value) == type({}) or type(value) == type([])):
            if minify_resources:
                value = json.dumps(value, indent=None)
            else:
                value = json.dumps(value)
        valueToLower = str(value).lower()
        if valueToLower.endswith(".json"):
            if os.path.isfile(value) == False :
                print(os.path.isfile(value))
                raise ExportError("chartConfig [URL] not found. Please provide an appropriate path")
            json_value = Utils.read_text_file(value)
            if minify_resources:
                return jsmin(json_value)
            else:
                return json_value
        else:
            try:
                json.loads(value)
                if minify_resources:
                    return jsmin(value)
                else:
                    return value
            except Exception:
                raise ExportError(("chartConfig of type '%s' is unsupported. Supported data types are string, object,array & file path." % type(value).__name__))

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
                raise ExportError("URL/File path in '" + config_name + "' not found. Please provide an appropriate path")
            return value
        else:
            raise ExportError("'%s' of type '%s' is unsupported. Supported data types is string" % (config_name, type(value).__name__))

class HtmlConverter(object):
    @staticmethod
    def convert(value, config_name, minify_resources=False):
        if (type(value) == type("")):
            if value.startswith("<") == False or value.lower().endswith("</html>") == False :
                raise ExportError(config_name + ": String should be a valid HTML template")
            if minify_resources:
                html_content = Minifier(value)
                return html_content.minify()
            else:
                return value
        else:
            raise ExportError("'%s' of type '%s' is unsupported. Supported data types is string" % (config_name, type(value).__name__))

class ObjectConverter(object):
    @staticmethod
    def convert(value, config_name, minify_resources=False):
        if(type(value) == type({})):
            if minify_resources:
                value = json.dumps(value, indent=None)
            else:
                value = json.dumps(value)
            return value