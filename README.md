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

### 上传

```shell
   $ qiniu_upload upload -c ~/config.json -s ~/directory_need_to_upload
```

### 删除

```shell
   $ qiniu_upload remove -c ~/config.json -p file_prefix // 如未设置-p属性，则清空当前bucket下所有文件
```


## 感谢
>- [七牛Python-SDK](https://github.com/qiniu/python-sdk)

## License
>- [MIT](http://www.opensource.org/licenses/MIT)


## Release History

_2013-09-16   v0.1.1   （1）支持覆盖已有文件（2）将删除文件的逻辑从上传逻辑中剥离出来_

_2013-09-13   v0.1.0   发布第一版本_


