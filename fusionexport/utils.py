import sys
import base64
import json
import os
import glob2
import tempfile
import shutil
from bs4 import BeautifulSoup

from .constants import Constants
from .export_error import ExportError

class Utils(object):
    @staticmethod
    def read_text_file(file_path):
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def json_parse(value):
        try:
            return json.loads(value)
        except Exception:
            return None

    @staticmethod
    def create_template_zip_paths(template_file_path, resource_file_path):
        template_file_path = os.path.abspath(template_file_path)

        ref_files = Utils.extract_ref_files_from_template(template_file_path)
        base_path, res_paths = Utils.normalize_resource_file_paths(resource_file_path)
        if base_path is None:
            base_path = Utils.get_common_path([template_file_path] + ref_files)
        
        if base_path == "":
            raise ExportError("Couldn't calculate the basepath of template resources")
        
        res_paths = filter(lambda path: Utils.is_within_path(path, base_path), res_paths)

        zip_files_map = Utils.create_template_zip_files_map(
            ref_files + res_paths + [template_file_path],
            base_path
        )

        prefixed_template_file_zip_path = os.path.join(
            Constants.TEMPLATE_ZIP_PREFIX,
            Utils.get_rel_path_within_root(template_file_path, base_path)
        )

        return zip_files_map, prefixed_template_file_zip_path
    
    @staticmethod
    def create_template_zip_files_map(paths, base_path):
        return map(
            lambda path: { "zipPath": Utils.create_prefixed_template_zip_path(path, base_path), "localPath": path },
            paths
        )
    
    @staticmethod
    def create_prefixed_template_zip_path(local_path, base_path):
        rel_path = Utils.get_rel_path_within_root(local_path, base_path)
        return os.path.join(Constants.TEMPLATE_ZIP_PREFIX, rel_path)
    
    @staticmethod
    def generate_zip_file(zip_files_map):
        temp_dir = tempfile.mkdtemp()
        temp_write_dir = os.path.abspath(os.path.join(temp_dir, "files"))
        os.makedirs(temp_write_dir)

        for path_map in zip_files_map:
            rel_path = path_map["zipPath"]
            if rel_path is not None:
                rel_path = rel_path.strip(os.sep)
                temp_output_file_path = os.path.abspath(os.path.join(temp_write_dir, rel_path))
                if not os.path.exists(os.path.dirname(temp_output_file_path)):
                    os.makedirs(os.path.dirname(temp_output_file_path))
                shutil.copyfile(path_map["localPath"], temp_output_file_path)

        return shutil.make_archive(os.path.abspath(os.path.join(temp_dir, "archive")), 'zip', temp_write_dir)
    
    @staticmethod
    def is_within_path(target_path, parent_path):
        return target_path.startswith(parent_path + os.sep)

    @staticmethod
    def get_rel_path_within_root(path, root_path):
        rel_path = os.path.relpath(path, root_path)
        if not rel_path.startswith(os.pardir + os.sep):
            return rel_path

    @staticmethod
    def get_common_path(paths):
        return os.path.abspath(os.path.dirname(os.path.commonprefix(paths)))

    @staticmethod
    def extract_ref_files_from_template(template_file_path):
        if template_file_path is None:
            return []

        ref_files = []
        template_file_path = os.path.abspath(template_file_path)
        template_file_dir = os.path.dirname(template_file_path)
        html_template = Utils.read_text_file(template_file_path)
        html_soup = BeautifulSoup(html_template, 'html.parser')

        for link in html_soup.find_all('link'):
            ref = Utils.resolve_template_ref(link.get("href"), template_file_dir)
            if ref is not None:
                ref_files.append(ref)

        for script in html_soup.find_all('script'):
            ref = Utils.resolve_template_ref(script.get("src"), template_file_dir)
            if ref is not None:
                ref_files.append(ref)

        for img in html_soup.find_all('img'):
            ref = Utils.resolve_template_ref(img.get("src"), template_file_dir)
            if ref is not None:
                ref_files.append(ref)

        return ref_files

    @staticmethod
    def normalize_resource_file_paths(resource_file_path):
        if resource_file_path is None:
            return None, []

        resource_file_path = os.path.abspath(resource_file_path)
        resource_file_dir = os.path.dirname(resource_file_path)

        rc_config = Utils.json_parse(Utils.read_text_file(resource_file_path))
        if rc_config is None:
            raise ExportError("Failed to parse the resource JSON file")

        base_path = rc_config.get("basePath", None)
        # Resolve base_path wrt resource_file_dir not cwd
        base_path = os.path.abspath(os.path.join(resource_file_dir, base_path)) if base_path is not None else None

        include_paths = Utils.glob_matched_paths(rc_config.get("include", None), resource_file_dir)
        exclude_paths = Utils.glob_matched_paths(rc_config.get("exclude", None), resource_file_dir)

        return base_path, list(set(include_paths).difference(set(exclude_paths)))

    @staticmethod
    def resolve_template_ref(ref, template_file_dir):
        if ref is None or ref == "":
            return None

        if not Utils.is_url(ref):
            return os.path.abspath(os.path.join(template_file_dir, ref))

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
    def is_url(value):
        value = str(value)
        prefixes = ["//", "http://", "https://", "file://"]
        for prefix in prefixes:
            if value.startswith(prefix):
                return True
        return False
