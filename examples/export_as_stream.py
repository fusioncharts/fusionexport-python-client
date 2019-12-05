import shutil
import os

#!/usr/bin/env python
from fusionexport import ExportManager, ExportConfig  # Import sdk


# Instantiate the ExportConfig class and add the required configurations
export_config = ExportConfig()

export_config["chartConfig"] = "config-user.json"

# Instantiate the ExportManager class
em = ExportManager(host="127.0.0.1", port=1337)

# Call the export() method with the export config and the output location
exported_files = em.exportAsStream(export_config, unzip=False)

# print list of exported files
print("Exported file(s): ")
for file in exported_files:
    with open(file, 'wb') as f:
        f.write(exported_files[file])
        print("\t" + os.path.abspath(file))

