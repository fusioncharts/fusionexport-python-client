# -*- coding: utf-8 -*-


import os
import base64
import boto3
import ftplib
import io

from .constants import Constants
from .exporter import Exporter
from .utils import Utils


class ExportManager(object):
    """Exports charts using specified host and port of Export Server"""

    def __init__(self, host=None, port=None):
        if host is not None:
            self.__host = host
        else:
            self.__host = Constants.DEFAULT_HOST

        if port is not None:
            self.__port = port
        else:
            self.__port = Constants.DEFAULT_PORT

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

    def export(self, export_config=None, export_done_listener=None, export_state_changed_listener=None):
        exporter = Exporter(export_config, export_done_listener, export_state_changed_listener)
        exporter.set_export_connection_config(self.__host, self.__port)
        exporter.start()
        return exporter

    @staticmethod
    def save_exported_files(dir_path, exported_output):
        dir_path = os.path.abspath(dir_path)
        for exported_data in exported_output["data"]:
            Utils.write_binary_data(os.path.join(dir_path, exported_data["realName"]),
                                    base64.b64decode(exported_data["fileContent"]))

    @staticmethod
    def upload_to_amazon_s3(bucket_name, access_key, secret_key, exported_output):
        try:
            # Create an AS3 client
            s3client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

            # Flag for ensuring bucket exists in AS3
            bucket_exist = False

            # Iterate the list of buckets to search the desired bucket exist or not.
            list_buckets_resp = s3client.list_buckets()
            for bucket in list_buckets_resp['Buckets']:
                if bucket['Name'] == bucket_name:
                    bucket_exist = True
                    break

            if bucket_exist is True:
                # Loop for creating image file in bucket
                for exported_data in exported_output["data"]:
                    # write binary image data in bucket
                    filename = '{file_name}'.format(file_name=exported_data["realName"])
                    s3client.put_object(Bucket=bucket_name, Key=filename,
                                        Body=base64.b64decode(exported_data["fileContent"]))
            else:
                print("Failed to upload: due to bucket does not exist.")

        except Exception as e:
            print(e)

    @staticmethod
    def upload_to_ftp(ftp_host, ftp_port, user_name, login_password, remote_directory, exported_output):
        try:
            # initialize FTP
            ftp = ftplib.FTP()

            # Connect to ftp server
            ftp.connect(ftp_host, ftp_port)

            # Assign login credential
            ftp.login(user_name, login_password)

            # Generate remote path from root
            remote_location = '/{dir_name}/'.format(dir_name=remote_directory)

            # Check for remote directory exist or not, if not create directory
            if ExportManager.directory_exists(ftp, remote_directory) is False:
                ftp.mkd(remote_location)

            # Change working directory.
            ftp.cwd(remote_location)

            # Loop for creating image file in remote directory
            for exported_data in exported_output["data"]:
                # write binary image data in remote directory
                ftp.storbinary("STOR " + exported_data["realName"],
                               io.BytesIO(base64.b64decode(exported_data["fileContent"])))

        except Exception as e:
            print(e)

    @staticmethod
    def directory_exists(ftp_client, dir_name):
        file_list = []

        # Get remote file folder listing
        ftp_client.retrlines('LIST', file_list.append)

        # Check for directory exist
        for f in file_list:
            if f.split()[-1] == dir_name:
                return True

        return False

    @staticmethod
    def get_exported_file_names(exported_output):
        return [x["realName"] for x in exported_output["data"]]
