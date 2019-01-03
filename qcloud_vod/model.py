from tencentcloud.vod.v20180717 import models


class VodUploadRequest(models.ApplyUploadRequest):
    def __init__(self):
        super().__init__()
        self.MediaFilePath = None
        self.CoverFilePath = None
        self.ConcurrentUploadNumber = None


class VodUploadResponse(models.CommitUploadResponse):
    def __init__(self):
        super().__init__()
