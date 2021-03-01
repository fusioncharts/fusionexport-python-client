from fusionexport import ExportManager, ExportConfig

export_config = ExportConfig()
export_config["chartConfig"] = "resources/chartconfig_big.json"
export_config["templateFilePath"] = "resources/dashboard_big_template.html"

em = ExportManager(minify_resources=True)
exported_files = em.export(export_config, "./exported", True)
print(exported_files)