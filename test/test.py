# -*- coding: utf-8 -*-


from fusionexport import ExportManager, ExportConfig


def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(e)


def on_export_done(event, error):
    if error:
        print(error)
    else:
        ExportManager.save_exported_files("exported_images", event["result"])


def on_export_state_changed(event):
    print(event["state"])


export_config = ExportConfig()
export_config["chartConfig"] = read_file("chart-config.json")

export_server_host = "127.0.0.1"
export_server_port = 1337

em = ExportManager(export_server_host, export_server_port)
em.export(export_config, on_export_done, on_export_state_changed)