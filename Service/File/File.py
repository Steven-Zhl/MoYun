import re
from os import path, listdir, remove

from Service.utils import getConfig


class FileMgr:
    """文件管理"""

    def __init__(self, workPath: str):
        storagePath = workPath + getConfig("Path", "StoragePath")
        self._storagePath = storagePath.replace("\\", "/")  # images文件夹路径，所有图片文件都放在这里
        self._projPath = workPath.replace("\\", "/")  # 项目根目录，用以将绝对路径转换为相对路径
        if not path.exists(storagePath):
            raise FileNotFoundError("storagePath not found")
        if not path.exists(workPath):
            raise FileNotFoundError("workPath not found")
        # 让project和storage路径都不以"/"结尾
        self._projPath = self._projPath[:-1] if self._projPath[-1] == "/" else self._projPath  # 去除projPath末尾的"/"
        self._storagePath = self._storagePath[:-1] if self._storagePath[-1] == "/" else self._storagePath
        # 初始化该目录下其他文件夹路径
        self._bookCoverPath = self._storagePath + "/" + "bookCover"  # 书籍封面
        self._journalHeaderPath = self._storagePath + "/" + "journalHeader"  # 书评封面
        self._profilePhotoPath = self._storagePath + "/" + "profilePhoto"  # 头像
        self._groupIconPath = self._storagePath + "/" + "groupIcon"  # 群组头像
        self._errorImagePath = self._storagePath + "/" + "errorImage"  # 错误提示图片

    """book"""

    def getBookCoverPath(self, bookID, abs=False, enableDefault=True) -> str:
        """
        寻找书籍封面路径
        :param bookID: 书籍ID
        :param abs: 是否返回绝对路径
        :param enableDefault: 是否允许返回默认路径(找不到的情况下)
        :return: 封面图路径
        """
        for i in listdir(self._bookCoverPath):
            if re.match(f"{bookID}\..+", i):
                absPath = self._bookCoverPath + "/" + i
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
        else:
            if enableDefault:
                relPath = self._bookCoverPath + "/" + "default.jpg"
                relPath = relPath.replace(self._projPath, "")
                return relPath
            else:
                return ""

    """journal"""

    def getJournalHeaderPath(self, journalID, abs=False, enableDefault=True) -> str:
        """
        寻找书评封面路径
        :param journalID: 期刊ID
        :param abs: 是否返回绝对路径
        :param enableDefault: 是否允许返回默认路径(找不到的情况下)
        :return: 封面图路径
        """
        for i in listdir(self._journalHeaderPath):
            if re.match(f"{journalID}\..+", i):
                absPath = self._journalHeaderPath + "/" + i
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
        else:
            if enableDefault:
                relPath = self._journalHeaderPath + "/" + "default.jpg"
                relPath = relPath.replace(self._projPath, "")
                return relPath
            else:
                return ""

    def generateJournalHeaderPath(self, journalID, abs=False) -> str:
        """
        生成书评封面图片应存放的路径
        :param journalID: 书评ID
        :param abs: 是否返回绝对路径
        :return:
        """
        absPath = self._journalHeaderPath + "/" + f"{journalID}.jpg"
        relPath = absPath.replace(self._projPath, "")
        return absPath if abs else relPath

    def deleteJournalHeader(self, journalID) -> bool:
        """
        删除书评封面图片
        :param journalID: 书评ID
        :return: True(删除成功)/False(文件不存在)
        """
        for i in listdir(self._journalHeaderPath):
            if re.match(f"{journalID}\..+", i):
                remove(self._journalHeaderPath + "/" + i)
                return True
        else:
            return False

    """profile"""

    def getProfilePhotoPath(self, userID, abs=False, enableDefault=True) -> str:
        """
        寻找头像路径
        :param userID: 用户ID
        :param abs: 是否返回绝对路径
        :param enableDefault: 是否允许返回默认路径
        :return: 头像路径
        """
        for i in listdir(self._profilePhotoPath):
            if re.match(f"{userID}\..+", i):
                absPath = self._profilePhotoPath + "/" + i
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
        else:
            if enableDefault:
                absPath = self._profilePhotoPath + "/" + "default.jpg"
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
            else:
                return ''

    def generateProfilePhotoPath(self, userID, abs=False) -> str:
        """
        生成头像图片应存放的路径
        :param userID: 用户ID
        :param abs: 是否返回绝对路径
        :return:
        """
        absPath = self._profilePhotoPath + "/" + f"{userID}.jpg"
        relPath = absPath.replace(self._projPath, "")
        return absPath if abs else relPath

    def deleteProfilePhoto(self, userID) -> bool:
        """
        删除头像图片
        :param userID: 用户ID
        :return: True(删除成功)/False(文件不存在)
        """
        for i in listdir(self._profilePhotoPath):
            if re.match(f"{userID}\..+", i):
                remove(self._profilePhotoPath + "/" + i)
                return True
        else:
            return False

    """group"""

    def getGroupIconPath(self, groupID, abs=False, enableDefault=True) -> str:
        """
        寻找群组头像路径
        :param groupID:
        :param abs:
        :param enableDefault:
        :return:
        """
        for i in listdir(self._groupIconPath):
            if re.match(f"{groupID}\..+", i):
                absPath = self._groupIconPath + "/" + i
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
        else:
            if enableDefault:
                absPath = self._groupIconPath + "/" + "default.jpg"
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
            else:
                return ''
    def deleteGroupIcon(self, groupID) -> bool:
        """
        删除群组头像图片
        :param groupID: 群组ID
        :return: True(删除成功)/False(文件不存在)
        """
        for i in listdir(self._groupIconPath):
            if re.match(f"{groupID}\..+", i):
                remove(self._groupIconPath + "/" + i)
                return True
        else:
            return False
    def generateGroupIconPath(self, groupID, abs=False) -> str:
        """
                生成圈子icon应存放的路径
                :param groupID: 圈子ID
                :param abs: 是否返回绝对路径
                :return:
                """
        absPath = self._groupIconPath + "/" + f"{groupID}.jpg"
        relPath = absPath.replace(self._projPath, "")
        return absPath if abs else relPath
    """error"""

    def getErrorImagePath(self, errorCode: int, abs=False):
        """
        获取错误详情页的图片
        :param errorCode: 错误码
        :param abs: 是否返回绝对路径
        :return:
        """
        for i in listdir(self._errorImagePath):
            if re.match(f"{errorCode}\..+", i):
                absPath = self._errorImagePath + "/" + i
                relPath = absPath.replace(self._projPath, "")
                return absPath if abs else relPath
        else:
            return ''
