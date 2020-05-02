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
client = VodUploadClient("your secretId", "your secretKey")
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
            self.assertEqual(err.message, "invalid video type")

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


if __name__ == '__main__':
    unittest.main()
