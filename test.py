# -*- coding: utf-8 -*-


from fusionexport import ExportManager, ExportConfig, Utils, BooleanConverter, NumberConverter
import json

#
# def read_file(file_path):
#     try:
#         with open(file_path, "r") as f:
#             return f.read()
#     except Exception as e:
#         print(e)
#
#
# def on_export_done(result, error):
#     if error:
#         print(error)
#     else:
#         print(ExportManager.save_exported_files("./exported_images", result))
#
#
# def on_export_state_changed(state):
#     print(state)
#     pass
#
#
# chart_config = read_file("chart-config.json")
# export_server_host = "127.0.0.1"
# export_server_port = 1337
#
# export_config = ExportConfig()
# export_config["chartConfig"] = chart_config
#
# em = ExportManager(export_server_host, export_server_port)
# em.export(export_config, on_export_done, on_export_state_changed)

d = {
    "chartConfig": '[{"x": 2}, {"ss": "\\n"}]'
}

ec = ExportConfig(d)
print(ec.get_formatted_configs())