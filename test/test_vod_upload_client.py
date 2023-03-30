from qcloud_vod.vod_upload_client import VodUploadClient
from qcloud_vod.model import VodUploadRequest
from qcloud_vod.exception import VodClientException
import unittest
import logging
import sys
import os
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
client = VodUploadClient("Your SecretId", "Your SecretKey")
# set credential token if necessary
# client = VodUploadClient("your secretId", "your secretKey", "your token")
path = os.path.split(os.path.abspath(__file__))[0]


class TestVodUploadClient(unittest.TestCase):
    def test_lack_media_path(self):
        request = VodUploadRequest()
        try:
            client.upload("ap-guangzhou", request)
        except VodClientException as err:
            self.assertEqual(err.message, "lack media path")

    def test_lack_media_type(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife")
        try:
            client.upload("ap-guangzhou", request)
        except VodClientException as err:
            self.assertEqual(err.message, "lack media type")

    def test_invalid_media_path(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "WildlifeA")
        try:
            client.upload("ap-guangzhou", request)
        except VodClientException as err:
            self.assertEqual(err.message, "media path is invalid")

    def test_invalid_cover_path(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.CoverFilePath = os.path.join(path, "Wildlife-CoverA")
        try:
            client.upload("ap-guangzhou", request)
        except VodClientException as err:
            self.assertEqual(err.message, "cover path is invalid")

    def test_lack_cover_type(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.CoverFilePath = os.path.join(path, "Wildlife-Cover")
        try:
            client.upload("ap-guangzhou", request)
        except VodClientException as err:
            self.assertEqual(err.message, "lack cover type")

    def test_invalid_media_type(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.MediaType = "test"
        try:
            client.upload("ap-guangzhou", request)
        except TencentCloudSDKException as err:
            self.assertEqual(err.message, "invalid media type")

    def test_invalid_cover_type(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.CoverFilePath = os.path.join(path, "Wildlife-Cover.png")
        request.MediaType = "mp4"
        request.CoverType = "ttt"
        try:
            client.upload("ap-guangzhou", request)
        except TencentCloudSDKException as err:
            self.assertEqual(err.message, "invalid cover type")

    def test_upload(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.CoverFilePath = os.path.join(path, "Wildlife-Cover.png")
        response = client.upload("ap-guangzhou", request)
        self.assertIsNotNone(response.FileId)

    def test_upload_with_progress_callback(self):      
        """仅支持对 20M 以上的文件回调上传进度
        """
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.CoverFilePath = os.path.join(path, "Wildlife-Cover.png")
        response = client.upload("ap-guangzhou", request, upload_percentage)
        self.assertIsNotNone(response.FileId)

    def test_upload_with_procedure(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.Procedure = "QCVB_SimpleProcessFile(1, 1)"
        response = client.upload("ap-guangzhou", request)
        self.assertIsNotNone(response.FileId)

    def test_upload_with_storage_region(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.StorageRegion = "ap-chongqing"
        response = client.upload("ap-guangzhou", request)
        self.assertIsNotNone(response.FileId)

    def test_upload_with_media_name(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "Wildlife.mp4")
        request.MediaName = "test_test"
        response = client.upload("ap-guangzhou", request)
        self.assertIsNotNone(response.FileId)

    def test_upload_hls(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "hls", "prog_index.m3u8")
        response = client.upload("ap-guangzhou", request)
        self.assertIsNotNone(response.FileId)

    def test_upload_hls_masterplaylist(self):
        request = VodUploadRequest()
        request.MediaFilePath = os.path.join(path, "hls", "bipbopall.m3u8")
        response = client.upload("ap-guangzhou", request)
        self.assertIsNotNone(response.FileId)


def upload_percentage(consumed_bytes, total_bytes):
    """默认上传进度回调函数，计算当前上传的百分比

    :param consumed_bytes: 已经上传的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\ruploaded {0} bytes, percent {1}% '.format(consumed_bytes, rate))
        sys.stdout.flush()


if __name__ == '__main__':
    unittest.main()
