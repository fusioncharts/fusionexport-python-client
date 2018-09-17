FusionExport Python Client
==========================

Language SDK for FusionExport which enables exporting of charts and dashboards through Python.


Installation
------------

To install this Python package, use pip:

.. code-block:: shell

    pip install fusionexport


Getting Started
---------------

After installing the package, create a new file named ``chart-config.json`` which contains
the chart configurations to be exported. Before exporting your chart, make sure
the FusionExport service is running.

The ``chart-config.json`` file looks as shown below:

.. code-block:: json

   [{
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
           "data": [
               {
                   "label": "Mon",
                   "value": "15123"
               },
               {
                   "label": "Tue",
                   "value": "14233"
               },
               {
                   "label": "Wed",
                   "value": "25507"
               }
           ]
       }
   }]


Now, import the ``fusionexport`` module into your project and write export logic as follows:

.. code-block:: python

      from fusionexport import ExportManager, ExportConfig  # Import sdk

      # Instantiate the ExportConfig class and add the required configurations
      export_config = ExportConfig()
      export_config["chartConfig"] = "./chart-config.json"

      # Provide port and host of FusionExport Service
      export_server_host = "127.0.0.1"
      export_server_port = 1337

      # Instantiate the ExportManager class
      em = ExportManager(export_server_host, export_server_port)
      # Call the export() method with the export config and the output location
      exported_files = em.export(export_config, "./exported-charts")
      print(exported_files)


Now run this file, then the exported chart files will be saved in ``./exported-charts`` folder.


API Reference
-------------
You can find the full reference `here <https://www.fusioncharts.com/dev/exporting-charts/using-fusionexport/sdk-api-reference/python.html>`_