from fusionexport import ExportManager, ExportConfig

export_config = ExportConfig()
export_config["chartConfig"] = [{
            "type": "column2d",
            "renderAt": "chart-container",
            "width": "600",
            "height": "400",
            "dataFormat": "json",
            "dataSource": {
                "chart": {
                    "caption": "Number of visitors last week",
                    "subCaption": "Bakersfield Central vs Los Angeles Topanga"
                },
                "data": [{
                        "label": "Mon",
                        "value": "15123"
                    },{
                        "label": "Tue",
                        "value": "14233"
                    },{
                        "label": "Wed",
                        "value": "25507"
                    }
                ]
            }
        }]
export_server_host = "127.0.0.1"
export_server_port = 1337
is_secure = True
em = ExportManager(export_server_host, export_server_port, is_secure)
exported_files = em.export(export_config, "./exported", True)
print(exported_files)