# -*- coding: utf-8 -*-


from fusionexport import ExportManager, ExportConfig


def read_file(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        print(e)


def on_export_done(event, error):
    if error:
        print(error)
    else:
        ExportManager.save_exported_files("./exported_images", event["result"])


def on_export_state_changed(event):
    print(event["state"])


chart_config = read_file("./template-test/dashboard/chart-config.json")
export_server_host = "127.0.0.1"
export_server_port = 1337

export_config = ExportConfig()
export_config["chartConfig"] = chart_config
# export_config["exportAsZip"] = True
# export_config["inputSVG"] = "./template-test/sample.svg"
# export_config["type"] = "xsls"
export_config["templateFilePath"] = "./template-test/dashboard/template.html"
export_config["resourceFilePath"] = "./template-test/dashboard/resources.json"
export_config["dashboardLogo"] = "/Users/rousan/Projects/fusionexport-python-client/template-test/dashboard/angular-smgkcu.zip"
export_config["dashboardHeading"] = "AI is best"
export_config["dashboardSubheading"] = "A sdf sfsd"
# export_config["callbackFilePath"] = "./template-test/callback.js"

em = ExportManager(export_server_host, export_server_port)
em.export(export_config, on_export_done, on_export_state_changed)