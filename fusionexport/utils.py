# -*- coding: utf-8 -*-


import base64
import json
import os
import glob2
import tempfile
import shutil
from bs4 import BeautifulSoup

from .constants import Constants


class Utils(object):
    """Contains utility methods"""

    __export_metadata = None

    @staticmethod
    def read_file_in_base64(file_path):
        base64_content = base64.b64encode(Utils.read_binary_file(file_path))
        if (not isinstance(base64_content, str)) and isinstance(base64_content, bytes):
            base64_content = base64_content.decode("utf-8")
        return base64_content

    @staticmethod
    def read_binary_file(file_path):
        with open(file_path, "rb") as f:
            return f.read()

    @staticmethod
    def read_text_file(file_path):
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def json_stringify(value):
        try:
            return json.dumps(value)
        except Exception:
            return None

    @staticmethod
    def json_parse(value):
        try:
            return json.loads(value)
        except Exception:
            return None

    @staticmethod
    def get_export_metadata_file_path():
        return {
            "meta": os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), Constants.EXPORT_METADATA_FILES["meta"])),
            "typings": os.path.abspath(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), Constants.EXPORT_METADATA_FILES["typings"]))
        }

    @staticmethod
    def get_export_metadata():
        metadata_file_path = Utils.get_export_metadata_file_path()
        if Utils.__export_metadata is None:
            Utils.__export_metadata = {
                "meta": Utils.json_parse(Utils.read_text_file(metadata_file_path["meta"])),
                "typings": Utils.json_parse(Utils.read_text_file(metadata_file_path["typings"]))
            }
        return Utils.__export_metadata

    @staticmethod
    def get_zipped_template_in_base64(template_file_path, resource_file_path):
        template_file_path = os.path.abspath(template_file_path)
        template_file_refs = Utils.__extract_ref_files_from_template(template_file_path)
        base_path, resource_file_paths = Utils.__normalize_resource_file_paths(resource_file_path)

        all_paths = [template_file_path] + template_file_refs + resource_file_paths

        if base_path is None:
            base_path = Utils.get_common_path(all_paths)

        temp_dir = tempfile.mkdtemp()
        temp_write_dir = os.path.abspath(os.path.join(temp_dir, "fusioncharts"))
        os.makedirs(temp_write_dir)

        for path in all_paths:
            rel_path = Utils.get_rel_path_within_root(path, base_path)
            if rel_path is not None:
                temp_output_file_path = os.path.abspath(os.path.join(temp_write_dir, rel_path))
                if not os.path.exists(os.path.dirname(temp_output_file_path)):
                    os.makedirs(os.path.dirname(temp_output_file_path))
                shutil.copyfile(path, temp_output_file_path)

        template_rel_path_within_zip = Utils.get_rel_path_within_root(template_file_path, base_path)
        if template_rel_path_within_zip is None:
            template_rel_path_within_zip = os.path.basename(template_file_path)

        temp_template_output_file_path = os.path.abspath(os.path.join(temp_write_dir, template_rel_path_within_zip))
        if not os.path.exists(temp_template_output_file_path):
            shutil.copyfile(template_file_path, temp_template_output_file_path)

        shutil.make_archive(os.path.abspath(os.path.join(temp_dir, "fusioncharts")), 'zip', temp_write_dir)

        base64_zip = Utils.read_file_in_base64(os.path.abspath(os.path.join(temp_dir, "fusioncharts.zip")))
        shutil.rmtree(temp_dir)

        return template_rel_path_within_zip, base64_zip

    @staticmethod
    def get_rel_path_within_root(path, root_path):
        rel_path = os.path.relpath(path, root_path)
        if not rel_path.startswith(os.pardir + os.sep):
            return rel_path

    @staticmethod
    def get_common_path(paths):
        return os.path.abspath(os.path.dirname(os.path.commonprefix(paths)))

    @staticmethod
    def __extract_ref_files_from_template(template_file_path):
        if template_file_path is None:
            return []

        ref_files = []
        template_file_path = os.path.abspath(template_file_path)
        template_file_dir = os.path.dirname(template_file_path)
        html_template = Utils.read_text_file(template_file_path)
        html_soup = BeautifulSoup(html_template, 'html.parser')

        for link in html_soup.find_all('link'):
            ref = Utils.__resolve_template_ref(link.get("href"), template_file_dir)
            if ref is not None:
                ref_files.append(ref)

        for script in html_soup.find_all('script'):
            ref = Utils.__resolve_template_ref(script.get("src"), template_file_dir)
            if ref is not None:
                ref_files.append(ref)

        for img in html_soup.find_all('img'):
            ref = Utils.__resolve_template_ref(img.get("src"), template_file_dir)
            if ref is not None:
                ref_files.append(ref)

        return ref_files

    @staticmethod
    def __normalize_resource_file_paths(resource_file_path):
        if resource_file_path is None:
            return None, []

        resource_file_path = os.path.abspath(resource_file_path)
        resource_file_dir = os.path.dirname(resource_file_path)
        rc_config = Utils.json_parse(Utils.read_text_file(resource_file_path))
        base_path = rc_config.get("basePath", None)  # Resolve base_path wrt resource_file_dir not cwd
        base_path = os.path.abspath(os.path.join(resource_file_dir, base_path)) if base_path is not None else None

        include_paths = Utils.glob_matched_paths(rc_config.get("include", None), resource_file_dir)
        exclude_paths = Utils.glob_matched_paths(rc_config.get("exclude", None), resource_file_dir)

        return base_path, list(set(include_paths).difference(set(exclude_paths)))

    @staticmethod
    def __resolve_template_ref(ref, template_file_dir):
        if not Utils.is_url(ref):
            return Utils.resolve_url_to_path(ref, template_file_dir)

    @staticmethod
    def glob_matched_paths(glob_pats, root_path):
        if glob_pats is None:
            return []

        root_path = os.path.abspath(root_path)
        matched_paths = []

        prev_cwd = os.getcwd()
        os.chdir(root_path)

        for glob_pat in glob_pats:
            for path in glob2.iglob(glob_pat):
                path = os.path.abspath(os.path.join(root_path, path))
                if os.path.isfile(path):
                    matched_paths.append(path)

        os.chdir(prev_cwd)
        return matched_paths

    @staticmethod
    def resolve_url_to_path(relative_url, root_path):
        return os.path.abspath(os.path.join(root_path, relative_url))

    @staticmethod
    def is_url(value):
        value = str(value)
        prefixes = ["//", "http://", "https://", "file://"]
        for prefix in prefixes:
            if value.startswith(prefix):
                return True
        return False
