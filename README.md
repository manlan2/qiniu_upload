# qiniu_upload

通过命令行将指定目录下的文件资源上传到 [七牛云存储服务](https://portal.qiniu.com/) 

## 安装

```shell
  $ pip install qiniu_upload
```

## 使用说明

创建以下格式的配置文件（请将xxxxxx替换成实际值）：

```
{
    "access_key": "xxxxxx",
    "secret_key": "xxxxxx",
    "bucket_name": "xxxxxx"
}
```

### 例子

```shell
   $ qiniu_upload -c ~/config.json -s ~/directory_need_to_upload //常规上传
   $ qiniu_upload -c ~/config.json -s ~/directory_need_to_upload -r //上传前清空远程资源
```

### Usage
```shell
  $ qiniu_upload -h
  
  Usage: qiniu_upload [options]
  
  Options:
    -h, --help            show this help message and exit
    -c  CONFIG, --config=CONFIG set config file path
    -s  SOURCE, --source=SOURCE set local file(directory) path
    -r, --remove          remove remote files before uploading
    -v, --version         show version number
```

## 感谢
>- [七牛Python-SDK](https://github.com/qiniu/python-sdk)

## License
>- [MIT](http://www.opensource.org/licenses/MIT)



