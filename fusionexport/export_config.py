# -*- coding: utf-8 -*-


class ExportConfig(object):
    """Contains export configurations e.g. 'chartConfig', 'inputSVG' etc"""

    def __init__(self, config_dict=None):
        if config_dict is not None:
            self.__configs = config_dict.copy()
        else:
            self.__configs = {}

    def __setitem__(self, key, value):
        self.__configs[key] = value

    def __getitem__(self, key):
        return self.__configs[key]

    def set(self, config_name, config_value):
        self.__configs[config_name] = config_value

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
        configs_as_json = ""
        for config_name, config_value in self.__configs.items():
            formatted_config_value = self.__get_formatted_config_value(config_name, config_value)
            configs_as_json += "\"%s\": %s, " % (config_name, formatted_config_value)
        return "{ " + configs_as_json[:-2] + " }"

    def __get_formatted_config_value(self, config_name, config_value):
        if config_name == "chartConfig":
            return config_value
        elif config_name == "maxWaitForCaptureExit":
            return str(config_value)
        elif config_name == "asyncCapture":
            return str(config_value).lower()
        elif config_name == "exportAsZip":
            return str(config_value).lower()
        else:
            return "\"%s\"" % config_value

    def __str__(self):
        return self.get_formatted_configs()

    def __eq__(self, other):
        if isinstance(other, ExportConfig):
            return self.__configs == other.__configs
        return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
