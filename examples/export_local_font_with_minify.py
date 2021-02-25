from fusionexport import ExportManager, ExportConfig

export_config = ExportConfig()
export_config["chartConfig"] = "resources/chartconfig_file.json"
export_config["templateFilePath"] = "./resources/dashboardtemplate.html"
export_config["type"] = "png"

export_server_host = "127.0.0.1"
export_server_port = 1337

em = ExportManager(export_server_host, export_server_port, minify_resources=True)
exported_files = em.export(export_config, "./exported", True)
print(exported_files)