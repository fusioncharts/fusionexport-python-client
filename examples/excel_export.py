from fusionexport import ExportManager, ExportConfig  # Import sdk

# Instantiate the ExportConfig class and add the required configurations
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

export_config["type"] = 'xlsx'
# Instantiate the ExportManager class
em = ExportManager()

# Call the export() method with the export config and the output location
exported_files = em.export(export_config, "./exported-charts", True)

# print list of exported files
print(exported_files)