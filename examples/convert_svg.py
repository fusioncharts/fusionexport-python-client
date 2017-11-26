#!/usr/bin/env python

from fusionexport import ExportManager, ExportConfig


def on_export_done(result, error):
    if error:
        print error
    else:
        print result


def on_export_state_changed(state):
    print state


export_server_host = "127.0.0.1"
export_server_port = 1337

export_config = ExportConfig()
export_config["inputSVG"] = "fullpath/of/chart.svg"

em = ExportManager(export_server_host, export_server_port)
em.export(export_config, on_export_done, on_export_state_changed)
