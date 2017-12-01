FusionExport Python Client
==========================

Language SDK for FusionExport which enables exporting of charts & dashboards through Python.

Installation
------------

To install this Python package, simply use ``pip``:

.. code-block:: shell

    pip install fusionexport


Getting Started
---------------

After installing the package, create a new file named ``chart-config.json`` which contains
the chart configurations to be exported. Before exporting your chart, make sure
the export server is running.

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

      #!/usr/bin/env python

      from fusionexport import ExportManager, ExportConfig  # Import sdk


      def read_file(file_path):
          try:
              with open(file_path, "r") as f:
                  return f.read()
          except Exception as e:
              print(e)


      # Called when export is done
      def on_export_done(result, error):
          if error:
              print(error)
          else:
              print(result)


      # Called on each export state change
      def on_export_state_changed(state):
          print(state)


      # Instantiate the ExportConfig class and add the required configurations
      export_config = ExportConfig()
      export_config["chartConfig"] = read_file("chart-config.json")

      # Instantiate the ExportManager class
      em = ExportManager()
      # Call the export() method with the export config and the respective callbacks
      em.export(export_config, on_export_done, on_export_state_changed)

Now run this file, then the exported chart will be received on ``ExportDone`` event.


`API Reference <https://www.fusioncharts.com/dev/exporting-charts/using-fusionexport/sdk-api-reference/python.html>`_
----------------------------------------------------------------------------------------------------------------------

