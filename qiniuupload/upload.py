#-*- coding: utf-8 -*-
import os
import sys
import config
import StringIO
import qiniu.io
import qiniu.rs
import qiniu.rsf
import qiniu.conf
from termcolor import colored

class Upload():
    def __init__(self, path, config_path, remove_remote_files):
        config_instance = config.Config(config_path)

        self.path = path
        self.remove_remote_files = remove_remote_files
        self.bucket_name = config_instance.get_bucket_name()
        self.config_dir = os.path.abspath(config_path + '/../')

        qiniu.conf.ACCESS_KEY = str(config_instance.get_access_key())
        qiniu.conf.SECRET_KEY = str(config_instance.get_secret_key())

    def _get_remote_files(self):
        rets, err = qiniu.rsf.Client().list_prefix(self.bucket_name)
        return [ret['key'] for ret in rets['items']]

    def _remove_remote_files(self):
        print(colored('Removing remote files...', 'magenta'))
        remote_files = self._get_remote_files()
        if remote_files:
            for remote_file in remote_files:
                ret, error = qiniu.rs.Client().delete(self.bucket_name, remote_file)
                if error is not None:
                    print(colored('Remote file %s removed failed' % remote_file, 'red'))
                else:
                    print('Remote file %s removed successful' % remote_file)

    def _get_upload_files(self):
        if not os.path.exists(self.path):
            return None

        if os.path.isfile(self.path):
            return [self.path]

        if os.path.isdir(self.path):
            result = []
            for root, dirs, files in os.walk(self.path):
                result += [root + '/' + file_path for file_path in files]
            return result

        return None

    def _upload(self):
        print(colored('Uploading local files...', 'magenta'))
        upload_files = self._get_upload_files()
        if upload_files:

            for upload_file in upload_files:
                upload_file_key = upload_file.replace(
                    self.config_dir + '/', ''
                ).replace('/', '_')

                uptoken = qiniu.rs.PutPolicy(
                    '%s:%s' % (self.bucket_name, upload_file_key)
                ).token()

                ret, error = qiniu.io.put_file(
                    uptoken, upload_file_key, upload_file
                )
                if error is not None:
                    print(colored('File %s uploaded failed' % upload_file, 'red'))
                else:
                    print('File %s uploaded successful' % upload_file)

    def run(self):
        if self.remove_remote_files == True:
            self._remove_remote_files()

        self._upload()
