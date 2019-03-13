from fusionexport import ExportManager, ExportConfig

export_config = ExportConfig()
export_config["chartConfig"] = "chart-config.json"
# #export_config["inputSVG"] = "./chart.svg"
# export_config["chartConfig"] = "./template-test/dashboard/chart-config.json"
# export_config["templateFilePath"] = "./template-test/dashboard/template.html"
# export_config["resourceFilePath"] = "./template-test/resources.json"

export_server_host = "127.0.0.1"
export_server_port = 1337

em = ExportManager(export_server_host, export_server_port)
exported_files = em.export(export_config, "./exported", True)
print(exported_files)