from fusionexport import ExportManager, ExportConfig  # Import sdk

# Instantiate the ExportConfig class and add the required configurations
export_config = ExportConfig()

export_config["chartConfig"] = "./resources/single.json"
export_config["type"] = 'csv'
# Instantiate the ExportManager class
em = ExportManager()

# Call the export() method with the export config and the output location
exported_files = em.export(export_config, "./exported-charts", True)

# print list of exported files
print(exported_files)