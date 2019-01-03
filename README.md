## 简介

基于 Python 语言平台的服务端上传的 SDK，通过 SDK 和配合的 Demo，可以将视频和封面文件直接上传到腾讯云点播系统，同时可以指定各项服务端上传的可选参数。

## 使用方式

### 通过 Pip 安装(推荐)
您可以通过 pip 安装方式将 SDK 安装到您的项目中，如果您的项目环境尚未安装 pip，请详细参见 pip 官网安装。

```
pip install vod-python-sdk
```


### 通过源码包安装

下载最新代码，解压后：
```
$ cd vod-python-sdk
$ python setup.py install
```

## 示例

```
from qcloud_vod.vod_upload_client import VodUploadClient
from qcloud_vod.model import VodUploadRequest

try:
    client = VodUploadClient("your secretId", "your secretKey")
    request = VodUploadRequest()
    request.MediaFilePath = "/data/file/Wildlife.mp4"
    response = client.upload("ap-guangzhou", request)
    print(response.FileId)
except Exception as err:
    print(err)
```
