import os


class StringUtil(object):
    @staticmethod
    def is_empty(target):
        return target is None or target == ""

    @staticmethod
    def is_not_empty(target):
        return not StringUtil.is_empty(target)


class FileUtil(object):
    @staticmethod
    def is_file_exist(target):
        return os.path.isfile(target)

    @staticmethod
    def get_file_type(target):
        info = os.path.splitext(target)
        if info[-1] == "":
            return ""
        return info[-1][1:]

    @staticmethod
    def get_file_name(target):
        path_info = os.path.split(target)
        info = os.path.splitext(path_info[-1])
        return info[0]
