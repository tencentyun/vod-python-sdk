import logging
from .common import StringUtil, FileUtil
from .exception import VodClientException
from .model import VodUploadResponse
from tencentcloud.common import credential
from tencentcloud.vod.v20180717 import vod_client, models
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from qcloud_cos import CosConfig, CosS3Client


logger = logging.getLogger(__name__)


class VodUploadClient:
    def __init__(self, secret_id, secret_key, token=None):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.token = token
        self.ignore_check = False
        self.retry_time = 3

    def upload(self, region, request):
        if not self.ignore_check:
            self._prefix_check_and_set_default_val(region, request)

        request_str = request.to_json_string()
        logger.info("vod upload req = {}, region = {}".format(request_str, region))
        cred = credential.Credential(self.secret_id, self.secret_key, self.token)
        api_client = vod_client.VodClient(cred, region)

        apply_upload_request = models.ApplyUploadRequest()
        apply_upload_request.from_json_string(request_str)
        apply_upload_response = self.apply_upload(api_client, apply_upload_request)
        logger.info("vod upload ApplyUpload rsp = {}".format(apply_upload_response.to_json_string()))

        if apply_upload_response.TempCertificate is None:
            cos_config = CosConfig(
                Region=apply_upload_response.StorageRegion,
                SecretId=self.secret_id,
                SecretKey=self.secret_key
            )
        else:
            temp_certificate = apply_upload_response.TempCertificate
            cos_config = CosConfig(
                Region=apply_upload_response.StorageRegion,
                SecretId=temp_certificate.SecretId,
                SecretKey=temp_certificate.SecretKey,
                Token=temp_certificate.Token
            )
        cos_client = CosS3Client(cos_config)

        if StringUtil.is_not_empty(request.MediaType) \
                and StringUtil.is_not_empty(apply_upload_response.MediaStoragePath):
            self.upload_cos(
                cos_client,
                request.MediaFilePath,
                apply_upload_response.StorageBucket,
                apply_upload_response.MediaStoragePath[1:],
                request.ConcurrentUploadNumber
            )
        if StringUtil.is_not_empty(request.CoverType) \
                and StringUtil.is_not_empty(apply_upload_response.CoverStoragePath):
            self.upload_cos(
                cos_client,
                request.CoverFilePath,
                apply_upload_response.StorageBucket,
                apply_upload_response.CoverStoragePath[1:],
                request.ConcurrentUploadNumber
            )

        commit_upload_request = models.CommitUploadRequest()
        commit_upload_request.VodSessionKey = apply_upload_response.VodSessionKey
        commit_upload_request.SubAppId = request.SubAppId

        commit_upload_response = self.commit_upload(api_client, commit_upload_request)
        commit_upload_response_str = commit_upload_response.to_json_string()
        logger.info("vod upload CommitUpload rsp = {}".format(commit_upload_response_str))

        response = VodUploadResponse()
        response.from_json_string(commit_upload_response_str)

        return response

    @staticmethod
    def upload_cos(cos_client, local_path, bucket, cos_path, max_thread):
        if max_thread is None:
            cos_client.upload_file(
                Bucket=bucket,
                LocalFilePath=local_path,
                Key=cos_path
            )
        else:
            cos_client.upload_file(
                Bucket=bucket,
                LocalFilePath=local_path,
                Key=cos_path,
                MAXThread=max_thread
            )

    def apply_upload(self, api_client, request):
        err_info = None
        for i in range(self.retry_time):
            try:
                response = api_client.ApplyUpload(request)
                return response
            except TencentCloudSDKException as err:
                if StringUtil.is_empty(err.get_request_id()):
                    err_info = err
                    continue
                raise err
        raise err_info

    def commit_upload(self, api_client, request):
        err_info = None
        for i in range(self.retry_time):
            try:
                response = api_client.CommitUpload(request)
                return response
            except TencentCloudSDKException as err:
                if StringUtil.is_empty(err.get_request_id()):
                    err_info = err
                    continue
                raise err
        raise err_info

    @staticmethod
    def _prefix_check_and_set_default_val(region, request):
        if StringUtil.is_empty(region):
            raise VodClientException("lack region")
        if StringUtil.is_empty(request.MediaFilePath):
            raise VodClientException("lack media path")
        if not FileUtil.is_file_exist(request.MediaFilePath):
            raise VodClientException("media path is invalid")
        if StringUtil.is_empty(request.MediaType):
            video_type = FileUtil.get_file_type(request.MediaFilePath)
            if StringUtil.is_empty(video_type):
                raise VodClientException("lack media type")
            request.MediaType = video_type
        if StringUtil.is_empty(request.MediaName):
            request.MediaName = FileUtil.get_file_name(request.MediaFilePath)

        if not StringUtil.is_empty(request.CoverFilePath):
            if not FileUtil.is_file_exist(request.CoverFilePath):
                raise VodClientException("cover path is invalid")
            if StringUtil.is_empty(request.CoverType):
                cover_type = FileUtil.get_file_type(request.CoverFilePath)
                if StringUtil.is_empty(cover_type):
                    raise VodClientException("lack cover type")
                request.CoverType = cover_type
