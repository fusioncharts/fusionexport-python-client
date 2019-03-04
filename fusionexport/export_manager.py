import os
import base64
import io
import requests
import tempfile
import shutil
import zipfile

from .export_error import ExportError
from .constants import Constants
from .utils import Utils

class ExportManager(object):
    def __init__(self, host=None, port=None):
        if host is not None:
            self.__host = host
        else:
            self.__host = Constants.DEFAULT_SERVICE_HOST

        if port is not None:
            self.__port = port
        else:
            self.__port = Constants.DEFAULT_SERVICE_PORT

    def port(self, port=None):
        if port is not None:
            self.__port = port
        else:
            return self.__port

    def host(self, host=None):
        if host is not None:
            self.__host = host
        else:
            return self.__host

    def convertResultToBase64String(self, export_files):
        files = []
        for file in export_files:
            print("FILE: %s" % file)
            with open(file, "rb") as sfile:
                encoded_string = base64.b64encode(sfile.read())
            files.append(encoded_string)
        return files

    def export(self, export_config, output_dir='.', unzip=False):
        configs = export_config.get_formatted_configs()
        payloadData = {}
        zip_file_path = None
        zip_file_fd = None

        for config_name, config_value in configs.items():
            if config_name == Constants.EXPORT_CONFIG_NAME_PAYLOAD:
                zip_file_path = config_value
                zip_file_fd = open(zip_file_path, 'rb')
                payloadData[config_name] = ("archive.zip", zip_file_fd, "application/zip")
            else:
                payloadData[config_name] = (None, config_value)
        try:
            res = requests.post(self.__api_url(), files=payloadData, stream=True)
            if not res.status_code == 200:
                if zip_file_path is not None:
                    zip_file_fd.close()
                    shutil.rmtree(os.path.dirname(zip_file_path))
                raise ExportError(res.text)

            temp_dir = tempfile.mkdtemp()
            temp_export_zip_file = os.path.abspath(os.path.join(temp_dir, "python_" + Constants.EXPORT_ZIP_FILE_NAME))

            with open(temp_export_zip_file, 'wb') as fd:
                for chunk in res.iter_content(chunk_size=1024):
                    fd.write(chunk)

            output_dir = os.path.abspath(output_dir)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)


            export_files = []
            if unzip:
                zip_ref = zipfile.ZipFile(temp_export_zip_file, 'r')
                zip_ref.extractall(output_dir)
                export_files.extend(list(filter(lambda entry: not entry.endswith("/"), zip_ref.namelist())))
                zip_ref.close()
            else:
                shutil.copyfile(temp_export_zip_file, os.path.abspath(os.path.join(output_dir, Constants.EXPORT_ZIP_FILE_NAME)))
                export_files.append(Constants.EXPORT_ZIP_FILE_NAME)

            if zip_file_path is not None:
                zip_file_fd.close()
                shutil.rmtree(os.path.dirname(zip_file_path))

            shutil.rmtree(temp_dir)

            files = []
            for file in export_files:
                f = os.path.join(output_dir, file)
                files.append(f)

            return files

        except (requests.ConnectionError, requests.ConnectTimeout):
            raise ExportError("Connection Refused: Unable to connect to FusionExport server. Make sure that your server is running on %s:%s" % (self.__host, self.__port))

    def __api_url(self):
        return "http://%s:%d/api/v2.0/export" % (self.__host, self.__port)
