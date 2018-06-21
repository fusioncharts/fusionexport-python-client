#!/usr/bin/env python

from fusionexport import ExportManager, ExportConfig  # Import sdk


def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(e)


# Called when export is done
def on_export_done(event, error):
    if error:
        print(error)
    else:
        ExportManager.save_exported_files("exported_images", event["result"])


# Called on each export state change
def on_export_state_changed(event):
    print(event["state"])


# Instantiate the ExportConfig class and add the required configurations
export_config = ExportConfig()
export_config["templateFilePath"] = "template_highcharts.html"
export_config["type"] = "pdf"
export_config["asyncCapture"] = "true"

# Provide port and host of FusionExport Service
export_server_host = "127.0.0.1"
export_server_port = 1337

# Instantiate the ExportManager class
em = ExportManager(export_server_host, export_server_port)
# Call the export() method with the export config and the respective callbacks
em.export(export_config, on_export_done, on_export_state_changed)
