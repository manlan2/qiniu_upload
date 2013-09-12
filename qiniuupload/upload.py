#-*- coding: utf-8 -*-
import os
import sys
import config
import StringIO
import qiniu.io
import qiniu.rs
import qiniu.conf
import qiniu.resumable_io
from urllib2 import urlopen
from urllib2 import HTTPError
from termcolor import colored

class Upload():
    def __init__(self, path, config_path):
        config_instance = config.Config(config_path)

        self.path = path
        self.lock_file = 'qiniu.lock'
        self.domain = config_instance.get_domain()
        self.bucket_name = config_instance.get_bucket_name()
        self.config_dir = os.path.abspath(config_path + '/../')
        qiniu.conf.ACCESS_KEY = str(config_instance.get_access_key())
        qiniu.conf.SECRET_KEY = str(config_instance.get_secret_key())

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

    def _get_upload_token(self):
        return qiniu.rs.PutPolicy(self.bucket_name).token()

    def _upload_lock_file(self, uploaded_files):
        if uploaded_files:
            qiniu.rs.Client().delete(self.bucket_name, self.lock_file)

            file_data = '\n'.join(uploaded_files)
            extra = qiniu.resumable_io.PutExtra(self.bucket_name)
            extra.mime_type = "text/plain"
            ret, error = qiniu.resumable_io.put(
                self._get_upload_token(),
                self.lock_file,
                StringIO.StringIO(file_data),
                len(file_data),
                extra
            )

            if error is not None:
                print(colored('Lock file %s created failed' % self.lock_file,  'red'))
            else:
                print('Lock file %s created successful' % self.lock_file)

    def _remove_remote_unuseful_files(self, upload_files):
        lock_file_url = qiniu.rs.GetPolicy().make_request(
            qiniu.rs.make_base_url(self.domain, self.lock_file)
        )

        try:
            remote_files = urlopen(lock_file_url).read().split('\n')
            remove_files = [remote_file for remote_file in remote_files if remote_file not in upload_files]
            for remove_file in remove_files:
                ret, error = qiniu.rs.Client().delete(self.bucket_name, remote_file)
                if error is not None:
                    print(colored('Remote file %s deleted failed' % remote_file, 'red'))
                else:
                    print('Remote file %s deleted successful' % remote_file)
        except HTTPError:
            return False

    def run(self):
        print(colored('Uploading local files...', 'magenta'))
        upload_files = self._get_upload_files()
        if upload_files:
            uptoken = self._get_upload_token()
            uploaded_files = []
            for upload_file in upload_files:
                upload_file_key = upload_file.replace(
                    self.config_dir + '/', ''
                ).replace('/', '_')

                ret, error = qiniu.io.put_file(
                    uptoken, upload_file_key, upload_file
                )
                if error is not None:
                    print(colored('File %s uploaded failed' % upload_file, 'red'))
                else:
                    uploaded_files.append(upload_file_key)
                    print('File %s uploaded successful' % upload_file)

            print(colored('\nRemoving remote unuseful files...', 'magenta'))
            self._remove_remote_unuseful_files(uploaded_files)

            print(colored('\nUploading %s...' % self.lock_file, 'magenta'))
            self._upload_lock_file(uploaded_files)