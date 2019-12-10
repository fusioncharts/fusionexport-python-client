#!/usr/bin/env python
from fusionexport import ExportManager, ExportConfig  # Import sdk


# Instantiate the ExportConfig class and add the required configurations
export_config = ExportConfig()

export_config["chartConfig"] = "multiple.json"
export_config["outputFile"] = "export-<%= number(5) %>"
export_config["type"] = "pdf"
export_config["templateFormat"] = "A4"

# Instantiate the ExportManager class
em = ExportManager()

# Call the export() method with the export config and the output location
exported_files = em.export(export_config, "./exports", True)

# print list of exported files
print(exported_files)