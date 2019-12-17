
#!/usr/bin/env python

import os.path as op
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from fusionexport import ExportManager, ExportConfig  # Import sdk

# Instantiate the ExportConfig class and add the required configurations
export_config = ExportConfig()
export_config["chartConfig"] = "resources/multiple.json"
export_config["templateFilePath"] = "resources/template.html"
export_config["type"] = "pdf"
export_config["headerEnabled"] = True

# Provide port and host of FusionExport Service
export_server_host = "127.0.0.1"
export_server_port = 1337

# Instantiate the ExportManager class
em = ExportManager(export_server_host, export_server_port)
# Call the export() method with the export config and the output location
exported_files = em.export(export_config, "./exports", True)

# Sending email
mail = MIMEMultipart()
mail['From'] = "<FROM EMAIL ID>"
mail['To'] = "<TO EMAIL ID>"
mail['Subject'] = "FusionExport"
mail.attach(MIMEText('''Hello,

Kindly find the attachment of FusionExport exported files.

Thank you!''', 'plain'))

# Attaching files
for f in exported_files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(open(f, 'rb').read())
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % op.basename(f)
        mail.attach(part)

# Connect to SMTP Server
server = smtplib.SMTP('smtp.mailtrap.io: 587')
server.starttls()
server.login('9217733c3a014f', '39564c5d1ddd00')
server.sendmail(mail['From'], mail['To'], mail.as_string())
server.quit()

print ("FusionExport Python Client: email sent")