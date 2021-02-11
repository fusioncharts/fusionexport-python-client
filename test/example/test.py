from fusionexport import ExportManager, ExportConfig

export_config = ExportConfig()
export_config["chartConfig"] = "chart-config-file.json"
export_config["templateFilePath"] = "./dashboard-template.html"

export_server_host = "127.0.0.1"
export_server_port = 1337

em = ExportManager(export_server_host, export_server_port)
exported_files = em.export(export_config, "./exported", True)
print(exported_files)