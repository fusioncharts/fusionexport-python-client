#!/usr/bin/env python

from fusionexport import ExportManager, ExportConfig  # Import sdk


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
export_config["inputSVG"] = "fullpath/of/chart.svg"

# Instantiate the ExportManager class
em = ExportManager()
# Call the export() method with the export config and the respective callbacks
em.export(export_config, on_export_done, on_export_state_changed)
