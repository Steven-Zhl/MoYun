import os

import cv2

__doc__ = """图像处理相关方法"""


def getImageSize(filePath: str) -> (int, int):
    """
    依次是高度, 宽度
    :param filePath:
    :return:
    """
    if not os.path.exists(filePath):
        raise False
    img = cv2.imread(filePath)
    return img.shape[0], img.shape[1]


def cropImage(filePath: str, width: int, height: int, hAlign: str = "center", vAlign: str = "center") -> bool:
    """
    裁剪图片，注意：会直接覆盖原图片
    :param filePath: 图片路径
    :param width: 裁剪后的宽度
    :param height: 裁剪后的高度
    :param hAlign: 水平对齐方式，可选值为"left", "center", "right"
    :param vAlign: 垂直对齐方式，可选值为"top", "center", "bottom"
    :return: True(裁剪成功)/False(裁剪失败，指定的宽or高大于原图)
    """
    if not os.path.exists(filePath):
        raise False
    img = cv2.imread(filePath)
    originHeight, originWidth = img.shape[0], img.shape[1]
    if width > originWidth or height > originHeight:
        return False
    if hAlign == "left":
        widthRange = (0, width)
    elif hAlign == "center":
        widthRange = ((originWidth - width) // 2, (originWidth + width) // 2)
    elif hAlign == "right":
        widthRange = (originWidth - width, originWidth)
    else:
        raise ValueError("hAlign must be one of 'left', 'center', 'right'")
    if vAlign == "top":
        height_range = (0, height)
    elif vAlign == "center":
        height_range = ((originHeight - height) // 2, (originHeight + height) // 2)
    elif vAlign == "bottom":
        height_range = (originHeight - height, originHeight)
    else:
        raise ValueError("vAlign must be one of 'top', 'center', 'bottom'")
    img = img[height_range[0]:height_range[1], widthRange[0]:widthRange[1]]
    cv2.imwrite(filePath, img)
    return True


def cropImageByScale(filePath: str, width: int, height: int):
    """
    根据比例(Width:height)居中最大裁剪，注意：会直接覆盖原图片
    :param filePath: 图片路径
    :param width: 宽度比例
    :param height: 高度比例
    :return:
    """
    if not os.path.exists(filePath):
        raise False
    img = cv2.imread(filePath)
    originHeight, originWidth = img.shape[0], img.shape[1]
    if originWidth / originHeight > width / height:
        newWidth = originHeight * width // height
        newHeight = originHeight
    else:
        newWidth = originWidth
        newHeight = originWidth * height // width
    img = img[(originHeight - newHeight) // 2:(originHeight + newHeight) // 2,
          (originWidth - newWidth) // 2:(originWidth + newWidth) // 2]
    cv2.imwrite(filePath, img)
    return True


def cropImageSquare(filePath: str):
    """
    裁剪图片为正方形(最大尺寸裁切)
    :param filePath:
    :return:
    """
    if not os.path.exists(filePath):
        raise False
    img = cv2.imread(filePath)
    originHeight, originWidth = img.shape[0], img.shape[1]
    if originWidth == originHeight:
        return True
    edgeLength = min(originWidth, originHeight)
    if originWidth > originHeight:
        newImg = img[:, (originWidth - edgeLength) // 2:(originWidth + edgeLength) // 2]
    else:
        newImg = img[(originHeight - edgeLength) // 2:(originHeight + edgeLength) // 2, :]
    cv2.imwrite(filePath, newImg)
    return True
