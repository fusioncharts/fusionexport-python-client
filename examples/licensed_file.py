#!/usr/bin/env python

from fusionexport import ExportManager, ExportConfig  # Import sdk


def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print e


# Called when export is done
def on_export_done(result, error):
    if error:
        print error
    else:
        print result


# Called on each export state change
def on_export_state_changed(state):
    print state


# Instantiate the ExportConfig class and add the required configurations
export_config = ExportConfig()
export_config["chartConfig"] = read_file("chart-config-file.json")
export_config["libraryDirectoryPath"] = "fullpath/of/fusioncharts"

# Instantiate the ExportManager class
em = ExportManager()
# Call the export() method with the export config and the respective callbacks
em.export(export_config, on_export_done, on_export_state_changed)
