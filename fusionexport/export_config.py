import os
import tempfile
import json

from .constants import Constants
from .utils import Utils
from .export_error import ExportError
from .typings import typings
from .converters import BooleanConverter, NumberConverter, ChartConfigConverter, EnumConverter, FileConverter, HtmlConverter

class ExportConfig(object):
    def __init__(self, config_dict=None):
        self.__configs = {}

        if config_dict is not None:
            for config_name, config_value in config_dict.items():
                self.set(config_name, config_value)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def set(self, config_name, config_value):
        #if (isinstance(config_value, dict)):
            #config_value = json.dumps(config_value)
        self.__configs[config_name] = self.__resolve_config_value(config_name, config_value)

    def __resolve_config_value(self, config_name, config_value):
        if config_name not in typings:
            raise ExportError("Invalid export config: %s" % config_name)

        if config_name == "template":
            if "templateFilePath" in self.__configs:
                print("Both 'templateFilePath' and 'template' is provided. 'templateFilePath' will be ignored.");

        if config_name == "templateFilePath":
            if "template" in self.__configs:
                print("Both 'templateFilePath' and 'template' is provided. 'templateFilePath' will be ignored.");

        converter = typings[config_name].get("converter", None)
        if converter is not None:
            if converter == "BooleanConverter":
                return BooleanConverter.convert(config_value, config_name)
            elif converter == "NumberConverter":
                return NumberConverter.convert(config_value, config_name)
            elif converter == "ChartConfigConverter":
                return ChartConfigConverter.convert(config_value)
            elif converter == "EnumConverter":
                dataset = typings[config_name].get("dataset")
                return EnumConverter.convert(config_value, dataset, config_name)
            elif converter == "FileConverter":
                return FileConverter.convert(config_value, config_name)
            elif converter == "HtmlConverter":
                return HtmlConverter.convert(config_value, config_name)
            else:
                raise ExportError("Unknown converter: %s" % converter)
        elif typings[config_name]["type"] == "string":
            return str(config_value)
        else:
            raise ExportError("Could not resolve the config name and config value")

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
        configs = self.__process_config_values()
        configs.pop(Constants.EXPORT_CONFIG_NAME_RESOURCE_FILE_PATH, None)
        return configs

    def __process_config_values(self):
        configs = self.__configs.copy()
        zip_files_map = []
        
        configs["clientName"] = "Python"

        if Constants.EXPORT_CONFIG_NAME_INPUTSVG in configs:
            self.__resolve_zip_path_config(
                configs,
                zip_files_map,
                Constants.EXPORT_CONFIG_NAME_INPUTSVG,
                Constants.EXPORT_CONFIG_ZIP_PATH_INPUTSVG
            )

        if Constants.EXPORT_CONFIG_NAME_CALLBACK_FILE_PATH in configs:
            self.__resolve_zip_path_config(
                configs,
                zip_files_map,
                Constants.EXPORT_CONFIG_NAME_CALLBACK_FILE_PATH,
                Constants.EXPORT_CONFIG_ZIP_PATH_CALLBACK_FILE_PATH
            )
        
        if Constants.EXPORT_CONFIG_NAME_DASHBOARD_LOGO in configs:
            ext = os.path.splitext(configs[Constants.EXPORT_CONFIG_NAME_DASHBOARD_LOGO])[1]
            self.__resolve_zip_path_config(
                configs,
                zip_files_map,
                Constants.EXPORT_CONFIG_NAME_DASHBOARD_LOGO,
                Constants.EXPORT_CONFIG_ZIP_PATH_DASHBOARD_LOGO + ext
            )

        if Constants.EXPORT_CONFIG_NAME_OUTPUT_FILE_DEFINITION in configs:
            self.__resolve_zip_path_config(
                configs,
                zip_files_map,
                Constants.EXPORT_CONFIG_NAME_OUTPUT_FILE_DEFINITION,
                Constants.EXPORT_CONFIG_ZIP_PATH_OUTPUT_FILE_DEFINITION
            )

        if Constants.EXPORT_CONFIG_NAME_TEMPLATE_FILE_PATH in configs:
            fileContent = configs[Constants.EXPORT_CONFIG_NAME_TEMPLATE_FILE_PATH]
            # If it is not a file but html content, then save the content to a temp file and set the path of that temp file
            if (fileContent.startswith("<")):
                tmp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
                tmp.writelines(fileContent)
                tmp.close();
                configs[Constants.EXPORT_CONFIG_NAME_TEMPLATE_FILE_PATH] = tmp.name

            template_zip_files_map, prefixed_template_zip_path = Utils.create_template_zip_paths(
                configs[Constants.EXPORT_CONFIG_NAME_TEMPLATE_FILE_PATH],
                configs.get(Constants.EXPORT_CONFIG_NAME_RESOURCE_FILE_PATH, None)
            )
            configs[Constants.EXPORT_CONFIG_NAME_TEMPLATE_FILE_PATH] = prefixed_template_zip_path
            zip_files_map.extend(template_zip_files_map)

        if Constants.EXPORT_CONFIG_NAME_ASYNC_CAPTURE in configs:
            bool_val = configs[Constants.EXPORT_CONFIG_NAME_ASYNC_CAPTURE]
            configs[Constants.EXPORT_CONFIG_NAME_ASYNC_CAPTURE] = str(bool_val).lower()

        if len(zip_files_map) > 0:
            zip_file_path = Utils.generate_zip_file(zip_files_map)
            configs[Constants.EXPORT_CONFIG_NAME_PAYLOAD] = zip_file_path
        
        return configs

    def __resolve_zip_path_config(self, configs, zip_files_map, config_name, zip_path):
        zip_files_map.append({
            "zipPath": zip_path,
            "localPath": configs[config_name]
        })
        configs[config_name] = zip_path

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
