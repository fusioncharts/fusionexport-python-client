FusionExport Python Client
==========================

Language SDK for FusionExport which enables exporting of charts and dashboards through Python.


Installation
------------

To install this Python package, use pip:

.. code-block:: shell

    pip install fusionexport


Usage
-----

To use the SDK in your project:

.. code-block:: python

    from fusionexport import ExportManager, ExportConfig



Getting Started
---------------

Start with a simple chart export. For exporting a single chart just pass the chart configuration as you would have passed it to the FusionCharts constructor.

.. code-block:: python

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

        # Instantiate the ExportManager class
        em = ExportManager()

        # Call the export() method with the export config and the output location
        exported_files = em.export(export_config, "./exported-charts", True)

        # print list of exported files
        print(exported_files)


Now run this file, then the exported chart files will be saved in ``./exported-charts`` folder.


API Reference
-------------
You can find the full reference `here <https://www.fusioncharts.com/dev/exporting-charts/using-fusionexport/sdk-api-reference/python.html>`_