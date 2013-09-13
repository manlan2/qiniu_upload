#-*- coding: utf-8 -*-
import optparse
from os import path
from sys import exit
from upload import Upload
from qiniuupload import __version__

def run():
    program = optparse.OptionParser()
    program.add_option(
        '--config', '-c', help = 'set config file path'
    )
    program.add_option(
        '--source', '-s', help = 'set local file(directory) path'
    )
    program.add_option(
        '--remove', '-r', help = 'remove remote files before uploading',
        action = 'store_true', default = False
    )
    program.add_option(
        '--version', '-v', help = 'show version number', action = 'store_true'
    )

    options, arguments = program.parse_args()

    if options.version == True:
        print(__version__)
        exit()

    if options.config and options.source:
        if not path.exists(options.config):
            print('Usage: qiniu_upload [options]\n')
            print('qiniu_upload error: config file `%s` not found' % options.config)
            exit(2)

        if not path.exists(options.source):
            print('Usage: qiniu_upload [options]\n')
            print('qiniu_upload error: source file(directory) `%s` not found' % options.source)
            exit(2)

        upload = Upload(options.source, options.config, options.remove)
        upload.run()
    else:
        print('Usage: qiniu_upload [options]\n')
        print('qiniu_upload: error: -%s option requires an argument' % ('c' if options.source else 's'))
        exit(2)
