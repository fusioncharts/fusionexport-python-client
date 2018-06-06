# -*- coding: utf-8 -*-


from .constants import Constants
from .utils import Utils
from .export_error import ExportError
from .converters import BooleanConverter, NumberConverter


class ExportConfig(object):
    """Contains export configurations according to the export metadata"""

    def __init__(self, config_dict=None):
        self.__export_metadata = Utils.get_export_metadata()
        self.__configs = {}

        if config_dict is not None:
            for config_name, config_value in config_dict.items():
                self.set(config_name, config_value)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def set(self, config_name, config_value):
        self.__configs[config_name] = self.__resolve_config_value(config_name, config_value)

    def __resolve_config_value(self, config_name, config_value):
        metadata = self.__export_metadata

        if config_name not in metadata["typings"]:
            raise ExportError("Export config '%s' is not supported" % config_name)

        if "converter" in metadata["typings"][config_name]:
            if metadata["typings"][config_name]["converter"] == "BooleanConverter":
                return BooleanConverter.convert(config_value)
            elif metadata["typings"][config_name]["converter"] == "NumberConverter":
                return NumberConverter.convert(config_value)
            else:
                raise ExportError("Unknown converter for the specified config name")
        elif metadata["typings"][config_name]["type"] == "string":
            return str(config_value)
        else:
            raise ExportError("Could not resolved the config name and config value")

    def get(self, config_name):
        return self.__configs[config_name]

    def __delitem__(self, index):
        del self.__configs[index]

    def remove(self, config_name):
        if config_name in self.__configs:
            self.__configs.pop(config_name)
            return True
        else:
            return False

    def __contains__(self, key):
        return key in self.__configs

    def has(self, config_name):
        return config_name in self.__configs

    def clear(self):
        self.__configs.clear()

    def __len__(self):
        return len(self.__configs)

    def count(self):
        return len(self.__configs)

    def config_names(self):
        return list(self.__configs)

    def config_values(self):
        return list(self.__configs.values())

    def clone(self):
        return ExportConfig(self.__configs)

    def get_formatted_configs(self):
        configs = self.__configs.copy()
        ec_template = Constants.EXPORT_CONFIG_NAME_TEMPLATE_FILE_PATH
        ec_resource = Constants.EXPORT_CONFIG_NAME_RESOURCE_FILE_PATH
        configs_as_json = ""

        if ec_template in configs:
            template_path = configs[ec_template]
            resource_path = configs[ec_resource] = configs.get(ec_resource, None)

            zipped_content = Utils.get_zipped_template_in_base64(template_path, resource_path)
            configs_as_json += "\"%s\": %s, " % (ec_template, Utils.json_stringify(zipped_content[0]))
            configs_as_json += "\"%s\": %s, " % (ec_resource, Utils.json_stringify(zipped_content[1]))

            del configs[ec_template]
            del configs[ec_resource]
        elif ec_resource in configs:
            del configs[ec_resource]

        for config_name, config_value in configs.items():
            formatted_config_value = self.__get_formatted_config_value(config_name, config_value)
            configs_as_json += "\"%s\": %s, " % (config_name, formatted_config_value)

        configs_as_json += "\"clientName\": %s, " % Utils.json_stringify(Constants.CLIENT_NAME)
        configs_as_json += "\"platform\": %s" % Utils.json_stringify(Utils.system_platform())
        return "{ " + configs_as_json + " }"

    def __get_formatted_config_value(self, config_name, config_value):
        metadata = self.__export_metadata

        if config_name in metadata["meta"] and "isBase64Required" in metadata["meta"][config_name]:
            return Utils.json_stringify(Utils.read_file_in_base64(config_value))
        else:
            return Utils.json_stringify(config_value)

    def __str__(self):
        return str(self.__configs)

    def __eq__(self, other):
        if isinstance(other, ExportConfig):
            return self.__configs == other.__configs
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
